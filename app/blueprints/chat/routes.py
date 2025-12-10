"""Chat routes."""
from flask import render_template, jsonify, request, session, Response, stream_with_context
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import json
from app.blueprints.chat import chat_bp
from app.models.user import Message, ConversationSession
from app.models.file_attachment import FileAttachment
from app.services.model_service import get_model_response
from app.utils.rate_limit import check_rate_limit
from app.translations import get_all_translations
from app import db
from datetime import datetime, timedelta

# File upload configuration
UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mov', 'avi', 'webm', 'pdf', 'doc', 'docx', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    """Determine file type from extension."""
    ext = filename.rsplit('.', 1)[1].lower()
    if ext in {'png', 'jpg', 'jpeg', 'gif', 'webp'}:
        return 'image'
    elif ext in {'mp4', 'mov', 'avi', 'webm'}:
        return 'video'
    elif ext in {'pdf', 'doc', 'docx', 'txt'}:
        return 'document'
    return 'other'


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
    
    # Check if model requires premium and user is free
    premium_models = ['code', 'deepseek', 'document', 'llama', 'image']
    if model_name in premium_models and not current_user.can_use_feature(model_name):
        return jsonify({
            'error': 'This feature requires Premium subscription',
            'upgrade_required': True
        }), 403
    
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
    
    # Get conversation context (with token limit to avoid exceeding context window)
    # Most models have 2048 token context, leave ~500 tokens for response
    context_messages = conv_session.get_context_messages(limit=None, max_tokens=1500)
    
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


@chat_bp.route('/stream', methods=['POST'])
@login_required
def stream_message():
    """Stream AI response in real-time using Server-Sent Events (SSE)."""
    # Check rate limit
    rate_limit_ok, message = check_rate_limit(current_user)
    if not rate_limit_ok:
        return jsonify({'error': message}), 429
    
    # Get request data
    data = request.get_json() if request.is_json else request.form.to_dict()
    user_message = data.get('message', '').strip()
    model_name = data.get('model', 'auto')
    
    if not user_message:
        return jsonify({'error': 'Message cannot be empty'}), 400
    
    # Check premium requirements (hermes/creative is free, removed from list)
    premium_models = ['code', 'deepseek', 'document', 'llama', 'image']
    if model_name in premium_models and not current_user.can_use_feature(model_name):
        return jsonify({'error': 'This feature requires Premium subscription', 'upgrade_required': True}), 403
    
    # Get or create session
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
    
    # Get conversation history (with token limit to avoid exceeding context window)
    context_messages = conv_session.get_context_messages(limit=None, max_tokens=1500)
    conversation_history = []
    for ctx_msg in context_messages:
        conversation_history.append({
            'role': ctx_msg.role,
            'content': ctx_msg.content
        })
    
    # Stream AI response
    @stream_with_context
    def generate():
        try:
            # Send immediate start signal to show loading started
            yield f"data: {json.dumps({'status': 'processing'})}\n\n"
            
            full_response = []
            token_count = 0
            
            # Get streaming response from AI
            generator = get_model_response(
                user_message,
                model_name,
                current_user,
                history=conversation_history,
                stream=True
            )
            
            for token in generator:
                token_count += 1
                full_response.append(token)
                # Send token as SSE event
                yield f"data: {json.dumps({'token': token})}\n\n"
            
            # Save complete response to database
            complete_response = ''.join(full_response)
            
            response_msg = Message(
                user_id=current_user.id,
                session_id=conv_session.id,
                role='assistant',
                content=complete_response,
                model=model_name
            )
            db.session.add(response_msg)
            conv_session.updated_at = datetime.utcnow()
            db.session.commit()
            
            # Send completion event
            yield f"data: {json.dumps({'done': True, 'message_id': response_msg.id, 'session_id': conv_session.id})}\n\n"
            
        except Exception as e:
            print(f"❌ Stream error: {e}")
            import traceback
            traceback.print_exc()
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    return Response(generate(), mimetype='text/event-stream')


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


