"""Test model service functionality."""
import pytest
from unittest.mock import MagicMock, patch
from app.services.model_service import (
    detect_content_type,
    select_model_for_content,
    get_model_response,
    get_available_models,
    MistralAdapter,
    CodeLlamaAdapter,
    Llama3Adapter,
    HermesAdapter
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


def test_streaming_with_empty_chunks():
    """Test that streaming yields empty chunks and token counter increments."""
    # Create a mock adapter
    adapter = MistralAdapter()
    adapter._is_loaded = True
    
    # Simulate llama-cpp-python streaming format with empty chunks
    # Use side_effect to return a NEW generator each time
    def mock_stream_generator_factory(*args, **kwargs):
        # Only return generator if stream=True
        if kwargs.get('stream', False):
            def gen():
                yield {'choices': [{'text': ''}]}  # Empty chunk
                yield {'choices': [{'text': ''}]}  # Empty chunk
                yield {'choices': [{'text': 'Hello'}]}  # Real token
                yield {'choices': [{'text': ' '}]}  # Whitespace
                yield {'choices': [{'text': 'World'}]}  # Real token
                yield {'choices': [{'text': ''}]}  # Empty chunk
            return gen()
        else:
            return {'choices': [{'text': 'mock'}]}
    
    # Mock the llama model - use side_effect to get fresh generator
    mock_model = MagicMock()
    mock_model.side_effect = mock_stream_generator_factory
    adapter.model = mock_model
    
    # Generate streaming response
    generator = adapter.generate("test prompt", stream=True)
    
    # Collect all tokens including empty ones
    tokens = list(generator)
    
    # Verify that we got tokens (including empty ones)
    # Note: First token is "Testing... " from the adapter's test mechanism
    assert len(tokens) > 1, f"Should yield tokens even with empty chunks, got {len(tokens)}: {tokens}"
    
    # Verify the generator didn't skip empty chunks
    # Remove the test token to check the actual stream
    stream_tokens = tokens[1:]  # Skip "Testing... " 
    assert any(t == '' for t in stream_tokens), "Should include empty string tokens"
    assert any(t and t.strip() for t in stream_tokens), "Should include non-empty tokens"


def test_streaming_with_only_empty_chunks_triggers_fallback():
    """Test that streaming with only empty chunks triggers fallback."""
    # Create a mock adapter
    adapter = CodeLlamaAdapter()
    adapter._is_loaded = True
    
    def mock_empty_stream_generator_factory(*args, **kwargs):
        if kwargs.get('stream', False):
            def gen():
                for _ in range(5):
                    yield {'choices': [{'text': ''}]}
            return gen()
        else:
            return {'choices': [{'text': 'mock'}]}
    
    # Mock the llama model
    mock_model = MagicMock()
    mock_model.side_effect = mock_empty_stream_generator_factory
    adapter.model = mock_model
    
    # Generate streaming response
    generator = adapter.generate("test prompt", stream=True)
    
    # Collect all tokens
    tokens = list(generator)
    
    # Should have empty tokens + fallback tokens
    assert len(tokens) > 5, f"Should include fallback tokens when only empty chunks, got {len(tokens)}"
    
    # Check that fallback message is present
    full_response = ''.join(tokens)
    assert 'fallback' in full_response.lower() or 'model not loaded' in full_response.lower()


def test_streaming_token_count_increments():
    """Test that SSE token counter increments even with empty chunks."""
    # This test simulates the SSE route behavior
    adapter = Llama3Adapter()
    adapter._is_loaded = True
    
    def mock_mixed_stream_generator_factory(*args, **kwargs):
        if kwargs.get('stream', False):
            def gen():
                yield {'choices': [{'text': ''}]}  # Empty - should still count
                yield {'choices': [{'text': 'Token'}]}  # Real token
                yield {'choices': [{'text': ''}]}  # Empty - should still count
            return gen()
        else:
            return {'choices': [{'text': 'mock'}]}
    
    mock_model = MagicMock()
    mock_model.side_effect = mock_mixed_stream_generator_factory
    adapter.model = mock_model
    
    # Simulate SSE route counting
    generator = adapter.generate("test", stream=True)
    token_count = 0
    
    for token in generator:
        token_count += 1  # This is what the SSE route does
    
    # Should count all chunks, not just non-empty ones
    assert token_count > 0, "Token count should be greater than 0"
    # We expect at least 3 tokens (empty, real, empty)
    assert token_count >= 3, f"Expected at least 3 tokens, got {token_count}"


def test_hermes_streaming_with_whitespace():
    """Test that Hermes adapter yields whitespace chunks."""
    adapter = HermesAdapter()
    adapter._is_loaded = True
    
    def mock_whitespace_stream_generator_factory(*args, **kwargs):
        if kwargs.get('stream', False):
            def gen():
                yield {'choices': [{'text': 'Word'}]}
                yield {'choices': [{'text': ' '}]}  # Whitespace should be yielded
                yield {'choices': [{'text': 'Another'}]}
                yield {'choices': [{'text': '  '}]}  # Multiple spaces
            return gen()
        else:
            return {'choices': [{'text': 'mock'}]}
    
    mock_model = MagicMock()
    mock_model.side_effect = mock_whitespace_stream_generator_factory
    adapter.model = mock_model
    
    generator = adapter.generate("test", stream=True)
    tokens = list(generator)
    
    # Check whitespace tokens are present
    assert any(t.isspace() for t in tokens if t), "Should yield whitespace tokens"
    
    # Reconstruct and verify
    full_text = ''.join(tokens)
    assert 'Word' in full_text
    assert 'Another' in full_text
