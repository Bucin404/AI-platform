"""Email service for sending emails."""
from flask import current_app, render_template, url_for
from flask_mail import Message
from app import mail
import logging

logger = logging.getLogger(__name__)


def send_email(subject, recipients, text_body, html_body):
    """Send email."""
    try:
        msg = Message(subject, recipients=recipients)
        msg.body = text_body
        msg.html = html_body
        mail.send(msg)
        logger.info(f"Email sent to {recipients}: {subject}")
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")


def send_password_reset_email(user):
    """Send password reset email."""
    reset_url = url_for('auth.reset_password', token=user.reset_token, _external=True)
    subject = 'Password Reset Request - AI Platform'
    
    text_body = f"""Dear {user.username},

You have requested to reset your password. Please click the link below to reset your password:

{reset_url}

This link will expire in 1 hour.

If you did not request this password reset, please ignore this email.

Best regards,
AI Platform Team
"""
    
    html_body = render_template('email/password_reset.html', user=user, reset_url=reset_url)
    
    send_email(subject, [user.email], text_body, html_body)


def send_registration_email(user):
    """Send registration confirmation email."""
    subject = 'Welcome to AI Platform!'
    
    text_body = f"""Dear {user.username},

Welcome to AI Platform! Your account has been successfully created.

You can now log in and start using our AI chat services.

Best regards,
AI Platform Team
"""
    
    html_body = render_template('email/registration.html', user=user)
    
    send_email(subject, [user.email], text_body, html_body)


def send_payment_success_email(user, transaction):
    """Send payment success email."""
    subject = 'Payment Successful - AI Platform'
    
    text_body = f"""Dear {user.username},

Your payment has been successfully processed!

Transaction ID: {transaction.transaction_id}
Amount: {transaction.amount} {transaction.currency}
Tier: {transaction.tier}

Thank you for upgrading to premium!

Best regards,
AI Platform Team
"""
    
    html_body = render_template('email/payment_success.html', user=user, transaction=transaction)
    
    send_email(subject, [user.email], text_body, html_body)
