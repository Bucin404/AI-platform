"""Model service for AI interactions with language detection and unique responses."""
from abc import ABC, abstractmethod
import random
import re
import hashlib
from pathlib import Path

# AUTO_INTEGRATED: This file has been automatically integrated with downloaded models
try:
    from llama_cpp import Llama
    LLAMA_CPP_AVAILABLE = True
except ImportError:
    LLAMA_CPP_AVAILABLE = False
    print("Warning: llama-cpp-python not available, using mock adapters")


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
    
    @abstractmethod
    def is_loaded(self):
        """Check if model is loaded."""
        pass


class LlamaCppAdapter(ModelAdapter):
    """Adapter for llama.cpp models - OPTIMIZED FOR MAXIMUM SPEED."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or './models/llama-2-7b.Q4_K_M.gguf'
        self.model = None
        self._is_loaded = False
        
        if LLAMA_CPP_AVAILABLE and Path(self.model_path).exists():
            try:
                print(f"⚡ Loading Llama model with SPEED OPTIMIZATIONS from {self.model_path}...")
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=2048,  # Reduced from 4096 for speed
                    n_threads=8,  # Increased from 4 for parallel processing
                    n_batch=512,  # Larger batch for faster processing
                    n_gpu_layers=0,  # Set to 35+ if GPU available
                    use_mlock=True,  # Lock memory for faster access
                    use_mmap=True,  # Memory mapping for speed
                    low_vram=False,  # Optimize for speed, not memory
                    verbose=False
                )
                self._is_loaded = True
                print(f"✅ Llama model loaded with SPEED OPTIMIZATIONS")
            except Exception as e:
                print(f"Warning: Could not load Llama model: {e}")
                self._is_loaded = False
    
    def is_loaded(self):
        return self._is_loaded
    
    def generate(self, prompt, user=None):
        """Generate response using llama.cpp - SPEED OPTIMIZED."""
        if self._is_loaded and self.model:
            try:
                response = self.model(
                    prompt,
                    max_tokens=256,  # Reduced from 512 for faster response
                    temperature=0.8,  # Slightly higher for faster sampling
                    top_p=0.9,  # Reduced from 0.95 for speed
                    top_k=40,  # Added for faster sampling
                    repeat_penalty=1.1,  # Prevent repetition
                    stop=["User:", "\n\nUser:", "\n\nQuestion:"],
                    echo=False,
                    stream=False  # No streaming for instant response
                )
                return response['choices'][0]['text'].strip()
            except Exception as e:
                print(f"Error generating response: {e}")
                return self._mock_response(prompt)
        else:
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt):
        """Fallback mock response."""
        return f"I can help you with document processing and general tasks. (Model not loaded - using fallback)"
    
    def get_name(self):
        return "llama.cpp"


class GPT4AllAdapter(ModelAdapter):
    """Adapter for GPT4All models - OPTIMIZED FOR MAXIMUM SPEED."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or './models/gpt4all-falcon-newbpe-q4_0.gguf'
        self.model = None
        self._is_loaded = False
        
        if LLAMA_CPP_AVAILABLE and Path(self.model_path).exists():
            try:
                print(f"⚡ Loading GPT4All model with SPEED OPTIMIZATIONS from {self.model_path}...")
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=1024,  # Reduced from 2048 for speed
                    n_threads=8,  # Increased for parallel processing
                    n_batch=512,  # Larger batch size
                    n_gpu_layers=0,  # Set to 35+ if GPU available
                    use_mlock=True,  # Lock memory
                    use_mmap=True,  # Memory mapping
                    low_vram=False,  # Optimize for speed
                    verbose=False
                )
                self._is_loaded = True
                print(f"✅ GPT4All model loaded with SPEED OPTIMIZATIONS")
            except Exception as e:
                print(f"Warning: Could not load GPT4All model: {e}")
                self._is_loaded = False
    
    def is_loaded(self):
        return self._is_loaded
    
    def generate(self, prompt, user=None):
        """Generate response using GPT4All - SPEED OPTIMIZED."""
        if self._is_loaded and self.model:
            try:
                response = self.model(
                    prompt,
                    max_tokens=200,  # Reduced from 512 for faster response
                    temperature=0.8,  # Higher for faster sampling
                    top_p=0.9,  # Reduced for speed
                    top_k=40,  # Faster sampling
                    repeat_penalty=1.1,
                    stop=["User:", "\n\nUser:"],
                    echo=False,
                    stream=False
                )
                return response['choices'][0]['text'].strip()
            except Exception as e:
                print(f"Error generating response: {e}")
                return self._mock_response(prompt)
        else:
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt):
        """Fallback mock response."""
        return f"I'm here to help you with your questions. (Model not loaded - using fallback)"
    
    def get_name(self):
        return "gpt4all"


