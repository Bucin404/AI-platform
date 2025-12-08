"""Test authentication functionality."""
import pytest
from app.models.user import User
from app import db


def test_registration(client, app):
    """Test user registration."""
    response = client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'password2': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    with app.app_context():
        user = User.query.filter_by(email='newuser@example.com').first()
        assert user is not None
        assert user.username == 'newuser'


def test_login_logout(client, init_database):
    """Test user login and logout."""
    # Test login
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'testpassword',
        'remember_me': False
    }, follow_redirects=True)
    
    assert response.status_code == 200
    
    # Test logout
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200


def test_login_invalid_credentials(client, init_database):
    """Test login with invalid credentials."""
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'wrongpassword'
    })
    
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data or b'login' in response.data.lower()


def test_password_hashing(app):
    """Test password hashing."""
    with app.app_context():
        user = User(username='hashtest', email='hash@example.com')
        user.set_password('testpassword')
        
        assert user.password_hash != 'testpassword'
        assert user.check_password('testpassword')
        assert not user.check_password('wrongpassword')


def test_duplicate_registration(client, init_database):
    """Test registration with existing email."""
    response = client.post('/auth/register', data={
        'username': 'duplicate',
        'email': 'test@example.com',  # Already exists
        'password': 'password123',
        'password2': 'password123'
    })
    
    assert response.status_code == 200
    # Should show error about email already registered
