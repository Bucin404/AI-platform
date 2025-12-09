"""File attachment model."""
from app import db
from datetime import datetime


class FileAttachment(db.Model):
    """File attachment model for chat messages."""
    __tablename__ = 'file_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)  # image, video, document
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    mime_type = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('file_attachments', lazy='dynamic'))
    message = db.relationship('Message', backref=db.backref('attachments', lazy='dynamic'))
    
    def __repr__(self):
        return f'<FileAttachment {self.filename}>'
    
    def is_image(self):
        """Check if file is an image."""
        return self.file_type == 'image'
    
    def is_video(self):
        """Check if file is a video."""
        return self.file_type == 'video'
    
    def is_document(self):
        """Check if file is a document."""
        return self.file_type == 'document'
    
    def get_file_url(self):
        """Get URL to access the file."""
        from flask import url_for
        return url_for('static', filename=f'uploads/{self.filename}')