class DeepSeekAdapter(ModelAdapter):
    """Adapter for DeepSeek models - OPTIMIZED FOR CODING SPEED."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or './models/deepseek-coder-6.7b-instruct.Q4_K_M.gguf'
        self.model = None
        self._is_loaded = False
        
        if LLAMA_CPP_AVAILABLE and Path(self.model_path).exists():
            try:
                print(f"⚡ Loading DeepSeek model with SPEED OPTIMIZATIONS from {self.model_path}...")
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=2048,  # Reduced from 4096 for speed
                    n_threads=8,  # Increased for parallel processing
                    n_batch=512,  # Larger batch
                    n_gpu_layers=0,  # Set to 35+ if GPU available
                    use_mlock=True,
                    use_mmap=True,
                    low_vram=False,
                    verbose=False
                )
                self._is_loaded = True
                print(f"✅ DeepSeek model loaded with SPEED OPTIMIZATIONS")
            except Exception as e:
                print(f"Warning: Could not load DeepSeek model: {e}")
                self._is_loaded = False
    
    def is_loaded(self):
        return self._is_loaded
    
    def generate(self, prompt, user=None):
        """Generate response using DeepSeek - SPEED OPTIMIZED."""
        if self._is_loaded and self.model:
            try:
                # DeepSeek uses a specific prompt format for coding
                formatted_prompt = f"### Instruction:\n{prompt}\n\n### Response:\n"
                response = self.model(
                    formatted_prompt,
                    max_tokens=512,  # Reduced from 1024 for speed
                    temperature=0.3,  # Slightly higher for faster sampling while keeping precision
                    top_p=0.9,  # Reduced for speed
                    top_k=40,
                    repeat_penalty=1.1,
                    stop=["###", "\n\n\n"],
                    echo=False,
                    stream=False
                )
                return response['choices'][0]['text'].strip()
            except Exception as e:
                print(f"Error generating response: {e}")
                return self._mock_response(prompt)
        else:
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt):
        """Fallback mock response."""
        return f"I can help you with coding and programming tasks. (Model not loaded - using fallback)\n\n```python\n# Example code structure\ndef example():\n    pass\n```"
    
    def get_name(self):
        return "deepseek"


class VicunaAdapter(ModelAdapter):
    """Adapter for Vicuna models - OPTIMIZED FOR CONVERSATIONAL SPEED."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or './models/vicuna-7b-v1.5.Q4_K_M.gguf'
        self.model = None
        self._is_loaded = False
        
        if LLAMA_CPP_AVAILABLE and Path(self.model_path).exists():
            try:
                print(f"⚡ Loading Vicuna model with SPEED OPTIMIZATIONS from {self.model_path}...")
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=1024,  # Reduced from 2048 for speed
                    n_threads=8,  # Increased for parallel processing
                    n_batch=512,  # Larger batch
                    n_gpu_layers=0,  # Set to 35+ if GPU available
                    use_mlock=True,
                    use_mmap=True,
                    low_vram=False,
                    verbose=False
                )
                self._is_loaded = True
                print(f"✅ Vicuna model loaded with SPEED OPTIMIZATIONS")
            except Exception as e:
                print(f"Warning: Could not load Vicuna model: {e}")
                self._is_loaded = False
    
    def is_loaded(self):
        return self._is_loaded
    
    def generate(self, prompt, user=None):
        """Generate response using Vicuna - SPEED OPTIMIZED."""
        if self._is_loaded and self.model:
            try:
                response = self.model(
                    prompt,
                    max_tokens=256,  # Reduced from 512 for speed
                    temperature=0.8,  # Higher for faster sampling
                    top_p=0.9,  # Reduced for speed
                    top_k=40,
                    repeat_penalty=1.1,
                    stop=["USER:", "ASSISTANT:"],
                    echo=False,
                    stream=False
                )
                return response['choices'][0]['text'].strip()
            except Exception as e:
                print(f"Error generating response: {e}")
                return self._mock_response(prompt)
        else:
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt):
        """Fallback mock response."""
        return f"I can help with conversational tasks and multimodal content. (Model not loaded - using fallback)"
    
    def get_name(self):
        return "vicuna"


# NEW BEST MODELS - 2024 Recommendations

