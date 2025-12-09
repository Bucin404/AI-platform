"""Test model service functionality."""
import pytest
from app.services.model_service import (
    detect_content_type,
    select_model_for_content,
    get_model_response,
    get_available_models
)


def test_detect_coding_content():
    """Test detection of coding-related content."""
    prompts = [
        "Write a Python function to sort a list",
        "Debug this JavaScript code",
        "How to implement a binary search algorithm",
        "What's wrong with my C++ program",
        "def my_function():"
    ]
    
    for prompt in prompts:
        content_type = detect_content_type(prompt)
        assert content_type == 'code', f"Failed for prompt: {prompt}"


def test_detect_file_content():
    """Test detection of file-related content."""
    prompts = [
        "Analyze this PDF document",
        "Process this large file",
        "Read this CSV file",
        "Extract text from PDF"
    ]
    
    for prompt in prompts:
        content_type = detect_content_type(prompt)
        assert content_type in ['pdf', 'file'], f"Failed for prompt: {prompt}"


def test_detect_image_content():
    """Test detection of image-related content."""
    prompts = [
        "Analyze this image",
        "What's in this photo",
        "Describe this picture",
        "Image recognition task"
    ]
    
    for prompt in prompts:
        content_type = detect_content_type(prompt)
        assert content_type == 'image', f"Failed for prompt: {prompt}"


def test_detect_video_content():
    """Test detection of video-related content."""
    prompts = [
        "Analyze this video",
        "Process this mp4 file",
        "What happens in this video"
    ]
    
    for prompt in prompts:
        content_type = detect_content_type(prompt)
        assert content_type == 'video', f"Failed for prompt: {prompt}"


def test_detect_general_content():
    """Test detection of general content."""
    prompts = [
        "What is the weather today?",
        "Tell me a joke",
        "Explain quantum physics",
        "How are you?"
    ]
    
    for prompt in prompts:
        content_type = detect_content_type(prompt)
        assert content_type == 'general', f"Failed for prompt: {prompt}"


def test_model_selection_for_coding():
    """Test that coding tasks select DeepSeek."""
    prompt = "Write a function to reverse a string in Python"
    model = select_model_for_content(prompt)
    assert model == 'deepseek'


def test_model_selection_for_files():
    """Test that file tasks select Llama."""
    prompt = "Analyze this PDF document"
    model = select_model_for_content(prompt)
    assert model == 'llama'


def test_model_selection_for_images():
    """Test that image tasks select Vicuna."""
    prompt = "Describe this image"
    model = select_model_for_content(prompt)
    assert model == 'vicuna'


def test_model_selection_for_general():
    """Test that general tasks select GPT4All."""
    prompt = "What is artificial intelligence?"
    model = select_model_for_content(prompt)
    assert model == 'gpt4all'


def test_manual_model_selection():
    """Test that manual model selection is respected."""
    prompt = "Any question"
    model = select_model_for_content(prompt, requested_model='llama')
    assert model == 'llama'


def test_get_model_response():
    """Test getting response from model."""
    response = get_model_response("Hello, AI!", "gpt4all")
    assert response is not None
    assert len(response) > 0
    assert isinstance(response, str)


def test_auto_model_response():
    """Test auto model selection in get_model_response."""
    # Coding task should use DeepSeek
    response = get_model_response("Write a Python function", "auto")
    assert 'deepseek' in response.lower() or 'code' in response.lower()


def test_get_available_models():
    """Test getting list of available models."""
    models = get_available_models()
    assert len(models) > 0
    
    model_ids = [m['id'] for m in models]
    assert 'auto' in model_ids
    assert 'deepseek' in model_ids
    assert 'gpt4all' in model_ids
    assert 'llama' in model_ids
    assert 'vicuna' in model_ids
    
    # Check model with use_case
    deepseek = next(m for m in models if m['id'] == 'deepseek')
    assert 'use_case' in deepseek
    assert 'Coding' in deepseek['use_case']
