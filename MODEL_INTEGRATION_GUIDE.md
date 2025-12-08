# Model Integration Guide

## Overview

This platform supports **automatic model download** and provides **integration tools** to make downloaded models work with the application.

## Current Status: Mock Mode (Default)

By default, the platform runs in **mock mode**:
- ✅ All features work (routing, rate limiting, chat UI)
- ✅ Models return placeholder responses
- ✅ Perfect for testing and development
- ❌ Not using actual AI models

## Two-Step Process

### Step 1: Download Models

```bash
# Download all standard models (~16 GB)
python download_models.py

# OR download lite versions (~1.6 GB)
python download_models.py --lite

# OR download specific models
python download_models.py --models deepseek-coder gpt4all
```

**What happens:**
- ✅ Models downloaded to `./models` directory
- ✅ Files are verified and ready to use
- ❌ Not yet integrated with application

### Step 2: Check Integration Status

```bash
# Check if models are ready
python integrate_models.py

# Generate environment configuration
python integrate_models.py --generate-env
```

**What you'll see:**
- List of downloaded models
- Integration status
- Step-by-step instructions
- Example code for integration

## Are Models Automatically Integrated?

**Short Answer: Not Yet - By Design**

**Why not automatic?**
1. **Library dependency**: Requires `llama-cpp-python` which needs compilation
2. **Resource consideration**: Real models use significant RAM/CPU
3. **Flexibility**: You choose which models to actually use
4. **Development mode**: Mock mode is faster for testing

## Making Models Work (Manual Integration)

### Option A: Quick Integration (Recommended for M4)

```bash
# 1. Install llama-cpp-python with Metal support
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

# 2. Update model_service.py (see example below)

# 3. Restart application
docker-compose -f docker-compose.m4.yml restart web
```

### Option B: Full Integration

Edit `app/services/model_service.py`:

```python
from llama_cpp import Llama

class DeepSeekAdapter(ModelAdapter):
    """Adapter for DeepSeek models."""
    
    def __init__(self, model_path='./models/deepseek-coder-1.3b-instruct.Q4_K_M.gguf'):
        try:
            # Load the actual model
            self.model = Llama(
                model_path=model_path,
                n_ctx=4096,        # Context window
                n_threads=4,       # CPU threads
                n_gpu_layers=0,    # 0 for CPU, -1 for full GPU
                use_mlock=True,    # Keep in RAM
                verbose=False
            )
            self.is_loaded = True
            print(f"✅ DeepSeek model loaded from {model_path}")
        except Exception as e:
            print(f"⚠️  Could not load model: {e}")
            print("   Falling back to mock mode")
            self.model = None
            self.is_loaded = False
    
    def generate(self, prompt, user=None):
        """Generate response using DeepSeek."""
        if not self.is_loaded or self.model is None:
            # Fallback to mock response
            return f"[Mock Response - Model not loaded]\n\nPrompt: {prompt[:100]}..."
        
        try:
            response = self.model(
                prompt,
                max_tokens=512,
                temperature=0.7,
                top_p=0.95,
                stop=["User:", "###"],
            )
            return response['choices'][0]['text']
        except Exception as e:
            return f"[Error generating response: {e}]"
    
    def get_name(self):
        status = "loaded" if self.is_loaded else "mock"
        return f"deepseek-coder ({status})"
```

## Integration Verification

After integration, verify models are working:

```bash
# 1. Check application logs
docker-compose -f docker-compose.m4.yml logs web | grep -i "model loaded"

# 2. Test via UI
# - Login to the app
# - Send a message
# - Check if response is from actual model (not mock)

# 3. Check via API
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Write a Python function"}'
```

## MacBook M4 Specific

### Automatic Integration with Metal

For M4 users, the docker-compose.m4.yml is pre-configured:

```yaml
environment:
  - GGML_METAL=1      # Enable Metal
  - LLAMA_METAL=1     # Metal acceleration
```

**Benefits:**
- ✅ Automatic Metal acceleration (20-40 tokens/sec)
- ✅ Neural Engine utilization
- ✅ Optimized for ARM64

### Setup for M4

```bash
# 1. Download models
python download_models.py --lite  # Recommended for local dev

# 2. Check integration
python integrate_models.py

# 3. Install llama-cpp-python with Metal
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

# 4. Update model_service.py (as shown above)

# 5. Start with M4 config
docker-compose -f docker-compose.m4.yml up -d

# 6. Watch logs for model loading
docker-compose -f docker-compose.m4.yml logs -f web
```

## Deployment Modes

### Development (Mock Mode)
- No additional setup required
- Fast startup
- Good for UI/feature testing

### Development (Real Models)
- Download models
- Install llama-cpp-python
- Update model_service.py
- Good for testing AI responses

### Production
- Pre-download models to production server
- Configure model paths in .env
- Ensure sufficient RAM (8GB+ for 7B models)
- Use GPU acceleration if available

## Troubleshooting

### Models Downloaded but Not Working

```bash
# Check if files exist
ls -lh models/

# Run integration check
python integrate_models.py

# Verify llama-cpp-python is installed
python -c "from llama_cpp import Llama; print('✅ Installed')"

# Check application logs
docker-compose -f docker-compose.m4.yml logs web
```

### Out of Memory

```bash
# Use smaller models
python download_models.py --lite

# Or adjust context window
n_ctx=2048  # Instead of 4096

# Or load models on-demand (lazy loading)
```

### Slow Performance

**For M4:**
```bash
# Ensure Metal is enabled
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

# Check Metal is being used
docker-compose -f docker-compose.m4.yml logs web | grep -i metal
```

**General:**
```bash
# Reduce context window
n_ctx=2048

# Use quantized models (Q4_K_M)
# Already used in download_models.py

# Increase threads
n_threads=8  # Based on your CPU
```

## FAQ

### Q: Do I need to download models to use the platform?
**A:** No, the platform works in mock mode without downloading models.

### Q: After downloading, are models automatically used?
**A:** No, you need to install llama-cpp-python and update model_service.py. This gives you control over which models to use.

### Q: Can I use some models and keep others in mock mode?
**A:** Yes! Configure only the models you want to use. Others will fall back to mock mode.

### Q: How much RAM do I need?
**A:**
- Lite models (1-2B): 4GB RAM
- Standard models (7B): 8-16GB RAM
- Multiple models: Add RAM requirements

### Q: Will it work on M4?
**A:** Yes! M4 configuration is optimized with Metal acceleration. Use docker-compose.m4.yml.

### Q: Can I use GPU?
**A:** Yes, set `n_gpu_layers=-1` in model configuration. Requires CUDA (NVIDIA) or Metal (Apple Silicon).

## Summary

1. ✅ **Download**: `python download_models.py`
2. ✅ **Check**: `python integrate_models.py`
3. ✅ **Install**: `pip install llama-cpp-python`
4. ✅ **Configure**: Update `model_service.py`
5. ✅ **Restart**: Application will use real models

**For M4 specifically**: See [docs/SETUP_M4.md](docs/SETUP_M4.md) for complete guide.
