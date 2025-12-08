"""Chat blueprint."""
from flask import Blueprint

chat_bp = Blueprint('chat', __name__, template_folder='../../templates/chat')

# Import routes after blueprint is created
from app.blueprints.chat import routes  # noqa: F401, E402
