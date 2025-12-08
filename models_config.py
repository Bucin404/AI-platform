"""
Model Download Configuration
Defines URLs and settings for downloading open-source AI models
"""

# Model download URLs and configurations
MODELS_CONFIG = {
    'deepseek-coder': {
        'name': 'DeepSeek Coder 6.7B',
        'description': 'Specialized for coding and programming tasks',
        'url': 'https://huggingface.co/TheBloke/deepseek-coder-6.7B-instruct-GGUF/resolve/main/deepseek-coder-6.7b-instruct.Q4_K_M.gguf',
        'filename': 'deepseek-coder-6.7b-instruct.Q4_K_M.gguf',
        'size': '4.1 GB',
        'required': True,
        'type': 'gguf',
        'use_case': 'code'
    },
    'llama-cpp': {
        'name': 'Llama 2 7B',
        'description': 'Optimized for document processing and general tasks',
        'url': 'https://huggingface.co/TheBloke/Llama-2-7B-GGUF/resolve/main/llama-2-7b.Q4_K_M.gguf',
        'filename': 'llama-2-7b.Q4_K_M.gguf',
        'size': '4.1 GB',
        'required': True,
        'type': 'gguf',
        'use_case': 'documents'
    },
    'gpt4all': {
        'name': 'GPT4All Falcon',
        'description': 'General purpose conversational AI',
        'url': 'https://gpt4all.io/models/gguf/gpt4all-falcon-newbpe-q4_0.gguf',
        'filename': 'gpt4all-falcon-newbpe-q4_0.gguf',
        'size': '3.9 GB',
        'required': True,
        'type': 'gguf',
        'use_case': 'general'
    },
    'vicuna': {
        'name': 'Vicuna 7B v1.5',
        'description': 'For conversational tasks and multimodal support',
        'url': 'https://huggingface.co/TheBloke/vicuna-7B-v1.5-GGUF/resolve/main/vicuna-7b-v1.5.Q4_K_M.gguf',
        'filename': 'vicuna-7b-v1.5.Q4_K_M.gguf',
        'size': '4.1 GB',
        'required': False,
        'type': 'gguf',
        'use_case': 'multimodal'
    }
}

# Alternative smaller models for resource-constrained environments
MODELS_CONFIG_LITE = {
    'deepseek-coder-lite': {
        'name': 'DeepSeek Coder 1.3B',
        'description': 'Lightweight version for coding tasks',
        'url': 'https://huggingface.co/TheBloke/deepseek-coder-1.3b-instruct-GGUF/resolve/main/deepseek-coder-1.3b-instruct.Q4_K_M.gguf',
        'filename': 'deepseek-coder-1.3b-instruct.Q4_K_M.gguf',
        'size': '0.9 GB',
        'required': True,
        'type': 'gguf',
        'use_case': 'code'
    },
    'tinyllama': {
        'name': 'TinyLlama 1.1B',
        'description': 'Lightweight model for general tasks',
        'url': 'https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf',
        'filename': 'tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf',
        'size': '0.7 GB',
        'required': True,
        'type': 'gguf',
        'use_case': 'general'
    }
}

# Model download settings
DOWNLOAD_SETTINGS = {
    'models_dir': './models',
    'chunk_size': 8192,  # 8KB chunks for download
    'timeout': 300,  # 5 minutes timeout per chunk
    'retry_attempts': 3,
    'verify_checksum': False,  # Set to True if checksums are provided
}