class MistralAdapter(ModelAdapter):
    """Adapter for Mistral-7B-Instruct-v0.3 - BEST GENERAL CHAT MODEL."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or './models/Mistral-7B-Instruct-v0.3-Q4_K_M.gguf'
        self.model = None
        self._is_loaded = False
        
        if LLAMA_CPP_AVAILABLE and Path(self.model_path).exists():
            try:
                print(f"⚡ Loading Mistral-7B with SPEED OPTIMIZATIONS from {self.model_path}...")
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=2048,  # Optimal for general chat
                    n_threads=8,  # Maximum parallel processing
                    n_batch=512,  # Large batch for speed
                    n_gpu_layers=0,  # Set to 35+ if GPU available
                    use_mlock=True,  # Lock memory for speed
                    use_mmap=True,  # Memory mapping
                    low_vram=False,
                    verbose=False
                )
                self._is_loaded = True
                print(f"✅ Mistral-7B loaded - BEST general chat quality!")
            except Exception as e:
                print(f"Warning: Could not load Mistral model: {e}")
                self._is_loaded = False
    
    def is_loaded(self):
        return self._is_loaded
    
    def generate(self, prompt, user=None, stream=False):
        """Generate response using Mistral - HIGHEST QUALITY with optional streaming."""
        if self._is_loaded and self.model:
            try:
                # SIMPLIFIED: Use direct prompt first, test if [INST] format is the issue
                formatted_prompt = prompt.strip()
                
                print(f"🎯 Mistral RAW prompt: {repr(prompt[:200])}")
                print(f"🎯 Mistral formatted prompt: {repr(formatted_prompt[:200])}")
                
                response = self.model(
                    formatted_prompt,
                    max_tokens=512,  # Increased for better responses
                    temperature=0.7,  # Standard temperature
                    top_p=0.95,  # Higher for more diverse output
                    top_k=50,  # Increased for better generation
                    repeat_penalty=1.05,  # Lower to allow more natural speech
                    stop=[],  # NO STOP TOKENS - let model decide when to stop
                    echo=False,
                    stream=stream  # Enable streaming if requested
                )
                
                if stream:
                    # Return generator for streaming
                    def streaming_generator():
                        print(f"🔄 Mistral streaming started...")
                        print(f"📁 Model file: {self.model_path}")
                        
                        # IMMEDIATE TEST: Yield test token to verify streaming works
                        print(f"🧪 Sending test token...")
                        yield "Testing... "
                        
                        token_count = 0
                        empty_count = 0
                        max_empty = 10  # After 10 empty iterations, use fallback
                        yielded_any = False
                        
                        try:
                            for chunk in response:
                                # Handle llama-cpp-python streaming format
                                # Streaming may return tokens directly or in dict format
                                if isinstance(chunk, str):
                                    token = chunk
                                elif isinstance(chunk, dict):
                                    token = chunk.get('choices', [{}])[0].get('text', '')
                                else:
                                    token = str(chunk)
                                
                                token_count += 1
                                
                                if token:
                                    print(f"  📦 Token {token_count}: {repr(token[:50])}")
                                    empty_count = 0  # Reset empty counter
                                    yielded_any = True
                                    yield token
                                else:
                                    empty_count += 1
                                    print(f"  ⚠️  Empty chunk {empty_count}/{max_empty}")
                                    
                                    # If too many empty chunks, switch to fallback
                                    if empty_count >= max_empty:
                                        print(f"  ⚠️  Too many empty chunks! Using fallback response...")
                                        fallback = self._mock_response(prompt)
                                        words = fallback.split()
                                        print(f"  📝 Starting fallback: {len(words)} words")
                                        for i, word in enumerate(words, 1):
                                            print(f"  📝 Fallback word {i}: {word}")
                                            yield word + " "
                                        print(f"  ✅ Fallback complete: {len(words)} words")
                                        return
                        except StopIteration:
                            pass
                        
                        # Check if we yielded anything at all (besides test token)
                        if not yielded_any:
                            print(f"  ⚠️  Generator completed with 0 tokens! Using fallback...")
                            fallback = self._mock_response(prompt)
                            words = fallback.split()
                            print(f"  📝 Starting fallback: {len(words)} words")
                            for i, word in enumerate(words, 1):
                                print(f"  📝 Fallback word {i}: {word}")
                                yield word + " "
                            print(f"  ✅ Fallback complete: {len(words)} words")
                        else:
                            print(f"  ✅ Mistral streaming done: {token_count} real tokens")
                    
                    return streaming_generator()
                else:
                    return response['choices'][0]['text'].strip()
            except Exception as e:
                print(f"❌ Mistral error: {e}")
                import traceback
                traceback.print_exc()
                if stream:
                    yield self._mock_response(prompt)
                else:
                    return self._mock_response(prompt)
        else:
            print(f"⚠️  Mistral model not loaded, using fallback")
            if stream:
                yield self._mock_response(prompt)
            else:
                return self._mock_response(prompt)
    
    def _mock_response(self, prompt):
        """Fallback mock response."""
        return f"I can help with general conversation, Q&A, and various tasks. (Mistral model not loaded - using fallback)"
    
    def get_name(self):
        return "mistral"


class CodeLlamaAdapter(ModelAdapter):
    """Adapter for CodeLlama-13B-Instruct - BEST CODING MODEL."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or './models/codellama-13b-instruct.Q4_K_M.gguf'
        self.model = None
        self._is_loaded = False
        
        if LLAMA_CPP_AVAILABLE and Path(self.model_path).exists():
            try:
                print(f"⚡ Loading CodeLlama-13B with SPEED OPTIMIZATIONS from {self.model_path}...")
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=2048,  # Good for code context
                    n_threads=8,  # Maximum parallel processing
                    n_batch=512,  # Large batch for speed
                    n_gpu_layers=0,  # Set to 35+ if GPU available
                    use_mlock=True,
                    use_mmap=True,
                    low_vram=False,
                    verbose=False
                )
                self._is_loaded = True
                print(f"✅ CodeLlama-13B loaded - BEST coding quality!")
            except Exception as e:
                print(f"Warning: Could not load CodeLlama model: {e}")
                self._is_loaded = False
    
    def is_loaded(self):
        return self._is_loaded
    
    def generate(self, prompt, user=None, stream=False):
        """Generate response using CodeLlama - PROFESSIONAL CODE QUALITY with optional streaming."""
        if self._is_loaded and self.model:
            try:
                response = self.model(
                    prompt,
                    max_tokens=512,  # Longer for code examples
                    temperature=0.3,  # Lower for precise code
                    top_p=0.9,
                    top_k=40,
                    repeat_penalty=1.1,
                    stop=["###", "\n\n\n", "User:"],
                    echo=False,
                    stream=stream  # Enable streaming if requested
                )
                
                if stream:
                    # Return generator for streaming with fallback protection
                    def streaming_generator():
                        print(f"🔄 CodeLlama streaming started...")
                        yielded_any = False
                        
                        try:
                            for chunk in response:
                                # Handle llama-cpp-python streaming format
                                if isinstance(chunk, str):
                                    token = chunk
                                elif isinstance(chunk, dict):
                                    token = chunk.get('choices', [{}])[0].get('text', '')
                                else:
                                    token = str(chunk)
                                    
                                if token:
                                    yielded_any = True
                                    yield token
                        except StopIteration:
                            pass
                        
                        # Fallback if no tokens yielded
                        if not yielded_any:
                            print(f"  ⚠️  CodeLlama: 0 tokens! Using fallback...")
                            fallback = self._mock_response(prompt)
                            for word in fallback.split():
                                yield word + " "
                            print(f"  ✅ CodeLlama fallback complete")
                        else:
                            print(f"  ✅ CodeLlama streaming done")
                    
                    return streaming_generator()
                else:
                    return response['choices'][0]['text'].strip()
            except Exception as e:
                print(f"Error generating response: {e}")
                if stream:
                    yield self._mock_response(prompt)
                else:
                    return self._mock_response(prompt)
        else:
            if stream:
                yield self._mock_response(prompt)
            else:
                return self._mock_response(prompt)
    
    def _mock_response(self, prompt):
        """Fallback mock response."""
        return f"I can help with code generation, debugging, and explanation. (CodeLlama model not loaded - using fallback)\n\n```python\n# Example code\ndef example():\n    pass\n```"
    
    def get_name(self):
        return "codellama"


