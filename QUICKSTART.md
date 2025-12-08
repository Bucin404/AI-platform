# Quick Start - AI Models (Fully Automated!)

## 🚀 One-Command Setup (RECOMMENDED)

The platform now includes **automatic download AND integration** for all AI models!

### Just Run This:

**Standard Models** (Recommended, ~16 GB total):
```bash
python download_models.py
```

**Lite Models** (For limited resources, ~1.6 GB total):
```bash
python download_models.py --lite
```

**That's it!** The script will:
1. ✅ Download all models with progress bars
2. ✅ Install `llama-cpp-python` automatically
3. ✅ Configure the platform to use real models
4. ✅ Update all necessary files

After download completes:
```bash
# Restart the application
docker-compose restart web
# or
python run.py
```

**Models are now fully integrated and ready to use! No manual steps required.**

## 📋 Check Before Download (Optional)

List available models:
```bash
python download_models.py --list
```

Download specific models only:
```bash
python download_models.py --models deepseek-coder gpt4all
```

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

## 📝 How It Works

**Before Download:**
- Platform uses **mock adapters** (placeholder responses) for development

**After Download:**
- Models are automatically integrated
- Real AI models load on application startup
- Platform intelligently routes queries to best model

**Manual Integration (Optional):**
If automatic integration fails, you can manually integrate:
```bash
python integrate_models.py --auto
```

## 🎯 Model Selection

The platform automatically selects the best model for your task:
- **DeepSeek Coder** → Coding, debugging, programming
- **Llama 2** → Documents, large files, PDFs
- **Vicuna** → Images, videos, multimodal content
- **GPT4All** → General conversation

Or manually select any model in the chat interface.
