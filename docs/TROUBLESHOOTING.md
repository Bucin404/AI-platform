# Troubleshooting Guide

This guide helps you solve common issues when setting up and running the AI Platform.

## Database Connection Errors

### Error: `sqlalchemy.exc.OperationalError` when running `flask db migrate`

**Symptoms:**
```
Traceback (most recent call last):
  File "...sqlalchemy/engine/base.py", line 143, in __init__
    self._dbapi_connection = engine.raw_connection()
...
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**Cause:** PostgreSQL is not running or the database URL is incorrect for local development.

**Solutions:**

#### Option 1: Use SQLite (Easiest for Local Development)

SQLite doesn't require a separate database server and works great for development.

1. Create/edit your `.env` file:
```bash
cp .env.local.example .env
```

2. Update the database URL to use SQLite:
```bash
DATABASE_URL=sqlite:///app.db
```

3. Initialize the database:
```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

4. Run the application:
```bash
python run.py
```

#### Option 2: Install and Configure PostgreSQL Locally

**On macOS:**
```bash
# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Create database and user
psql postgres
CREATE DATABASE aiplatform;
CREATE USER aiplatform WITH PASSWORD 'aiplatform';
GRANT ALL PRIVILEGES ON DATABASE aiplatform TO aiplatform;
\q
```

**On Ubuntu/Linux:**
```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
CREATE DATABASE aiplatform;
CREATE USER aiplatform WITH PASSWORD 'aiplatform';
GRANT ALL PRIVILEGES ON DATABASE aiplatform TO aiplatform;
\q
```

**Then update your `.env` file:**
```bash
# Use localhost instead of 'postgres' (Docker service name)
DATABASE_URL=postgresql://aiplatform:aiplatform@localhost:5432/aiplatform
```

**Run migrations:**
```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

#### Option 3: Use Docker (Recommended)

The easiest way is to use Docker which handles all dependencies:

```bash
# Use .env.example as is (it's configured for Docker)
cp .env.example .env

# Start all services (web, postgres, redis)
docker-compose up -d

# Run migrations inside container
docker-compose exec web flask db init
docker-compose exec web flask db migrate -m "Initial migration"
docker-compose exec web flask db upgrade

# Create admin user
docker-compose exec web flask create-admin
```

Access the app at `http://localhost:5000`

## Redis Connection Errors

**Error:** Cannot connect to Redis

**Solution:**

1. **Use in-memory rate limiting** (no Redis required):
   ```bash
   # In .env, leave REDIS_URL empty or comment it out
   # REDIS_URL=
   ```
   The platform will automatically use in-memory rate limiting.

2. **Or install Redis locally:**
   
   **macOS:**
   ```bash
   brew install redis
   brew services start redis
   ```
   
   **Ubuntu:**
   ```bash
   sudo apt-get install redis-server
   sudo systemctl start redis
   ```
   
   Then in `.env`:
   ```bash
   REDIS_URL=redis://localhost:6379/0
   ```

## Model Loading Issues

### Models not found after download

**Check models directory:**
```bash
ls -lh ./models/
```

You should see files like:
- `deepseek-coder-6.7b-instruct.Q4_K_M.gguf` (or 1.3B for lite)
- `llama-2-7b.Q4_K_M.gguf`
- `gpt4all-falcon-newbpe-q4_0.gguf`
- `vicuna-7b-v1.5.Q4_K_M.gguf`

**If models are missing:**
```bash
# Re-download
python download_models.py

# Or download lite versions
python download_models.py --lite
```

### Models fail to load

**Check if llama-cpp-python is installed:**
```bash
pip list | grep llama-cpp-python
```

**If not installed, the download script should have installed it. Manually install:**
```bash
# For macOS with Metal acceleration
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/metal

# For Linux with CUDA
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121

# For CPU only
pip install llama-cpp-python
```

### Mock mode vs Real models

The platform runs in **mock mode** by default if models aren't available. This is normal for development/testing.

**To enable real models:**
1. Download models: `python download_models.py`
2. Restart the application: `docker-compose restart web` or re-run `python run.py`
3. Models should load automatically on startup

**Check if models are loaded:**
Look for these messages in the console when starting the app:
```
✅ Llama model loaded successfully
✅ GPT4All model loaded successfully
✅ DeepSeek model loaded successfully
✅ Vicuna model loaded successfully
```

## Docker Issues

### Port already in use

**Error:** `Bind for 0.0.0.0:5000 failed: port is already allocated`

**Solution:**
```bash
# Find and stop the process using port 5000
lsof -ti:5000 | xargs kill -9

# Or change the port in docker-compose.yml
# ports:
#   - "5001:5000"  # Use 5001 instead
```

### Docker containers not starting

**Check logs:**
```bash
docker-compose logs web
docker-compose logs postgres
docker-compose logs redis
```

**Restart services:**
```bash
docker-compose down
docker-compose up -d
```

## MacBook M4 Specific Issues

### Slow performance

Use the M4-optimized configuration:
```bash
docker-compose -f docker-compose.m4.yml up -d
```

This uses ARM64-native images and enables Metal acceleration.

### Python version issues

Ensure you're using Python 3.11+:
```bash
python3 --version
```

If you have Python 3.14 (like in the error), that's fine, but you may need to install from source:
```bash
python3.14 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Permission Errors

### Cannot write to models directory

```bash
# Create models directory with correct permissions
mkdir -p models
chmod 755 models
```

### Flask db commands fail

```bash
# Make sure FLASK_APP is set
export FLASK_APP=run.py

# Or use full path
python -m flask db migrate -m "Initial migration"
```

## Common Setup Mistakes

### 1. Wrong .env file for local development

❌ **Wrong:** Using `.env.example` as-is for local development
```bash
DATABASE_URL=postgresql://aiplatform:aiplatform@postgres:5432/aiplatform
```
This uses `postgres` which is the Docker service name.

✅ **Correct:** For local development, use:
```bash
DATABASE_URL=postgresql://aiplatform:aiplatform@localhost:5432/aiplatform
# Or use SQLite:
DATABASE_URL=sqlite:///app.db
```

### 2. Not activating virtual environment

```bash
# Always activate venv first
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows
```

### 3. PostgreSQL not running

Check if PostgreSQL is running:
```bash
# macOS
brew services list | grep postgresql

# Linux
sudo systemctl status postgresql
```

## Getting Help

If you're still having issues:

1. **Check the logs:**
   - Docker: `docker-compose logs web`
   - Local: Check console output when running `python run.py`

2. **Verify environment:**
   ```bash
   # Check Python version
   python --version
   
   # Check installed packages
   pip list
   
   # Check environment variables
   cat .env
   ```

3. **Start fresh:**
   ```bash
   # Docker
   docker-compose down -v  # Remove volumes
   docker-compose up -d --build  # Rebuild
   
   # Local
   rm -rf venv migrations app.db
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Use SQLite for quick testing:**
   This is the fastest way to get started without external dependencies:
   ```bash
   DATABASE_URL=sqlite:///app.db
   REDIS_URL=
   ```

5. **Check documentation:**
   - Installation: `docs/INSTALL.md`
   - M4 Setup: `docs/SETUP_M4.md`
   - Models: `docs/MODELS.md`
   - API: `docs/API.md`

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Can't connect to database | Use `DATABASE_URL=sqlite:///app.db` |
| Can't connect to Redis | Leave `REDIS_URL=` empty |
| Models not loading | Run `python download_models.py` |
| Port already in use | Change port in docker-compose.yml |
| MacBook M4 slow | Use `docker-compose.m4.yml` |
| Flask commands fail | Set `export FLASK_APP=run.py` |
