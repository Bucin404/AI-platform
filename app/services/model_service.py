"""Model service for AI interactions."""
from abc import ABC, abstractmethod
import random
import re


class ModelAdapter(ABC):
    """Base class for model adapters."""
    
    @abstractmethod
    def generate(self, prompt, user=None):
        """Generate a response from the model."""
        pass
    
    @abstractmethod
    def get_name(self):
        """Get model name."""
        pass


class LlamaCppAdapter(ModelAdapter):
    """Adapter for llama.cpp models."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path
        # In production, initialize llama.cpp here
        # For now, this is a placeholder/mock
    
    def generate(self, prompt, user=None):
        """Generate response using llama.cpp - optimized for document processing."""
        # Mock implementation - replace with actual llama.cpp integration
        file_responses = [
            f"[Llama.cpp - Document Processing]\n\nAnalyzing document content: {prompt[:80]}...\n\nKey information extracted:\n- Document structure analysis\n- Content summarization\n- Key points identification\n\nNote: This is a mock response. Production version will process actual documents and large files.",
            f"[Llama.cpp File Processor]\n\nProcessing request: {prompt[:100]}...\n\nFor large files and documents, I can:\n- Extract and parse content\n- Summarize lengthy documents\n- Analyze structured data (CSV, JSON, etc.)\n\nPlaceholder response for development.",
            f"[Llama.cpp - Fast Document AI]\n\nDocument task: {prompt[:80]}...\n\nCapabilities:\n✓ PDF text extraction\n✓ Large file processing\n✓ Document summarization\n✓ Data analysis\n\nMock implementation. Real model will process actual files efficiently."
        ]
        return random.choice(file_responses)
    
    def get_name(self):
        return "llama.cpp"


class GPT4AllAdapter(ModelAdapter):
    """Adapter for GPT4All models."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path
        # In production, initialize GPT4All here
        # For now, this is a placeholder/mock
    
    def generate(self, prompt, user=None):
        """Generate response using GPT4All."""
        # Mock implementation - replace with actual GPT4All integration
        # Clean prompt from context markers
        clean_prompt = prompt.split("Assistant:")[-1].strip() if "Assistant:" in prompt else prompt
        
        responses = [
            f"I understand your question. Let me help you with that.\n\nBased on what you're asking, here's a comprehensive response that addresses your needs. The information I'm providing should give you a clear understanding of the topic.\n\nIf you need more details or have follow-up questions, feel free to ask!",
            f"Great question! I can help you with that.\n\nHere are the key insights:\n\n• This is an important topic that deserves careful consideration\n• There are multiple aspects to consider in your situation\n• I can provide guidance based on best practices\n\nLet me know if you'd like me to elaborate on any specific point!",
            f"I'll help you with that. Here's what you need to know:\n\nThe answer to your question involves several important factors. I've analyzed your request and can provide relevant information to help you understand this better.\n\nFeel free to ask follow-up questions if you need more clarification!"
        ]
        return random.choice(responses)
    
    def get_name(self):
        return "gpt4all"


class DeepSeekAdapter(ModelAdapter):
    """Adapter for DeepSeek models."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path
        # In production, initialize DeepSeek here
    
    def generate(self, prompt, user=None):
        """Generate response using DeepSeek - specialized for coding."""
        # Mock implementation - replace with actual DeepSeek integration
        coding_responses = [
            f"[DeepSeek Coder]\n\nAnalyzing your code request: {prompt[:80]}...\n\n```python\n# Here's a solution approach:\ndef example_function():\n    # Implementation details\n    pass\n```\n\nExplanation: This is a mock response. In production, DeepSeek will provide actual code analysis and solutions.",
            f"[DeepSeek Coder]\n\nI'll help you with this coding task.\n\nKey considerations:\n1. Code structure and best practices\n2. Error handling\n3. Performance optimization\n\n```\n// Sample implementation\n// {prompt[:60]}...\n```\n\nNote: This is a placeholder. Real DeepSeek model will provide detailed code assistance.",
            f"[DeepSeek Coder - Code Analysis]\n\nTask: {prompt[:100]}...\n\nRecommended approach:\n- Use appropriate design patterns\n- Follow language-specific conventions\n- Include proper error handling\n\nMock implementation provided. Production version will use actual DeepSeek Coder model."
        ]
        return random.choice(coding_responses)
    
    def get_name(self):
        return "deepseek"


class VicunaAdapter(ModelAdapter):
    """Adapter for Vicuna models."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path
        # In production, initialize Vicuna here
    
    def generate(self, prompt, user=None):
        """Generate response using Vicuna - specialized for multimodal content."""
        # Mock implementation - replace with actual Vicuna integration
        multimodal_responses = [
            f"[Vicuna - Multimodal Analysis]\n\nAnalyzing your content request: {prompt[:80]}...\n\nFor image/video content:\n- I can process visual information\n- Extract key features and descriptions\n- Provide detailed analysis\n\nNote: This is a mock response. Production version will process actual image/video data.",
            f"[Vicuna Vision Model]\n\nContent type: Image/Video processing\nQuery: {prompt[:100]}...\n\nIn production, I will:\n- Analyze visual content\n- Identify objects and scenes\n- Provide comprehensive descriptions\n\nPlaceholder response for development.",
            f"[Vicuna - Visual AI]\n\nTask: {prompt[:80]}...\n\nMultimodal capabilities:\n✓ Image recognition\n✓ Video analysis\n✓ Scene understanding\n✓ Content description\n\nMock implementation. Real model will process actual media files."
        ]
        return random.choice(multimodal_responses)
    
    def get_name(self):
        return "vicuna"


