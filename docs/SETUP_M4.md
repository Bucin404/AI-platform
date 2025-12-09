# MacBook M4 Setup Guide

Complete guide for setting up the AI Platform on MacBook M4 (Apple Silicon) with optimal performance.

## Prerequisites

### 1. Docker Desktop for Mac
```bash
# Install Docker Desktop (Apple Silicon version)
# Download from: https://www.docker.com/products/docker-desktop/

# Or using Homebrew:
brew install --cask docker
```

### 2. Docker Desktop Configuration

Open Docker Desktop → Settings:

**General:**
- ✅ Enable VirtioFS accelerated directory sharing
- ✅ Use Rosetta for x86/amd64 emulation (if needed)

**Resources:**
- CPUs: **6-8 cores** (M4 has 10 cores, reserve some for macOS)
- Memory: **12-16 GB** (depends on your total RAM)
- Swap: **2 GB**
- Disk image size: **64 GB+** (models are large)

**Advanced:**
- ✅ Enable default Docker socket

## Quick Start

### 1. Clone and Configure

```bash
# Clone repository
git clone https://github.com/Bucin404/AI-platform.git
cd AI-platform

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### 2. Download AI Models

```bash
# Install Python dependencies first
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download models (choose one):

# Option A: Standard models (~16 GB)
python download_models.py

# Option B: Lite models (~1.6 GB) - Recommended for M4
python download_models.py --lite

# Option C: Specific models only
python download_models.py --models deepseek-coder-lite tinyllama
```

### 3. Check Integration Status

```bash
# Check if models are ready
python integrate_models.py

# Generate environment configuration
python integrate_models.py --generate-env
```

### 4. Start with Docker Compose

```bash
# Start all services (optimized for M4)
docker-compose -f docker-compose.m4.yml up -d

# View logs
docker-compose -f docker-compose.m4.yml logs -f web

# Check status
docker-compose -f docker-compose.m4.yml ps
```

### 5. Initialize Database

```bash
# Run migrations
docker-compose -f docker-compose.m4.yml exec web flask db upgrade

# Create admin user
docker-compose -f docker-compose.m4.yml exec web flask create-admin

# Or interactive mode:
docker-compose -f docker-compose.m4.yml exec web flask shell
```

### 6. Access Application

- **Web App:** http://localhost:5000
- **pgAdmin:** http://localhost:5050 (if tools profile enabled)
- **Redis Commander:** http://localhost:8081 (if tools profile enabled)

## Development Workflow

### Hot Reload Enabled

The M4 Docker Compose configuration includes hot-reload. Any changes to Python files will automatically restart the application.

```bash
# Edit files locally
nano app/services/model_service.py

# Changes automatically detected and reloaded
# Watch logs to see reload:
docker-compose -f docker-compose.m4.yml logs -f web
```

### Running Commands

```bash
# Flask commands
docker-compose -f docker-compose.m4.yml exec web flask --help

# Python shell
docker-compose -f docker-compose.m4.yml exec web python

# Run tests
docker-compose -f docker-compose.m4.yml exec web pytest

# Database migrations
docker-compose -f docker-compose.m4.yml exec web flask db migrate -m "Description"
docker-compose -f docker-compose.m4.yml exec web flask db upgrade
```

### Using Optional Tools

```bash
# Start with pgAdmin and Redis Commander
docker-compose -f docker-compose.m4.yml --profile tools up -d

# pgAdmin: http://localhost:5050
# Email: admin@aiplatform.com
# Password: admin

# Redis Commander: http://localhost:8081
```

## Model Integration with Metal Acceleration

### Install llama-cpp-python with Metal Support

For best performance on M4, install llama-cpp-python with Metal acceleration:

```bash
# Activate virtual environment
source venv/bin/activate

# Install with Metal support
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

# Verify installation
python -c "from llama_cpp import Llama; print('✅ llama-cpp-python installed')"
```

### Update Model Service

Edit `app/services/model_service.py` to use actual models:

```python
from llama_cpp import Llama

