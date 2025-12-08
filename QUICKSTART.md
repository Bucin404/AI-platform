# Quick Start - Download AI Models

## 🚀 Automatic Model Download

The platform now includes an automatic model downloader to get all required open-source AI models.

### Step 1: List Available Models

```bash
python download_models.py --list
```

### Step 2: Choose Your Version

**Standard Models** (Recommended for production, ~16 GB total):
```bash
python download_models.py
```

**Lite Models** (For limited resources, ~1.6 GB total):
```bash
python download_models.py --lite
```

**Specific Models Only**:
```bash
python download_models.py --models deepseek-coder gpt4all
```

### Step 3: Wait for Download

The script will:
- ✅ Show progress bars for each download
- ✅ Automatically retry on failures
- ✅ Skip already downloaded files
- ✅ Verify file integrity

### Step 4: Integrate Models

See `docs/MODELS.md` for instructions on integrating downloaded models with the application.

## 📋 Available Models

### Standard (7B Parameters)
- **DeepSeek Coder 6.7B** (4.1 GB) - For coding tasks
- **Llama 2 7B** (4.1 GB) - For documents
- **GPT4All Falcon** (3.9 GB) - For general chat
- **Vicuna 7B** (4.1 GB) - For multimodal

### Lite (1-2B Parameters)
- **DeepSeek Coder 1.3B** (0.9 GB) - Coding
- **TinyLlama 1.1B** (0.7 GB) - General

## 🔧 Advanced Options

```bash
# Force re-download (overwrite existing)
python download_models.py --force

# Download to custom directory (edit models_config.py)
# Change DOWNLOAD_SETTINGS['models_dir']

# Resume interrupted download
python download_models.py  # Just run again
```

## 📚 Documentation

- Full guide: [docs/MODELS.md](docs/MODELS.md)
- Installation: [docs/INSTALL.md](docs/INSTALL.md)
- Configuration: `models_config.py`

## ⚠️ Notes

- Models are **large files** (GB range)
- Requires **stable internet connection**
- First-time download may take 30-60 minutes
- Models are downloaded from trusted sources (Hugging Face, GPT4All)
- All models are **open-source** and free to use

## 🐳 Docker Users

```bash
# Download models first (on host)
python download_models.py

# Models will be mounted to container via docker-compose.yml
docker-compose up -d
```

## ❓ Troubleshooting

**Download failed?**
- Check internet connection
- Run script again (auto-resumes)
- Check disk space: `df -h`

**Models not loading?**
- Verify files in `./models` directory
- Check file sizes match expected
- See integration guide in `docs/MODELS.md`

## 📝 Current Status

By default, the platform uses **mock adapters** (placeholder responses) for development. Download and integrate actual models to enable real AI responses.
