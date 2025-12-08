"""Test chat functionality."""
import pytest
from app.models.user import User, Message
from app import db
import json


def login_user(client, email='test@example.com', password='testpassword'):
    """Helper function to login user."""
    return client.post('/auth/login', data={
        'email': email,
        'password': password
    }, follow_redirects=True)


def test_chat_access_requires_login(client):
    """Test that chat page requires login."""
    response = client.get('/chat/')
    assert response.status_code == 302  # Redirect to login


def test_chat_page_access(client, init_database):
    """Test accessing chat page when logged in."""
    login_user(client)
    response = client.get('/chat/')
    assert response.status_code == 200


def test_send_message(client, init_database, app):
    """Test sending a chat message."""
    login_user(client)
    
    response = client.post('/chat/send',
        data=json.dumps({
            'message': 'Hello AI',
            'model': 'gpt4all'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'response' in data
    assert 'model' in data
    
    # Verify message was saved
    with app.app_context():
        user = User.query.filter_by(email='test@example.com').first()
        messages = Message.query.filter_by(user_id=user.id).all()
        assert len(messages) >= 2  # User message + AI response


def test_send_empty_message(client, init_database):
    """Test sending an empty message."""
    login_user(client)
    
    response = client.post('/chat/send',
        data=json.dumps({
            'message': '',
            'model': 'gpt4all'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 400


def test_get_chat_history(client, init_database, app):
    """Test retrieving chat history."""
    login_user(client)
    
    # Send a message first
    client.post('/chat/send',
        data=json.dumps({
            'message': 'Test message',
            'model': 'gpt4all'
        }),
        content_type='application/json'
    )
    
    # Get history
    response = client.get('/chat/history')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'messages' in data
    assert len(data['messages']) > 0


def test_model_selection(client, init_database):
    """Test getting available models."""
    login_user(client)
    
    response = client.get('/chat/models')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'models' in data
    assert len(data['models']) > 0
    
    # Check for specific models
    model_ids = [m['id'] for m in data['models']]
    assert 'deepseek' in model_ids
    assert 'gpt4all' in model_ids
    assert 'llama' in model_ids
    assert 'vicuna' in model_ids


def test_auto_model_selection_for_code(client, init_database):
    """Test that coding questions route to DeepSeek."""
    login_user(client)
    
    response = client.post('/chat/send',
        data=json.dumps({
            'message': 'Write a Python function to sort a list',
            'model': 'auto'
        }),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    # Should route to deepseek for coding
    assert 'deepseek' in data['model'].lower() or 'code' in data['response'].lower()