class Llama3Adapter(ModelAdapter):
    """Adapter for Llama-3-8B-Instruct - META'S LATEST MODEL."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or './models/Meta-Llama-3-8B-Instruct-Q4_K_M.gguf'
        self.model = None
        self._is_loaded = False
        
        if LLAMA_CPP_AVAILABLE and Path(self.model_path).exists():
            try:
                print(f"⚡ Loading Llama-3-8B with SPEED OPTIMIZATIONS from {self.model_path}...")
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=2048,  # Optimal for documents
                    n_threads=8,  # Maximum parallel processing
                    n_batch=512,  # Large batch for speed
                    n_gpu_layers=0,  # Set to 35+ if GPU available
                    use_mlock=True,
                    use_mmap=True,
                    low_vram=False,
                    verbose=False
                )
                self._is_loaded = True
                print(f"✅ Llama-3-8B loaded - Meta's latest model!")
            except Exception as e:
                print(f"Warning: Could not load Llama-3 model: {e}")
                self._is_loaded = False
    
    def is_loaded(self):
        return self._is_loaded
    
    def generate(self, prompt, user=None, stream=False):
        """Generate response using Llama-3 - META'S BEST with optional streaming."""
        if self._is_loaded and self.model:
            try:
                response = self.model(
                    prompt,
                    max_tokens=300,  # Good length for documents
                    temperature=0.7,
                    top_p=0.9,
                    top_k=40,
                    repeat_penalty=1.1,
                    stop=["<|eot_id|>", "<|start_header_id|>", "User:"],
                    echo=False,
                    stream=stream  # Enable streaming if requested
                )
                
                if stream:
                    # Return generator for streaming with fallback protection
                    def streaming_generator():
                        print(f"🔄 Llama3 streaming started...")
                        yielded_any = False
                        
                        try:
                            for chunk in response:
                                # Handle llama-cpp-python streaming format
                                if isinstance(chunk, str):
                                    token = chunk
                                elif isinstance(chunk, dict):
                                    token = chunk.get('choices', [{}])[0].get('text', '')
                                else:
                                    token = str(chunk)
                                    
                                if token:
                                    yielded_any = True
                                    yield token
                        except StopIteration:
                            pass
                        
                        # Fallback if no tokens yielded
                        if not yielded_any:
                            print(f"  ⚠️  Llama3: 0 tokens! Using fallback...")
                            fallback = self._mock_response(prompt)
                            for word in fallback.split():
                                yield word + " "
                            print(f"  ✅ Llama3 fallback complete")
                        else:
                            print(f"  ✅ Llama3 streaming done")
                    
                    return streaming_generator()
                else:
                    return response['choices'][0]['text'].strip()
            except Exception as e:
                print(f"Error generating response: {e}")
                if stream:
                    yield self._mock_response(prompt)
                else:
                    return self._mock_response(prompt)
        else:
            if stream:
                yield self._mock_response(prompt)
            else:
                return self._mock_response(prompt)
    
    def _mock_response(self, prompt):
        """Fallback mock response."""
        return f"I can help with document processing, analysis, and general tasks. (Llama-3 model not loaded - using fallback)"
    
    def get_name(self):
        return "llama3"


