"""Main blueprint."""
from flask import Blueprint, render_template, jsonify, session, request
from flask_login import current_user
from app.translations import get_all_translations

main_bp = Blueprint('main', __name__)


def get_locale():
    """Get user's preferred language from session or browser"""
    # Check if language is already set in session
    if 'lang' in session:
        return session['lang']
    
    # Otherwise, try to get from browser
    browser_lang = request.accept_languages.best_match(['en', 'id'])
    session['lang'] = browser_lang or 'id'  # Default to Indonesian
    return session['lang']


@main_bp.route('/set_language/<lang>')
def set_language(lang):
    """Set user's preferred language"""
    if lang in ['en', 'id']:
        session['lang'] = lang
    return jsonify({'status': 'success', 'lang': session.get('lang', 'id')})


@main_bp.route('/')
def index():
    """Home page."""
    lang = get_locale()
    translations = get_all_translations(lang)
    if current_user.is_authenticated:
        return render_template('index.html', t=translations, lang=lang)
    return render_template('landing.html', t=translations, lang=lang)


@main_bp.route('/about')
def about():
    """About page."""
    lang = get_locale()
    translations = get_all_translations(lang)
    return render_template('about.html', t=translations, lang=lang)


@main_bp.route('/faq')
def faq():
    """FAQ page."""
    lang = get_locale()
    translations = get_all_translations(lang)
    return render_template('faq.html', t=translations, lang=lang)


@main_bp.route('/pricing')
def pricing():
    """Pricing page."""
    lang = get_locale()
    translations = get_all_translations(lang)
    return render_template('pricing.html', t=translations, lang=lang)


@main_bp.route('/health')
def health():
    """Health check endpoint for monitoring and Docker."""
    return jsonify({
        'status': 'healthy',
        'service': 'ai-smooht',
        'version': '1.0.0'
    }), 200
