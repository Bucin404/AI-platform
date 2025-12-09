"""Authentication blueprint."""
from flask import Blueprint

auth_bp = Blueprint('auth', __name__, template_folder='../../templates/auth')

# Import routes after blueprint is created
from app.blueprints.auth import routes  # noqa: F401, E402
