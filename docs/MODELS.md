# AI Models Download Guide

This guide explains how to download and configure open-source AI models for the platform.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Download Models

**Option A: Download all standard models (Recommended)**
```bash
python download_models.py
```

**Option B: Download lite versions (for limited resources)**
```bash
python download_models.py --lite
```

**Option C: Download specific models only**
```bash
python download_models.py --models deepseek-coder gpt4all
```

## Available Models

### Standard Models (~16 GB total)

| Model | Size | Use Case | Description |
|-------|------|----------|-------------|
| **DeepSeek Coder 6.7B** | 4.1 GB | Coding | Specialized for programming and debugging tasks |
| **Llama 2 7B** | 4.1 GB | Documents | Optimized for document processing and analysis |
| **GPT4All Falcon** | 3.9 GB | General Chat | General purpose conversational AI |
| **Vicuna 7B v1.5** | 4.1 GB | Multimodal | For images, videos, and rich content |

### Lite Models (~1.6 GB total)

| Model | Size | Use Case | Description |
|-------|------|----------|-------------|
| **DeepSeek Coder 1.3B** | 0.9 GB | Coding | Lightweight version for coding tasks |
| **TinyLlama 1.1B** | 0.7 GB | General | Lightweight model for general tasks |

## Download Script Usage

### List Available Models
```bash
python download_models.py --list
```

### Download with Options
```bash
# Force re-download (overwrite existing)
python download_models.py --force

# Download specific models
python download_models.py --models deepseek-coder

# Download lite version of specific models
python download_models.py --lite --models deepseek-coder-lite
```

### Help
```bash
python download_models.py --help
```

## Model Configuration

Models are downloaded to the `./models` directory by default. Configuration can be customized in `models_config.py`:

```python
DOWNLOAD_SETTINGS = {
    'models_dir': './models',
    'chunk_size': 8192,
    'timeout': 300,
    'retry_attempts': 3,
}
```

## Integration with Application

After downloading models, update `app/services/model_service.py` to load the actual models:

### Example: Loading DeepSeek Coder

```python
class DeepSeekAdapter(ModelAdapter):
    def __init__(self, model_path='./models/deepseek-coder-6.7b-instruct.Q4_K_M.gguf'):
        from llama_cpp import Llama
        self.model = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=4,
        )
    
    def generate(self, prompt, user=None):
        response = self.model(
            prompt,
            max_tokens=512,
            temperature=0.7,
            top_p=0.95,
        )
        return response['choices'][0]['text']
```

### Required Library

For loading GGUF models, install:
```bash
pip install llama-cpp-python
```

For GPU acceleration:
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
```

## Troubleshooting

### Download Fails

1. **Check internet connection**: Models are large files (GB)
2. **Retry**: Script automatically retries 3 times
3. **Resume**: Re-run script, it skips existing files
4. **Manual download**: Download directly from URLs in `models_config.py`

### Disk Space Issues

- Standard models: ~16 GB required
- Lite models: ~1.6 GB required
- Check available space: `df -h`
- Use `--models` flag to download only needed models

### Model Loading Errors

1. **Verify file integrity**: Check file size matches expected
2. **Check permissions**: Ensure files are readable
3. **Update model paths**: Edit `app/services/model_service.py`

## Model Sources

All models are from trusted open-source repositories:

- **DeepSeek Coder**: [Hugging Face - TheBloke](https://huggingface.co/TheBloke/deepseek-coder-6.7B-instruct-GGUF)
- **Llama 2**: [Hugging Face - TheBloke](https://huggingface.co/TheBloke/Llama-2-7B-GGUF)
- **GPT4All**: [GPT4All Official](https://gpt4all.io)
- **Vicuna**: [Hugging Face - TheBloke](https://huggingface.co/TheBloke/vicuna-7B-v1.5-GGUF)

## Docker Integration

To use models in Docker:

1. **Download models on host**:
```bash
python download_models.py
```

2. **Mount in docker-compose.yml**:
```yaml
web:
  volumes:
    - ./models:/app/models:ro
```

3. **Update Dockerfile** (if building image with models):
```dockerfile
COPY models/ /app/models/
```

## Performance Optimization

### CPU Optimization
- Use quantized models (Q4_K_M) for best CPU performance
- Adjust `n_threads` based on CPU cores
- Set `n_ctx` based on RAM availability

### GPU Acceleration
- Install CUDA-enabled llama-cpp-python
- Models will automatically use GPU if available
- Monitor GPU memory usage

### Memory Requirements

| Model Size | Min RAM | Recommended RAM |
|------------|---------|-----------------|
| 1.3B (Lite) | 2 GB | 4 GB |
| 7B (Standard) | 8 GB | 16 GB |

## License

All downloaded models are open-source and subject to their respective licenses:
- DeepSeek Coder: MIT License
- Llama 2: Llama 2 Community License
- GPT4All: Apache 2.0
- Vicuna: Non-commercial research use

Please review individual model licenses before commercial deployment.
