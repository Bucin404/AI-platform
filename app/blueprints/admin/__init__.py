"""Admin blueprint."""
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, template_folder='../../templates/admin')

# Import routes after blueprint is created
from app.blueprints.admin import routes  # noqa: F401, E402
