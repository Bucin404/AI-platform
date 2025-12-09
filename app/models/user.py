"""Database models."""
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(UserMixin, db.Model):
    """User model."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, premium, admin
    tier = db.Column(db.String(20), default='free')  # free, premium
    tier_expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    messages = db.relationship('Message', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    sessions = db.relationship('ConversationSession', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def can_use_feature(self, feature):
        """Check if user can use a specific feature based on tier."""
        free_features = ['chat', 'general', 'qa', 'basic']
        
        if self.is_premium() or self.is_admin():
            return True
        
        return feature in free_features
    
    def can_upload_files(self):
        """Check if user can upload files."""
        return self.is_premium() or self.is_admin()
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password hash."""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """Check if user is admin."""
        return self.role == 'admin'
    
    def is_premium(self):
        """Check if user is premium."""
        if self.tier == 'premium' and self.tier_expires_at:
            return datetime.utcnow() < self.tier_expires_at
        return self.tier == 'premium' and self.tier_expires_at is None
    
    def get_rate_limit(self):
        """Get rate limit based on user tier."""
        from flask import current_app
        if self.is_admin():
            return current_app.config['RATE_LIMIT_ADMIN_TIER']
        elif self.is_premium():
            return current_app.config['RATE_LIMIT_PREMIUM_TIER']
        else:
            return current_app.config['RATE_LIMIT_FREE_TIER']
    
    def __repr__(self):
        return f'<User {self.username}>'


class ConversationSession(db.Model):
    """Conversation session model for organizing chat history."""
    __tablename__ = 'conversation_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    messages = db.relationship('Message', backref='session', lazy='dynamic', cascade='all, delete-orphan')
    
    def is_expired(self):
        """Check if session is older than 24 hours."""
        from datetime import timedelta
        return datetime.utcnow() - self.created_at > timedelta(days=1)
    
    def get_context_messages(self, limit=10):
        """Get recent messages for context (last N messages)."""
        return self.messages.order_by(Message.created_at.desc()).limit(limit).all()[::-1]
    
    def __repr__(self):
        return f'<ConversationSession {self.id} for User {self.user_id}>'


class Message(db.Model):
    """Chat message model."""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey('conversation_sessions.id'), nullable=True)
    role = db.Column(db.String(20), nullable=False)  # user, assistant, system
    content = db.Column(db.Text, nullable=False)
    model = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tokens = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Message {self.id} by User {self.user_id}>'


class Transaction(db.Model):
    """Payment transaction model."""
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='IDR')
    status = db.Column(db.String(20), default='pending')  # pending, success, failed
    payment_method = db.Column(db.String(50), nullable=True)
    tier = db.Column(db.String(20), default='premium')
    duration_days = db.Column(db.Integer, default=30)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Transaction {self.transaction_id}>'


class PromptTemplate(db.Model):
    """Custom prompt template model."""
    __tablename__ = 'prompt_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<PromptTemplate {self.name}>'


class Feedback(db.Model):
    """User feedback model."""
    __tablename__ = 'feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='open')  # open, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Feedback {self.id}>'