@chat_bp.route('/new_session', methods=['POST'])
@login_required
def create_new_session():
    """Create a new conversation session."""
    try:
        # Create new session
        new_session = ConversationSession(user_id=current_user.id)
        db.session.add(new_session)
        db.session.commit()
        
        return jsonify({
            'session_id': new_session.id,
            'message': 'New session created'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/sessions')
@login_required
def get_sessions():
    """Get all active conversation sessions for user."""
    try:
        # Cleanup old sessions first
        cleanup_old_sessions(current_user.id)
        
        # Get active sessions
        sessions = ConversationSession.query.filter_by(
            user_id=current_user.id,
            is_active=True
        ).order_by(ConversationSession.updated_at.desc()).all()
        
        session_list = []
        for sess in sessions:
            # Get message count
            msg_count = Message.query.filter_by(session_id=sess.id).count()
            
            # Get first message as preview
            first_msg = Message.query.filter_by(
                session_id=sess.id,
                role='user'
            ).order_by(Message.created_at.asc()).first()
            
            preview = first_msg.content[:50] + '...' if first_msg and len(first_msg.content) > 50 else (first_msg.content if first_msg else 'New conversation')
            
            session_list.append({
                'id': sess.id,
                'created_at': sess.created_at.isoformat(),
                'updated_at': sess.updated_at.isoformat(),
                'message_count': msg_count,
                'preview': preview
            })
        
        return jsonify({'sessions': session_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/session/<int:session_id>')
@login_required
def get_session_messages(session_id):
    """Get all messages for a specific session."""
    try:
        # Verify session belongs to user
        session = ConversationSession.query.filter_by(
            id=session_id,
            user_id=current_user.id
        ).first()
        
        if not session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Get messages
        messages = Message.query.filter_by(
            session_id=session_id
        ).order_by(Message.created_at.asc()).all()
        
        return jsonify({
            'session_id': session_id,
            'messages': [{
                'id': msg.id,
                'role': msg.role,
                'content': msg.content,
                'model': msg.model,
                'created_at': msg.created_at.isoformat()
            } for msg in messages]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/current_session')
@login_required
def get_current_session():
    """Get or create current active session."""
    try:
        session = get_or_create_session(current_user.id)
        return jsonify({'session_id': session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/session/<int:session_id>/delete', methods=['DELETE'])
@login_required
def delete_session(session_id):
    """Delete a conversation session."""
    try:
        # Verify session belongs to user
        conv_session = ConversationSession.query.filter_by(
            id=session_id,
            user_id=current_user.id
        ).first()
        
        if not conv_session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Delete all messages in session
        Message.query.filter_by(session_id=session_id).delete()
        
        # Delete session
        db.session.delete(conv_session)
        db.session.commit()
        
        return jsonify({'message': 'Session deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@chat_bp.route('/models')
@login_required
def get_models():
    """Get available models."""
    from app.services.model_service import get_available_models
    models = get_available_models()
    return jsonify({'models': models})


@chat_bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    """Upload a file attachment."""
    # Check if user can upload files
    if not current_user.can_upload_files():
        return jsonify({
            'error': 'File uploads require Premium subscription',
            'upgrade_required': True
        }), 403
    
    # Check if file is present
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)
    
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'File size exceeds 10MB limit'}), 400
    
    # Save file securely
    filename = secure_filename(file.filename)
    unique_filename = f"{current_user.id}_{datetime.utcnow().timestamp()}_{filename}"
    file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    
    # Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    
    file.save(file_path)
    
    # Create file attachment record
    attachment = FileAttachment(
        filename=unique_filename,
        original_filename=filename,
        file_path=file_path,
        file_type=get_file_type(filename),
        file_size=file_size,
        mime_type=file.content_type,
        user_id=current_user.id
    )
    db.session.add(attachment)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'file_id': attachment.id,
        'filename': filename,
        'file_type': attachment.file_type,
        'file_url': attachment.get_file_url()
    })
