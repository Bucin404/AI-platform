"""Payment routes."""
from flask import render_template, jsonify, request, current_app
from flask_login import login_required, current_user
from app.blueprints.payments import payments_bp
from app.models.user import Transaction
from app.services.payment_service import create_payment, process_webhook
from app import db
import logging

logger = logging.getLogger(__name__)


@payments_bp.route('/')
@login_required
def index():
    """Payment page."""
    return render_template('payments.html')


@payments_bp.route('/create', methods=['POST'])
@login_required
def create():
    """Create payment."""
    data = request.get_json()
    tier = data.get('tier', 'premium')
    duration_days = data.get('duration_days', 30)
    
    # Calculate amount based on tier and duration
    amount = 99000  # IDR per month for premium
    if duration_days == 90:
        amount = 249000  # Quarterly discount
    elif duration_days == 365:
        amount = 899000  # Annual discount
    
    try:
        payment_data = create_payment(current_user, amount, tier, duration_days)
        return jsonify(payment_data)
    except Exception as e:
        logger.error(f"Error creating payment: {str(e)}")
        return jsonify({'error': str(e)}), 500


@payments_bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle Midtrans webhook."""
    try:
        data = request.get_json()
        result = process_webhook(data)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500


@payments_bp.route('/history')
@login_required
def history():
    """Get payment history."""
    transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.created_at.desc()).all()
    
    return jsonify({
        'transactions': [{
            'id': t.id,
            'transaction_id': t.transaction_id,
            'amount': t.amount,
            'currency': t.currency,
            'status': t.status,
            'tier': t.tier,
            'duration_days': t.duration_days,
            'created_at': t.created_at.isoformat()
        } for t in transactions]
    })


@payments_bp.route('/check/<transaction_id>')
@login_required
def check_status(transaction_id):
    """Check payment status."""
    transaction = Transaction.query.filter_by(
        transaction_id=transaction_id,
        user_id=current_user.id
    ).first_or_404()
    
    return jsonify({
        'transaction_id': transaction.transaction_id,
        'status': transaction.status,
        'amount': transaction.amount,
        'created_at': transaction.created_at.isoformat()
    })
