"""API blueprint."""
from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import routes after blueprint is created
from app.blueprints.api import routes  # noqa: F401, E402