class HermesAdapter(ModelAdapter):
    """Adapter for OpenHermes-2.5-Mistral - BEST CREATIVE MODEL."""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or './models/openhermes-2.5-mistral-7b.Q4_K_M.gguf'
        self.model = None
        self._is_loaded = False
        
        if LLAMA_CPP_AVAILABLE and Path(self.model_path).exists():
            try:
                print(f"⚡ Loading OpenHermes-2.5 with SPEED OPTIMIZATIONS from {self.model_path}...")
                self.model = Llama(
                    model_path=self.model_path,
                    n_ctx=2048,  # Good for conversations
                    n_threads=8,  # Maximum parallel processing
                    n_batch=512,  # Large batch for speed
                    n_gpu_layers=0,  # Set to 35+ if GPU available
                    use_mlock=True,
                    use_mmap=True,
                    low_vram=False,
                    verbose=False
                )
                self._is_loaded = True
                print(f"✅ OpenHermes-2.5 loaded - BEST creative quality!")
            except Exception as e:
                print(f"Warning: Could not load OpenHermes model: {e}")
                self._is_loaded = False
    
    def is_loaded(self):
        return self._is_loaded
    
    def generate(self, prompt, user=None, stream=False):
        """Generate response using OpenHermes - CREATIVE & ENGAGING with optional streaming."""
        if self._is_loaded and self.model:
            try:
                response = self.model(
                    prompt,
                    max_tokens=350,  # Longer for creative responses
                    temperature=0.8,  # Higher for creativity
                    top_p=0.9,
                    top_k=40,
                    repeat_penalty=1.1,
                    stop=["<|im_end|>", "User:", "\n\nUser:"],
                    echo=False,
                    stream=stream  # Enable streaming if requested
                )
                
                if stream:
                    # Return generator for streaming with fallback protection
                    def streaming_generator():
                        print(f"🔄 Hermes streaming started...")
                        yielded_any = False
                        
                        try:
                            for chunk in response:
                                # Handle llama-cpp-python streaming format
                                if isinstance(chunk, str):
                                    token = chunk
                                elif isinstance(chunk, dict):
                                    token = chunk.get('choices', [{}])[0].get('text', '')
                                else:
                                    token = str(chunk)
                                    
                                if token:
                                    yielded_any = True
                                    yield token
                        except StopIteration:
                            pass
                        
                        # Fallback if no tokens yielded
                        if not yielded_any:
                            print(f"  ⚠️  Hermes: 0 tokens! Using fallback...")
                            fallback = self._mock_response(prompt)
                            for word in fallback.split():
                                yield word + " "
                            print(f"  ✅ Hermes fallback complete")
                        else:
                            print(f"  ✅ Hermes streaming done")
                    
                    return streaming_generator()
                else:
                    return response['choices'][0]['text'].strip()
            except Exception as e:
                print(f"Error generating response: {e}")
                if stream:
                    yield self._mock_response(prompt)
                else:
                    return self._mock_response(prompt)
        else:
            if stream:
                yield self._mock_response(prompt)
            else:
                return self._mock_response(prompt)
    
    def _mock_response(self, prompt):
        """Fallback mock response."""
        return f"I can help with creative writing, brainstorming, and engaging conversations. (OpenHermes model not loaded - using fallback)"
    
    def get_name(self):
        return "hermes"


# Initialize models - NEW BEST MODELS ONLY (2024)
# Create single instances of each model (load only once)
mistral_model = MistralAdapter()
codellama_model = CodeLlamaAdapter()
llama3_model = Llama3Adapter()
hermes_model = HermesAdapter()

