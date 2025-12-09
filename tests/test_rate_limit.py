"""Test rate limiting functionality."""
import pytest
from app.models.user import User, Message
from app.utils.rate_limit import check_rate_limit, get_user_usage_stats
from app import db
from datetime import datetime


def test_free_tier_rate_limit(app, init_database):
    """Test rate limit for free tier users."""
    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        
        # Should be allowed initially
        allowed, message = check_rate_limit(user)
        assert allowed is True
        
        # Add messages up to limit
        limit = user.get_rate_limit()
        for i in range(limit):
            msg = Message(
                user_id=user.id,
                role='user',
                content=f'Test message {i}',
                model='gpt4all'
            )
            db.session.add(msg)
        db.session.commit()
        
        # Should be rate limited now
        allowed, message = check_rate_limit(user)
        assert allowed is False


def test_premium_tier_rate_limit(app, init_database):
    """Test rate limit for premium tier users."""
    with app.app_context():
        user = User.query.filter_by(email='premium@example.com').first()
        
        limit = user.get_rate_limit()
        # Premium users should have higher limit
        assert limit > 10


def test_admin_rate_limit(app, init_database):
    """Test rate limit for admin users."""
    with app.app_context():
        user = User.query.filter_by(email='admin@example.com').first()
        
        limit = user.get_rate_limit()
        # Admin users should have highest limit
        assert limit >= 1000


def test_usage_stats(app, init_database):
    """Test getting user usage statistics."""
    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        
        # Add some messages
        for i in range(5):
            msg = Message(
                user_id=user.id,
                role='user',
                content=f'Test message {i}',
                model='gpt4all'
            )
            db.session.add(msg)
        db.session.commit()
        
        stats = get_user_usage_stats(user)
        assert stats['messages_today'] >= 5
        assert stats['messages_total'] >= 5
        assert 'rate_limit' in stats
        assert 'tier' in stats
