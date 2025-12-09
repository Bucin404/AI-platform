"""Rate limiting utilities."""
from datetime import datetime, timedelta
from app import db
from app.models.user import Message
import logging

logger = logging.getLogger(__name__)


def check_rate_limit(user):
    """Check if user has exceeded rate limit.
    
    Free users: No rate limit (unlimited messages with basic features)
    Premium/Admin: Tracked for statistics only, no blocking
    """
    # Free users have unlimited messages (no rate limit)
    if user.tier == 'free':
        logger.info(f"Free user {user.id}: No rate limit applied")
        return True, None
    
    # For premium/admin users: track usage but don't block
    # (keeping limits for statistics and monitoring only)
    limit = user.get_rate_limit()
    
    # Count messages in the last hour
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    message_count = Message.query.filter(
        Message.user_id == user.id,
        Message.role == 'user',
        Message.created_at >= one_hour_ago
    ).count()
    
    # Log usage but don't block (soft limit for monitoring)
    if message_count >= limit:
        logger.info(f"User {user.id} ({user.tier}) reached soft limit: {message_count}/{limit}")
    
    # Always allow messages (no blocking for any tier now)
    return True, None


def get_user_usage_stats(user):
    """Get usage statistics for a user."""
    today = datetime.utcnow().date()
    today_start = datetime.combine(today, datetime.min.time())
    
    messages_today = Message.query.filter(
        Message.user_id == user.id,
        Message.role == 'user',
        Message.created_at >= today_start
    ).count()
    
    messages_total = Message.query.filter(
        Message.user_id == user.id,
        Message.role == 'user'
    ).count()
    
    return {
        'messages_today': messages_today,
        'messages_total': messages_total,
        'rate_limit': user.get_rate_limit(),
        'tier': user.tier
    }
