"""Rate limiting utilities."""
from datetime import datetime, timedelta
from app import db
from app.models.user import Message
import logging

logger = logging.getLogger(__name__)


def check_rate_limit(user):
    """Check if user has exceeded rate limit."""
    # Get user's rate limit
    limit = user.get_rate_limit()
    
    # Count messages in the last hour
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    message_count = Message.query.filter(
        Message.user_id == user.id,
        Message.role == 'user',
        Message.created_at >= one_hour_ago
    ).count()
    
    if message_count >= limit:
        logger.warning(f"Rate limit exceeded for user {user.id} ({user.tier}): {message_count}/{limit}")
        return False, f"Rate limit exceeded. You can send {limit} messages per hour. Please try again later."
    
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
