"""Payment service for Midtrans integration."""
import requests
import base64
import hashlib
from flask import current_app, url_for
from app.models.user import Transaction, User
from app.services.email_service import send_payment_success_email
from app import db
from datetime import datetime, timedelta
import logging
import uuid

logger = logging.getLogger(__name__)


def get_midtrans_headers():
    """Get Midtrans API headers."""
    server_key = current_app.config['MIDTRANS_SERVER_KEY']
    auth_string = f"{server_key}:"
    auth_bytes = auth_string.encode('ascii')
    auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
    
    return {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Basic {auth_b64}'
    }


def get_midtrans_api_url():
    """Get Midtrans API URL."""
    is_production = current_app.config['MIDTRANS_IS_PRODUCTION']
    if is_production:
        return 'https://api.midtrans.com/v2'
    else:
        return 'https://api.sandbox.midtrans.com/v2'


def create_payment(user, amount, tier='premium', duration_days=30):
    """Create a payment transaction with Midtrans."""
    # Create transaction record
    transaction_id = f"TXN-{user.id}-{uuid.uuid4().hex[:8].upper()}"
    
    transaction = Transaction(
        user_id=user.id,
        transaction_id=transaction_id,
        amount=amount,
        currency='IDR',
        status='pending',
        tier=tier,
        duration_days=duration_days
    )
    db.session.add(transaction)
    db.session.commit()
    
    # Create Midtrans payment request
    # This is a simplified version - in production, use Snap API
    payment_data = {
        'transaction_details': {
            'order_id': transaction_id,
            'gross_amount': int(amount)
        },
        'customer_details': {
            'first_name': user.username,
            'email': user.email
        },
        'item_details': [{
            'id': tier,
            'price': int(amount),
            'quantity': 1,
            'name': f'{tier.capitalize()} Subscription - {duration_days} days'
        }],
        'callbacks': {
            'finish': url_for('payments.check_status', transaction_id=transaction_id, _external=True)
        }
    }
    
    try:
        # In production, make actual API call to Midtrans
        # For now, return mock data
        logger.info(f"Payment created: {transaction_id} for user {user.id}")
        
        # Mock response
        return {
            'transaction_id': transaction_id,
            'status': 'pending',
            'payment_url': f'/payments/check/{transaction_id}',
            'amount': amount,
            'currency': 'IDR'
        }
    except Exception as e:
        logger.error(f"Error creating Midtrans payment: {str(e)}")
        raise


def process_webhook(data):
    """Process Midtrans webhook notification."""
    transaction_id = data.get('order_id')
    transaction_status = data.get('transaction_status')
    fraud_status = data.get('fraud_status', 'accept')
    
    logger.info(f"Processing webhook for {transaction_id}: {transaction_status}")
    
    transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()
    if not transaction:
        logger.error(f"Transaction not found: {transaction_id}")
        return {'status': 'error', 'message': 'Transaction not found'}
    
    # Update transaction status
    if transaction_status == 'capture':
        if fraud_status == 'accept':
            transaction.status = 'success'
    elif transaction_status == 'settlement':
        transaction.status = 'success'
    elif transaction_status in ['deny', 'cancel', 'expire']:
        transaction.status = 'failed'
    elif transaction_status == 'pending':
        transaction.status = 'pending'
    
    transaction.payment_method = data.get('payment_type')
    db.session.commit()
    
    # If payment successful, upgrade user
    if transaction.status == 'success':
        user = User.query.get(transaction.user_id)
        user.tier = transaction.tier
        user.tier_expires_at = datetime.utcnow() + timedelta(days=transaction.duration_days)
        db.session.commit()
        
        # Send confirmation email
        try:
            send_payment_success_email(user, transaction)
        except Exception as e:
            logger.error(f"Error sending payment success email: {str(e)}")
        
        logger.info(f"User {user.id} upgraded to {transaction.tier}")
    
    return {'status': 'ok', 'transaction_id': transaction_id}


def check_expired_subscriptions():
    """Check and downgrade expired premium subscriptions."""
    expired_users = User.query.filter(
        User.tier == 'premium',
        User.tier_expires_at < datetime.utcnow()
    ).all()
    
    for user in expired_users:
        user.tier = 'free'
        user.tier_expires_at = None
        logger.info(f"User {user.id} subscription expired, downgraded to free")
    
    db.session.commit()
    return len(expired_users)
