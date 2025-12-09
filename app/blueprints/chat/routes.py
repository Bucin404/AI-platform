"""Chat routes."""
from flask import render_template, jsonify, request, session
from flask_login import login_required, current_user
from app.blueprints.chat import chat_bp
from app.models.user import Message, ConversationSession
from app.services.model_service import get_model_response
from app.utils.rate_limit import check_rate_limit
from app.translations import get_all_translations
from app import db
from datetime import datetime, timedelta


def get_locale():
    """Get user's preferred language from session or browser"""
    if 'lang' in session:
        return session['lang']
    browser_lang = request.accept_languages.best_match(['en', 'id'])
    session['lang'] = browser_lang or 'id'
    return session['lang']


def cleanup_old_sessions(user_id):
    """Delete conversation sessions older than 24 hours."""
    cutoff_time = datetime.utcnow() - timedelta(days=1)
    ConversationSession.query.filter(
        ConversationSession.user_id == user_id,
        ConversationSession.created_at < cutoff_time
    ).delete()
    db.session.commit()


def get_or_create_session(user_id):
    """Get active session or create new one if needed."""
    # Cleanup old sessions first
    cleanup_old_sessions(user_id)
    
    # Get most recent session
    session = ConversationSession.query.filter_by(
        user_id=user_id,
        is_active=True
    ).order_by(ConversationSession.updated_at.desc()).first()
    
    # Check if session exists and is not expired
    if session and not session.is_expired():
        return session
    
    # Create new session
    new_session = ConversationSession(user_id=user_id)
    db.session.add(new_session)
    db.session.commit()
    return new_session


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
    
    # Handle both JSON and form data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    user_message = data.get('message', '').strip()
    model_name = data.get('model', 'auto')
    
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # Get or create active conversation session
    conv_session = get_or_create_session(current_user.id)
    
    # Save user message
    msg = Message(
        user_id=current_user.id,
        session_id=conv_session.id,
        role='user',
        content=user_message,
        model=model_name
    )
    db.session.add(msg)
    db.session.commit()
    
    # Get conversation context (last 10 messages)
    context_messages = conv_session.get_context_messages(limit=10)
    
    # Build context for AI
    conversation_history = []
    for ctx_msg in context_messages:
        conversation_history.append({
            'role': ctx_msg.role,
            'content': ctx_msg.content
        })
    
    # Get AI response with context
    try:
        ai_response = get_model_response(
            user_message, 
            model_name, 
            current_user,
            history=conversation_history
        )
        
        # Save AI response
        response_msg = Message(
            user_id=current_user.id,
            session_id=conv_session.id,
            role='assistant',
            content=ai_response,
            model=model_name
        )
        db.session.add(response_msg)
        
        # Update session timestamp
        conv_session.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'response': ai_response,
            'model': model_name,
            'message_id': response_msg.id,
            'session_id': conv_session.id
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
