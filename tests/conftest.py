"""Test configuration."""
import pytest
from app import create_app, db
from app.models.user import User
from config import Config


class TestConfig(Config):
    """Test configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    REDIS_URL = None  # Use in-memory for tests


@pytest.fixture(scope='module')
def app():
    """Create application for testing."""
    app = create_app('default')
    app.config.from_object(TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def init_database(app):
    """Initialize database with test data."""
    with app.app_context():
        # Create test user
        user = User(
            username='testuser',
            email='test@example.com',
            role='user',
            tier='free'
        )
        user.set_password('testpassword')
        db.session.add(user)
        
        # Create premium user
        premium_user = User(
            username='premiumuser',
            email='premium@example.com',
            role='user',
            tier='premium'
        )
        premium_user.set_password('testpassword')
        db.session.add(premium_user)
        
        # Create admin user
        admin_user = User(
            username='admin',
            email='admin@example.com',
            role='admin',
            tier='premium'
        )
        admin_user.set_password('adminpassword')
        db.session.add(admin_user)
        
        db.session.commit()
        
        yield db
        
        # Cleanup
        db.session.query(User).delete()
        db.session.commit()