MODELS = {
    # New best models (2024) - Primary names
    'mistral': mistral_model,
    'codellama': codellama_model,
    'llama3': llama3_model,
    'hermes': hermes_model,
    # Aliases for backwards compatibility (use same instances - no duplication)
    'llama': llama3_model,  # Route old llama to llama3
    'gpt4all': mistral_model,  # Route old gpt4all to mistral
    'deepseek': codellama_model,  # Route old deepseek to codellama
    'vicuna': hermes_model  # Route old vicuna to hermes
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


def detect_language(text):
    """Detect language from user input (Indonesian vs English).
    
    Args:
        text: User input text
    
    Returns:
        str: 'id' for Indonesian, 'en' for English
    """
    text_lower = text.lower()
    
    # Indonesian indicators
    id_indicators = [
        'saya', 'anda', 'dengan', 'untuk', 'ini', 'itu', 'yang', 'adalah', 
        'dari', 'di', 'ke', 'pada', 'akan', 'telah', 'sudah', 'dapat',
        'bagaimana', 'mengapa', 'kapan', 'dimana', 'apa', 'siapa',
        'jelaskan', 'tolong', 'bantu', 'terima kasih', 'maaf',
        'bisakah', 'dapatkah', 'maukah', 'bisa', 'tidak', 'ya'
    ]
    
    # English indicators
    en_indicators = [
        'the', 'and', 'for', 'this', 'that', 'with', 'from', 'is', 'are',
        'have', 'has', 'had', 'can', 'will', 'would', 'should', 'could',
        'what', 'where', 'when', 'why', 'how', 'who', 'which',
        'please', 'help', 'thank', 'thanks', 'sorry', 'yes', 'no'
    ]
    
    # Count indicators
    id_count = sum(1 for word in id_indicators if word in text_lower)
    en_count = sum(1 for word in en_indicators if word in text_lower)
    
    # Return detected language
    return 'id' if id_count > en_count else 'en'


def generate_unique_response_id(prompt):
    """Generate unique ID for prompt to ensure different responses.
    
    Args:
        prompt: User prompt
    
    Returns:
        int: Hash value for variation selection
    """
    # Create hash from prompt
    hash_object = hashlib.md5(prompt.encode())
    hash_hex = hash_object.hexdigest()
    # Convert to integer for modulo operation
    return int(hash_hex, 16)
    
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
    """Select appropriate model based on content type - UPDATED FOR NEW MODELS.
    
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
    
    # Route to NEW BEST MODELS based on content type
    if content_type == 'code':
        return 'codellama'  # NEW: CodeLlama-13B is best for coding
    elif content_type in ['pdf', 'file']:
        return 'llama3'  # NEW: Llama-3 is best for documents
    elif content_type in ['image', 'video']:
        return 'hermes'  # NEW: OpenHermes for creative/multimodal
    else:
        try:
            default_model = current_app.config.get('DEFAULT_MODEL', 'mistral')
            return default_model if default_model in MODELS else 'mistral'  # NEW: Mistral is best for general
        except RuntimeError:
            return 'mistral'  # NEW: Default to Mistral


def generate_fallback_response(prompt, language='en', variation=0):
    """Generate language-appropriate fallback response with unique variations.
    
    Args:
        prompt: User prompt
        language: 'id' or 'en'
        variation: Variation index (0-4) for uniqueness
    
    Returns:
        str: Unique, language-appropriate response
    """
    prompt_lower = prompt.lower()
    
    # Detect question type
    is_how = any(word in prompt_lower for word in ['how', 'bagaimana', 'cara'])
    is_what = any(word in prompt_lower for word in ['what', 'apa itu', 'apa yang', 'apakah'])
    is_why = any(word in prompt_lower for word in ['why', 'mengapa', 'kenapa'])
    is_code = any(word in prompt_lower for word in ['code', 'coding', 'program', 'function', 'kode', 'fungsi'])
    
    # Indonesian responses
    if language == 'id':
        if is_code:
            return f"""Saya dapat membantu Anda dengan pemrograman!

```python
# Contoh struktur kode
def contoh_fungsi():
    # Kode Anda di sini
    hasil = "Halo Dunia"
    return hasil
```

**Konsep Penting:**
- Variabel dan tipe data
- Struktur kontrol (if/else, loop)
- Fungsi dan class
- Error handling

Apakah ada yang ingin Anda pelajari lebih lanjut?"""
        
        elif is_how:
            templates_id = [
                f"""Mari saya jelaskan cara melakukannya:

**Panduan Langkah demi Langkah:**

1. **Langkah Pertama** - Pahami konsep dasarnya
2. **Langkah Kedua** - Terapkan prinsip-prinsipnya
3. **Langkah Ketiga** - Latihan dan penyempurnaan

Apakah Anda butuh penjelasan lebih detail untuk bagian tertentu?""",
                
                f"""Saya akan memandu Anda melalui proses ini:

**Tahapan Pelaksanaan:**

• **Persiapan Awal** - Kumpulkan informasi yang diperlukan
• **Implementasi** - Jalankan langkah-langkah utama
• **Evaluasi** - Periksa hasil dan optimalkan

Silakan beri tahu saya jika ada bagian yang perlu dijelaskan lebih detail!""",
                
                f"""Berikut cara efektif untuk melakukannya:

**Metode yang Disarankan:**

1. Mulai dengan fondasi yang kuat
2. Bangun secara bertahap
3. Test dan validasi hasilnya
4. Iterasi untuk perbaikan

Apakah ini menjawab pertanyaan Anda?"""
            ]
            return templates_id[variation % len(templates_id)]
        
        elif is_what:
            templates_id = [
                f"""**Pemahaman:** {prompt[:50]}...

**Definisi:**
Berdasarkan pertanyaan Anda, konsep ini melibatkan beberapa aspek penting.

**Karakteristik Utama:**
- Fitur utama: Fungsi inti dari topik ini
- Fitur pendukung: Kemampuan tambahan yang mendukung
- Aplikasi praktis: Penggunaan dalam kehidupan nyata

Apakah Anda ingin penjelasan lebih mendalam?""",
                
                f"""**Definisi & Penjelasan**

Topik yang Anda tanyakan adalah konsep fundamental dalam bidangnya.

**Aspek Penting:**
• Prinsip dasar dan cara kerjanya
• Manfaat dan kegunaannya
• Contoh penerapan praktis

Silakan tanya jika ada yang kurang jelas!""",
                
                f"""Mari kita bahas konsep ini:

**Inti Pembahasan:**
Ini adalah topik yang menarik dan berguna untuk dipahami.

**Poin-Poin Kunci:**
1. Pengertian dasar
2. Fungsi utama
3. Cara menggunakannya
4. Tips praktis

Ada pertanyaan lanjutan?"""
            ]
            return templates_id[variation % len(templates_id)]
        
        elif is_why:
            templates_id = [
                f"""**Mengapa?** Pertanyaan yang bagus!

**Alasan 1: Prinsip Fundamental**
Ini terjadi karena mekanisme mendasar yang bekerja di baliknya.

**Alasan 2: Pertimbangan Praktis**
Dari sudut pandang praktis, ini memberikan manfaat yang signifikan.

**Alasan 3: Konteks Lebih Luas**
Dalam konteks yang lebih luas, ini memiliki implikasi penting.

Apakah ini menjawab pertanyaan Anda?""",
                
                f"""Saya akan menjelaskan alasannya:

**Faktor Utama:**
• Aspek teknis yang mempengaruhi
• Keuntungan yang diberikan
• Kebutuhan yang dipenuhi

**Kesimpulan:**
Kombinasi faktor-faktor ini membuat hal ini penting dan relevan.

Butuh penjelasan lebih detail?""",
                f"""**Penjelasan Alasan:**

Ada beberapa faktor yang menjelaskan hal ini:

1. **Faktor Pertama** - Dasar teoretis
2. **Faktor Kedua** - Bukti empiris
3. **Faktor Ketiga** - Aplikasi praktis

Semoga ini memberikan pemahaman yang lebih baik!"""
            ]
            return templates_id[variation % len(templates_id)]
        
        else:
            # General responses in Indonesian
            templates_id = [
                f"""Terima kasih atas pertanyaan Anda! Saya akan membantu menjawabnya.

**Poin-Poin Penting:**

• Pertama, mari kita pahami konteks pertanyaan Anda
• Kedua, saya akan memberikan penjelasan yang relevan
• Ketiga, kita dapat mendiskusikan aspek spesifik yang Anda butuhkan

Apakah ada bagian tertentu yang ingin Anda eksplorasi lebih dalam?""",
                
                f"""Saya mengerti pertanyaan Anda. Mari kita bahas dengan detail:

**Analisis:**
Topik ini memiliki beberapa aspek menarik yang perlu dipertimbangkan.

**Pembahasan:**
1. Aspek pertama yang relevan
2. Hubungan dengan topik terkait
3. Implikasi praktis

Silakan beri tahu jika Anda butuh klarifikasi!""",
                
                f"""Pertanyaan yang menarik! Berikut pandangan saya:

**Penjelasan Utama:**
- Konsep dasar yang perlu dipahami
- Aplikasi dalam konteks nyata
- Tips dan best practices

**Kesimpulan:**
Ini adalah topik yang berguna untuk dipelajari lebih lanjut.

Ada yang ingin ditanyakan lagi?""",
                
                f"""Saya akan membantu menjelaskan topik ini:

**Gambaran Umum:**
Ini adalah aspek penting yang sering ditanyakan.

**Detail Pembahasan:**
• Pengertian dan konsep
• Cara kerja dan mekanisme
• Manfaat dan penggunaan

Semoga penjelasan ini membantu!""",
                
                f"""Mari kita eksplorasi topik ini bersama:

**Pendekatan:**
1. Memahami dasar-dasarnya
2. Melihat contoh praktis
3. Mengap likasikan dalam situasi nyata

**Insight Tambahan:**
Topik ini sangat relevan dan berguna untuk dikuasai.

Butuh informasi tambahan?"""
            ]
            return templates_id[variation % len(templates_id)]
    
    # English responses
    else:
        if is_code:
            return f"""I can help you with programming!

```python
# Example code structure
def example_function():
    # Your code here
    result = "Hello World"
    return result
```

**Key Concepts:**
- Variables and data types
- Control structures (if/else, loops)
- Functions and classes
- Error handling

Would you like to learn more about any specific aspect?"""
        
        elif is_how:
            templates_en = [
                f"""Let me explain how to do this:

**Step-by-Step Guide:**

1. **First Step** - Understand the fundamentals
2. **Second Step** - Apply the principles
3. **Third Step** - Practice and refine

Would you like more details on any particular step?""",
                
                f"""I'll guide you through this process:

**Implementation Phases:**

• **Preparation** - Gather necessary information
• **Execution** - Follow the main steps
• **Evaluation** - Review and optimize results

Let me know if you need clarification on any part!""",
                
                f"""Here's an effective approach:

**Recommended Method:**

1. Start with a solid foundation
2. Build progressively
3. Test and validate
4. Iterate for improvement

Does this answer your question?"""
            ]
            return templates_en[variation % len(templates_en)]
        
        elif is_what:
            templates_en = [
                f"""**Understanding:** {prompt[:50]}...

**Definition:**
Based on your question, this concept involves several key aspects.

**Main Characteristics:**
- Primary feature: Core functionality
- Supporting features: Additional capabilities
- Practical applications: Real-world usage

Would you like a deeper explanation?""",
                
                f"""**Definition & Explanation**

The topic you're asking about is a fundamental concept in its field.

**Important Aspects:**
• Basic principles and how it works
• Benefits and use cases
• Practical implementation examples

Feel free to ask if anything is unclear!""",
                
                f"""Let's explore this concept:

**Core Discussion:**
This is an interesting and useful topic to understand.

**Key Points:**
1. Basic understanding
2. Main functions
3. How to use it
4. Practical tips

Any follow-up questions?"""
            ]
            return templates_en[variation % len(templates_en)]
        
        elif is_why:
            templates_en = [
                f"""**Why?** Great question!

**Reason 1: Fundamental Principle**
This occurs due to the underlying mechanisms at work.

**Reason 2: Practical Considerations**
From a practical standpoint, this provides significant benefits.

**Reason 3: Broader Context**
In the broader context, this has important implications.

Does this answer your question?""",
                
                f"""I'll explain the reasoning:

**Main Factors:**
• Technical aspects that influence this
• Advantages it provides
• Needs it fulfills

**Conclusion:**
The combination of these factors makes this important and relevant.

Need more details?""",
                
                f"""**Explanation of Reasons:**

Several factors explain this:

1. **First Factor** - Theoretical foundation
2. **Second Factor** - Empirical evidence
3. **Third Factor** - Practical applications

Hope this provides better understanding!"""
            ]
            return templates_en[variation % len(templates_en)]
        
        else:
            # General responses in English
            templates_en = [
                f"""Thank you for your question! I'll help answer it.

**Key Points:**

• First, let's understand the context of your question
• Second, I'll provide relevant explanations
• Third, we can discuss specific aspects you need

Is there any particular area you'd like to explore further?""",
                
                f"""I understand your question. Let's discuss it in detail:

**Analysis:**
This topic has several interesting aspects to consider.

**Discussion:**
1. First relevant aspect
2. Connections to related topics
3. Practical implications

Let me know if you need clarification!""",
                
                f"""Interesting question! Here's my perspective:

**Main Explanation:**
- Core concepts to understand
- Real-world applications
- Tips and best practices

**Conclusion:**
This is a useful topic to learn more about.

Anything else you'd like to know?""",
                
                f"""I'll help explain this topic:

**Overview:**
This is an important aspect that's frequently asked about.

**Detailed Discussion:**
• Definitions and concepts
• How it works and mechanisms
• Benefits and usage

Hope this explanation helps!""",
                
                f"""Let's explore this topic together:

**Approach:**
1. Understanding the basics
2. Looking at practical examples
3. Applying in real situations

**Additional Insight:**
This topic is very relevant and useful to master.

Need more information?"""
            ]
            return templates_en[variation % len(templates_en)]