class DeepSeekAdapter(ModelAdapter):
    def __init__(self, model_path='./models/deepseek-coder-1.3b-instruct.Q4_K_M.gguf'):
        self.model = Llama(
            model_path=model_path,
            n_ctx=4096,
            n_threads=4,
            n_gpu_layers=0,  # CPU only, Metal automatically used
            use_mlock=True,  # Keep model in RAM
            verbose=False
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

### Restart Application

```bash
docker-compose -f docker-compose.m4.yml restart web
```

## Performance Optimization

### 1. M4 Neural Engine Utilization

The M4 chip includes a 16-core Neural Engine. While llama.cpp doesn't directly use it, Metal acceleration provides significant speedup:

- **Without Metal:** ~5-10 tokens/sec
- **With Metal:** ~20-40 tokens/sec (depending on model size)

### 2. Memory Management

```bash
# Monitor memory usage
docker stats

# Adjust memory limits in docker-compose.m4.yml:
deploy:
  resources:
    limits:
      memory: 8G  # Adjust based on your models
```

### 3. Model Selection for M4

Recommended models for M4 (balance of speed and quality):

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| **TinyLlama 1.1B** | 0.7 GB | ⚡⚡⚡ | ⭐⭐ | General, fast responses |
| **DeepSeek 1.3B** | 0.9 GB | ⚡⚡⚡ | ⭐⭐⭐ | Coding, good balance |
| **Llama 2 7B** | 4.1 GB | ⚡⚡ | ⭐⭐⭐⭐ | Quality responses |
| **DeepSeek 6.7B** | 4.1 GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Best code quality |

### 4. Concurrent Model Loading

For better performance, you can load multiple small models:

```python
# Load different models for different tasks
deepseek_1b = DeepSeekAdapter('./models/deepseek-coder-1.3b-instruct.Q4_K_M.gguf')
tinyllama = GPT4AllAdapter('./models/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf')
```

## Troubleshooting

### Docker Issues

```bash
# Reset Docker Desktop
# Docker Desktop → Troubleshoot → Reset to factory defaults

# Clean up Docker resources
docker system prune -a --volumes

# Restart Docker Desktop
killall Docker && open /Applications/Docker.app
```

### Port Conflicts

```bash
# Check if ports are in use
lsof -i :5000
lsof -i :5432
lsof -i :6379

# Kill processes if needed
kill -9 <PID>

# Or change ports in docker-compose.m4.yml
```

### Model Loading Errors

```bash
# Check if models exist
ls -lh models/

# Verify model integrity
python integrate_models.py

# Re-download if corrupted
python download_models.py --force
```

### Performance Issues

```bash
# Check Docker resource usage
docker stats

# Monitor M4 performance
sudo powermetrics --samplers cpu_power,gpu_power -i 1000

# Check if Metal is being used (in container logs)
docker-compose -f docker-compose.m4.yml logs web | grep -i metal
```

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose -f docker-compose.m4.yml ps postgres

# Test connection
docker-compose -f docker-compose.m4.yml exec postgres psql -U aiplatform -d aiplatform

# Reset database
docker-compose -f docker-compose.m4.yml down -v
docker-compose -f docker-compose.m4.yml up -d
```

## Advanced Configuration

### Custom Model Paths

Create a `.env.local` file:

```bash
# Model paths
MODEL_DEEPSEEK_PATH=/path/to/your/model.gguf
MODEL_LLAMA_PATH=/path/to/llama.gguf

# Performance tuning
MODEL_N_THREADS=6
MODEL_N_CTX=4096
MODEL_N_GPU_LAYERS=0
```

### Load Balancing Multiple Models

For production-like setup on M4:

```bash
# Use docker-compose with multiple web instances
docker-compose -f docker-compose.m4.yml up -d --scale web=2
```

### Monitoring and Logging

```bash
# View real-time logs
docker-compose -f docker-compose.m4.yml logs -f

# Export logs
docker-compose -f docker-compose.m4.yml logs > app.log

# Monitor with ctop (install: brew install ctop)
ctop
```

## Comparison: Native vs Docker

### Native Python (Recommended for Development)

**Pros:**
- Direct Metal acceleration
- Faster model loading
- Better debugging

**Cons:**
- Manual dependency management
- No isolation

```bash
# Native setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

# Run directly
python run.py
```

### Docker (Recommended for Consistency)

**Pros:**
- Consistent environment
- Easy deployment
- Service isolation

**Cons:**
- Slight overhead
- More complex setup

## Next Steps

1. ✅ Set up development environment
2. ✅ Download and integrate models
3. 📝 Read [Model Documentation](MODELS.md)
4. 🧪 Run tests: `pytest`
5. 🚀 Deploy to production (see [DEPLOY.md](DEPLOY.md))

## Resources

- [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)
- [llama.cpp Metal Support](https://github.com/ggerganov/llama.cpp#metal-build)
- [Apple Silicon Optimization Guide](https://developer.apple.com/metal/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## Support

For issues specific to M4 setup, please check:
- Docker Desktop logs: `~/Library/Containers/com.docker.docker/Data/log`
- Application logs: `docker-compose -f docker-compose.m4.yml logs`
- GitHub Issues: [Report a bug](https://github.com/Bucin404/AI-platform/issues)