# Model registry
MODELS = {
    'llama': LlamaCppAdapter(),
    'gpt4all': GPT4AllAdapter(),
    'deepseek': DeepSeekAdapter(),
    'vicuna': VicunaAdapter()
}


def detect_content_type(prompt):
    """Detect content type from prompt to select appropriate model.
    
    Returns:
        str: Content type - 'code', 'file', 'pdf', 'image', 'video', 'general'
    """
    prompt_lower = prompt.lower()
    
    # Coding keywords
    coding_keywords = [
        'code', 'function', 'class', 'programming', 'debug', 'error',
        'python', 'javascript', 'java', 'c++', 'rust', 'go', 'php',
        'html', 'css', 'sql', 'algorithm', 'api', 'backend', 'frontend',
        'bug', 'syntax', 'compile', 'execute', 'script', 'package',
        'import', 'export', 'variable', 'loop', 'conditional', 'refactor',
        'optimize code', 'write code', 'fix code', 'review code',
        'implementation', 'coding', 'developer', 'program'
    ]
    
    # File processing keywords
    file_keywords = ['file', 'document', 'upload', 'large file', 'csv', 'json', 'xml', 'yaml']
    
    # PDF keywords
    pdf_keywords = ['pdf', 'document analysis', 'extract text', 'read pdf']
    
    # Image/photo keywords
    image_keywords = ['image', 'photo', 'picture', 'jpeg', 'png', 'analyze image', 'vision']
    
    # Video keywords
    video_keywords = ['video', 'mp4', 'avi', 'analyze video', 'video processing']
    
    # Check for coding content
    if any(keyword in prompt_lower for keyword in coding_keywords):
        return 'code'
    
    # Check for PDF content
    if any(keyword in prompt_lower for keyword in pdf_keywords):
        return 'pdf'
    
    # Check for image content
    if any(keyword in prompt_lower for keyword in image_keywords):
        return 'image'
    
    # Check for video content
    if any(keyword in prompt_lower for keyword in video_keywords):
        return 'video'
    
    # Check for file content
    if any(keyword in prompt_lower for keyword in file_keywords):
        return 'file'
    
    # Check for code blocks or patterns
    if '```' in prompt or re.search(r'def |class |function |import |const |var |let ', prompt):
        return 'code'
    
    return 'general'


def select_model_for_content(prompt, requested_model=None):
    """Select appropriate model based on content type.
    
    Args:
        prompt: User prompt/message
        requested_model: User-requested model (optional)
    
    Returns:
        str: Model name to use
    """
    from flask import current_app
    
    # If user specifically requested a model, use it
    if requested_model and requested_model in MODELS:
        return requested_model
    
    content_type = detect_content_type(prompt)
    
    # Route to appropriate model based on content type
    if content_type == 'code':
        # Use DeepSeek for coding tasks
        return 'deepseek'
    elif content_type in ['pdf', 'file']:
        # Use Llama for file/document processing
        return 'llama'
    elif content_type in ['image', 'video']:
        # Use Vicuna for multimodal content
        return 'vicuna'
    else:
        # Use configured default model for general chat
        try:
            default_model = current_app.config.get('DEFAULT_MODEL', 'gpt4all')
            return default_model if default_model in MODELS else 'gpt4all'
        except RuntimeError:
            # Outside app context, use gpt4all
            return 'gpt4all'


def get_model_response(prompt, model_name='auto', user=None, history=None):
    """Get response from specified model with conversation context.
    
    Args:
        prompt: User prompt/message
        model_name: Model to use ('auto' for automatic selection)
        user: User object
        history: List of previous messages for context (optional)
    
    Returns:
        str: AI response
    """
    from flask import current_app
    
    # Auto-select model based on content if requested
    if model_name == 'auto':
        model_name = select_model_for_content(prompt)
    elif model_name not in MODELS:
        # Fallback to configured default model if invalid model specified
        try:
            model_name = current_app.config.get('DEFAULT_MODEL', 'gpt4all')
            if model_name not in MODELS:
                model_name = 'gpt4all'
        except RuntimeError:
            model_name = 'gpt4all'
    
    model = MODELS[model_name]
    
    # Build context-aware prompt if history provided (internal use only)
    if history and len(history) > 0:
        # Build context string from conversation history
        context_parts = []
        for msg in history[-10:]:  # Last 10 messages for context
            role = "User" if msg['role'] == 'user' else "Assistant"
            context_parts.append(f"{role}: {msg['content'][:200]}")  # Limit each message to 200 chars
        
        context_parts.append(f"User: {prompt}")
        context_parts.append("Assistant:")
        
        full_prompt = "\n".join(context_parts)
    else:
        full_prompt = prompt
    
    # Generate response (context is hidden from user)
    response = model.generate(full_prompt, user)
    
    return response


def get_available_models():
    """Get list of available models."""
    return [
        {
            'id': 'auto',
            'name': 'Auto-Select',
            'description': 'Automatically selects the best model for your task',
            'recommended': True
        },
        {
            'id': 'deepseek',
            'name': 'DeepSeek Coder',
            'description': 'Specialized for coding, debugging, and programming tasks',
            'use_case': 'Coding & Development'
        },
        {
            'id': 'gpt4all',
            'name': 'GPT4All',
            'description': 'General purpose conversational AI for everyday tasks',
            'use_case': 'General Chat'
        },
        {
            'id': 'llama',
            'name': 'Llama.cpp',
            'description': 'Optimized for document processing and large files',
            'use_case': 'Files & Documents'
        },
        {
            'id': 'vicuna',
            'name': 'Vicuna',
            'description': 'Multimodal model for images, videos, and rich content',
            'use_case': 'Images & Videos'
        }
    ]