def get_model_response(prompt, model_name='auto', user=None, history=None, stream=False):
    """Get response from specified model - sends user input directly to AI.
    
    Args:
        prompt: User prompt/message - SENT DIRECTLY TO AI MODEL
        model_name: Model to use ('auto' for automatic selection)
        user: User object
        history: Conversation history (list of dicts with 'role' and 'content')
        stream: If True, returns generator for streaming responses
    
    Returns:
        str or generator: AI response directly from model
    """
    from flask import current_app
    
    print(f"\n=== MODEL SERVICE DEBUG ===")
    print(f"User prompt: {prompt}")
    print(f"Requested model: {model_name}")
    
    # Build context from history if provided - FULL CONVERSATION HISTORY
    if history:
        # Include ALL messages (both user and assistant) for full context
        conversation_context = []
        
        # Patterns to detect and skip mock/fallback responses
        mock_patterns = [
            "[Response generated by",
            "mock implementation",
            "(Model not loaded",
            "using fallback)",
            "Previous conversation:",
            "Interesting question! Regarding"
        ]
        
        for msg in history:  # ALL messages, not just last 5
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            if content.strip():
                # Skip messages with mock response patterns
                is_mock = any(pattern in content for pattern in mock_patterns)
                if not is_mock:
                    if role == 'user':
                        conversation_context.append(f"User: {content}")
                    else:
                        conversation_context.append(f"Assistant: {content}")
        
        # Build full conversation history with current prompt
        if conversation_context:
            context = "\n".join(conversation_context)
            full_prompt = f"{context}\nUser: {prompt}\nAssistant:"
        else:
            full_prompt = f"User: {prompt}\nAssistant:"
    else:
        # User's prompt goes DIRECTLY to AI model
        full_prompt = f"User: {prompt}\nAssistant:"
    
    print(f"Full prompt to AI: {full_prompt[:200]}...")
    
    # Auto-select model based on content if requested
    if model_name == 'auto':
        model_name = select_model_for_content(prompt)
        print(f"Auto-selected model: {model_name}")
    
    # Validate model exists
    if model_name not in MODELS:
        print(f"WARNING: Model '{model_name}' not found in MODELS: {list(MODELS.keys())}")
        print(f"Available models: {list(MODELS.keys())}")
        # Default to gpt4all
        model_name = 'gpt4all'
        print(f"Falling back to: {model_name}")
    
    print(f"Final selected model: {model_name}")
    
    try:
        model = MODELS[model_name]
        print(f"Model loaded status: {model.is_loaded()}")
        
        if not model.is_loaded():
            print(f"WARNING: Model {model_name} is not loaded, will use fallback response")
        
        # Generate response from model - USER INPUT GOES DIRECTLY HERE
        if stream:
            # Return generator for streaming
            print(f"Streaming mode enabled")
            print(f"=== END DEBUG ===\n")
            return model.generate(full_prompt, user, stream=True)
        else:
            # Return complete response
            response = model.generate(full_prompt, user, stream=False)
            print(f"AI response generated: {len(response)} characters")
            print(f"Response preview: {response[:200]}...")
            print(f"=== END DEBUG ===\n")
            return response
        
    except Exception as e:
        print(f"ERROR in get_model_response: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        print(f"=== END DEBUG (ERROR) ===\n")
        
        # Return user-friendly error message
        if stream:
            yield f"AI model error: {str(e)}"
        else:
            raise Exception(f"AI model error: {str(e)}")


def get_available_models():
    """Get list of available models with their status."""
    models_info = [
        {
            'id': 'auto',
            'name': 'Auto-Select',
            'description': 'Automatically selects the best model for your task',
            'recommended': True,
            'loaded': True
        },
        {
            'id': 'deepseek',
            'name': 'DeepSeek Coder',
            'description': 'Specialized for coding, debugging, and programming tasks',
            'use_case': 'Coding & Development',
            'loaded': MODELS['deepseek'].is_loaded()
        },
        {
            'id': 'gpt4all',
            'name': 'GPT4All',
            'description': 'General purpose conversational AI for everyday tasks',
            'use_case': 'General Chat',
            'loaded': MODELS['gpt4all'].is_loaded()
        },
        {
            'id': 'llama',
            'name': 'Llama.cpp',
            'description': 'Optimized for document processing and large files',
            'use_case': 'Files & Documents',
            'loaded': MODELS['llama'].is_loaded()
        },
        {
            'id': 'vicuna',
            'name': 'Vicuna',
            'description': 'Multimodal model for images, videos, and rich content',
            'use_case': 'Images & Videos',
            'loaded': MODELS['vicuna'].is_loaded()
        }
    ]
    return models_info
