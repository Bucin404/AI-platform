"""Main blueprint."""
from flask import Blueprint, render_template
from flask_login import current_user

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page."""
    if current_user.is_authenticated:
        return render_template('index.html')
    return render_template('landing.html')


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@main_bp.route('/faq')
def faq():
    """FAQ page."""
    return render_template('faq.html')


@main_bp.route('/pricing')
def pricing():
    """Pricing page."""
    return render_template('pricing.html')
