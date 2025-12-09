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
        # Mock implementation - provides varied responses based on actual query content
        # Clean prompt from context markers
        clean_prompt = prompt.split("Assistant:")[-1].strip() if "Assistant:" in prompt else prompt
        
        # Extract actual user query
        user_query = clean_prompt.strip()
        query_lower = user_query.lower()
        
        # Provide contextual mock responses based on query content
        # Python/coding related
        if any(word in query_lower for word in ['python', 'code', 'function', 'programming', 'debug']):
            return f"I can help you with Python programming!\n\nRegarding your question about: \"{user_query[:80]}...\"\n\nHere's what you need to know:\n\n```python\n# Example code structure\ndef example_function():\n    # Your code here\n    pass\n```\n\nPython is a powerful language. Key concepts:\n- Functions and classes\n- Data structures (lists, dicts)\n- Error handling\n- Libraries and modules\n\nWould you like more specific guidance?"
        
        # General how-to questions
        elif 'how' in query_lower or 'cara' in query_lower:
            return f"Let me explain how to do this:\n\n**Your Question:** {user_query[:100]}\n\n**Step-by-Step Guide:**\n\n1. **First Step** - Understand the fundamentals\n2. **Second Step** - Apply the concepts\n3. **Third Step** - Practice and refine\n\n**Important Points:**\n- Start with basics\n- Build progressively\n- Test thoroughly\n\nNeed more details on any specific step?"
        
        # What questions
        elif 'what' in query_lower or 'apa' in query_lower:
            return f"**Understanding:** {user_query[:80]}\n\n**Definition:**\nBased on your question, this concept involves several key aspects that work together to achieve specific goals.\n\n**Key Characteristics:**\n- Primary feature: Core functionality\n- Secondary feature: Supporting capabilities\n- Applications: Real-world uses\n\n**Common Uses:**\nThis is typically used in situations where you need efficient, reliable solutions.\n\n**Want to learn more about specific aspects?**"
        
        # Why questions
        elif 'why' in query_lower or 'mengapa' in query_lower or 'kenapa' in query_lower:
            return f"**Why?** Great question!\n\nRegarding: \"{user_query[:80]}\"\n\n**Reason 1: Fundamental Principle**\nThis happens because of underlying mechanisms that govern how things work.\n\n**Reason 2: Practical Considerations**\nFrom a practical standpoint, this approach offers several advantages.\n\n**Reason 3: Historical Context**\nThis has evolved over time based on experience and best practices.\n\n**In Summary:**\nThe key is understanding the relationship between cause and effect.\n\nDoes this answer your question?"
        
        # General conversation
        else:
            responses = [
                f"Thanks for your question: \"{user_query[:80]}\"\n\nHere's my response:\n\nThis is an interesting topic that many people ask about. Let me break it down:\n\n**Main Points:**\n- Key aspect 1: Important consideration\n- Key aspect 2: Related factor\n- Key aspect 3: Practical application\n\n**Recommendation:**\nBased on your question, I'd suggest focusing on understanding the fundamentals first, then building on that knowledge.\n\nWhat specific aspect would you like to explore further?",
                
                f"I understand you're asking about:\n\"{user_query[:80]}\"\n\nHere's what I can tell you:\n\n**Context:**\nThis topic is relevant in many situations where understanding is important.\n\n**Key Information:**\n• Point 1: Core concept\n• Point 2: Supporting details  \n• Point 3: Practical insights\n\n**Next Steps:**\nConsider how this applies to your specific situation.\n\nNeed clarification on anything?",
                
                f"**Your Query:** {user_query[:80]}\n\n**My Response:**\n\nLet me address this comprehensively:\n\n1. **Background:** Understanding the context is crucial\n2. **Analysis:** Breaking down the components\n3. **Application:** How to use this knowledge\n\n**Practical Tips:**\n- Start with clear goals\n- Take systematic approach\n- Verify results\n\nShall I elaborate on any particular point?"
            ]
            import random
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
