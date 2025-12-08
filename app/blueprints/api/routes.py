"""API routes."""
from flask import jsonify, request
from flask_login import login_required, current_user
from functools import wraps
from app.blueprints.api import api_bp
from app.models.user import Message
from app.services.model_service import get_model_response, get_available_models
from app.utils.rate_limit import check_rate_limit, get_user_usage_stats
from app import db


def api_key_required(f):
    """Decorator to require API key authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # For now, use session-based auth
        # In production, implement proper API key system
        if not current_user.is_authenticated:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function


@api_bp.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0'
    })


@api_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    """API endpoint for chat."""
    # Check rate limit
    rate_limit_ok, message = check_rate_limit(current_user)
    if not rate_limit_ok:
        return jsonify({'error': message}), 429
    
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    
    user_message = data.get('message', '').strip()
    model_name = data.get('model', 'gpt4all')
    
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # Save user message
    msg = Message(
        user_id=current_user.id,
        role='user',
        content=user_message,
        model=model_name
    )
    db.session.add(msg)
    db.session.commit()
    
    # Get AI response
    try:
        ai_response = get_model_response(user_message, model_name, current_user)
        
        # Save AI response
        response_msg = Message(
            user_id=current_user.id,
            role='assistant',
            content=ai_response,
            model=model_name
        )
        db.session.add(response_msg)
        db.session.commit()
        
        return jsonify({
            'response': ai_response,
            'model': model_name,
            'message_id': response_msg.id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/models', methods=['GET'])
@login_required
def models():
    """Get available models."""
    models = get_available_models()
    return jsonify({'models': models})


@api_bp.route('/usage', methods=['GET'])
@login_required
def usage():
    """Get usage statistics."""
    stats = get_user_usage_stats(current_user)
    return jsonify(stats)


@api_bp.route('/history', methods=['GET'])
@login_required
def history():
    """Get chat history."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    messages = Message.query.filter_by(user_id=current_user.id)\
        .order_by(Message.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'messages': [{
            'id': msg.id,
            'role': msg.role,
            'content': msg.content,
            'model': msg.model,
            'created_at': msg.created_at.isoformat()
        } for msg in messages.items],
        'total': messages.total,
        'pages': messages.pages,
        'current_page': messages.page
    })
