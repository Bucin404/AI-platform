"""Admin routes."""
from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from functools import wraps
from app.blueprints.admin import admin_bp
from app.models.user import User, Message, Transaction
from app import db
from datetime import datetime, timedelta


def admin_required(f):
    """Decorator to require admin access."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('You need admin privileges to access this page.', 'error')
            return redirect(url_for('chat.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@login_required
@admin_required
def index():
    """Admin dashboard."""
    # Get statistics
    total_users = User.query.count()
    premium_users = User.query.filter_by(tier='premium').count()
    total_messages = Message.query.count()
    total_transactions = Transaction.query.filter_by(status='success').count()
    
    # Recent users
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    return render_template('admin_dashboard.html',
                         total_users=total_users,
                         premium_users=premium_users,
                         total_messages=total_messages,
                         total_transactions=total_transactions,
                         recent_users=recent_users)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """List all users."""
    page = request.args.get('page', 1, type=int)
    users = User.query.paginate(page=page, per_page=20, error_out=False)
    return render_template('admin_users.html', users=users)


@admin_bp.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Edit user."""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        data = request.get_json()
        
        if 'role' in data:
            user.role = data['role']
        if 'tier' in data:
            user.tier = data['tier']
        if 'is_active' in data:
            user.is_active = data['is_active']
        
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    
    # Get user stats
    message_count = Message.query.filter_by(user_id=user.id).count()
    transactions = Transaction.query.filter_by(user_id=user.id).all()
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'tier': user.tier,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'message_count': message_count
        },
        'transactions': [{
            'id': t.id,
            'transaction_id': t.transaction_id,
            'amount': t.amount,
            'status': t.status,
            'created_at': t.created_at.isoformat()
        } for t in transactions]
    })


@admin_bp.route('/stats')
@login_required
@admin_required
def stats():
    """Get usage statistics."""
    # Daily stats for the last 7 days
    stats_data = []
    for i in range(7):
        date = datetime.utcnow().date() - timedelta(days=i)
        date_start = datetime.combine(date, datetime.min.time())
        date_end = datetime.combine(date, datetime.max.time())
        
        messages = Message.query.filter(
            Message.created_at >= date_start,
            Message.created_at <= date_end
        ).count()
        
        new_users = User.query.filter(
            User.created_at >= date_start,
            User.created_at <= date_end
        ).count()
        
        stats_data.append({
            'date': date.isoformat(),
            'messages': messages,
            'new_users': new_users
        })
    
    return jsonify({'stats': stats_data})


@admin_bp.route('/users/<int:user_id>/usage')
@login_required
@admin_required
def user_usage(user_id):
    """Get user usage details."""
    user = User.query.get_or_404(user_id)
    
    # Message count by day for last 30 days
    usage_data = []
    for i in range(30):
        date = datetime.utcnow().date() - timedelta(days=i)
        date_start = datetime.combine(date, datetime.min.time())
        date_end = datetime.combine(date, datetime.max.time())
        
        messages = Message.query.filter(
            Message.user_id == user.id,
            Message.created_at >= date_start,
            Message.created_at <= date_end
        ).count()
        
        usage_data.append({
            'date': date.isoformat(),
            'messages': messages
        })
    
    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'usage': usage_data
    })
