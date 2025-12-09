"""Chat routes."""
from flask import render_template, jsonify, request, session
from flask_login import login_required, current_user
from app.blueprints.chat import chat_bp
from app.models.user import Message
from app.services.model_service import get_model_response
from app.utils.rate_limit import check_rate_limit
from app.translations import get_all_translations
from app import db


def get_locale():
    """Get user's preferred language from session or browser"""
    if 'lang' in session:
        return session['lang']
    browser_lang = request.accept_languages.best_match(['en', 'id'])
    session['lang'] = browser_lang or 'id'
    return session['lang']


@chat_bp.route('/')
@login_required
def index():
    """Chat interface."""
    lang = get_locale()
    translations = get_all_translations(lang)
    return render_template('chat/chat.html', t=translations, lang=lang)


@chat_bp.route('/send', methods=['POST'])
@login_required
def send_message():
    """Send a chat message."""
    # Check rate limit
    rate_limit_ok, message = check_rate_limit(current_user)
    if not rate_limit_ok:
        return jsonify({'error': message}), 429
    
    data = request.get_json()
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


@chat_bp.route('/history')
@login_required
def get_history():
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


@chat_bp.route('/clear', methods=['POST'])
@login_required
def clear_history():
    """Clear chat history."""
    Message.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'message': 'Chat history cleared'})


@chat_bp.route('/models')
@login_required
def get_models():
    """Get available models."""
    from app.services.model_service import get_available_models
    models = get_available_models()
    return jsonify({'models': models})
