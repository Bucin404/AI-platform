# AI Platform - Installation Guide

## Prerequisites

- Docker and Docker Compose (recommended)
- Python 3.11+ (for local development without Docker)
- PostgreSQL 15+ (if not using Docker)
- Redis (optional, for rate limiting)

## Quick Start with Docker (Recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/Bucin404/AI-platform.git
cd AI-platform
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Start Services

```bash
docker-compose up -d
```

### 4. Initialize Database

```bash
docker-compose exec web flask db init
docker-compose exec web flask db migrate -m "Initial migration"
docker-compose exec web flask db upgrade
```

### 5. Create Admin User

```bash
docker-compose exec web flask create-admin
```

### 6. Access the Application

Open your browser and navigate to `http://localhost:5000`

Default admin credentials:
- Email: admin@aiplatform.com
- Password: changeme (change this immediately!)

## Local Development Setup (Without Docker)

**⚠️ IMPORTANT:** When running locally (not in Docker), you need to:
1. Use `.env.local.example` instead of `.env.example` 
2. Use `localhost` instead of Docker service names (`postgres`, `redis`)
3. Have PostgreSQL running locally, OR use SQLite for simplicity

**Quick SQLite Setup (Easiest):**
```bash
cp .env.local.example .env
# Edit .env and set: DATABASE_URL=sqlite:///app.db
```

**For issues, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)**

### 1. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Database

**Option A: Use SQLite (Easiest, no setup required)**
```bash
# In .env file:
DATABASE_URL=sqlite:///app.db
```

**Option B: Use PostgreSQL**

First, install and start PostgreSQL:

**On macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**On Ubuntu:**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

Then create the database:
```bash
# macOS
createdb aiplatform

# Ubuntu
sudo -u postgres createdb aiplatform
```

**Important:** Update .env with **localhost**, not 'postgres':
```bash
# ✅ Correct for local development
DATABASE_URL=postgresql://yourusername:yourpassword@localhost:5432/aiplatform

# ❌ Wrong - this is for Docker only
# DATABASE_URL=postgresql://aiplatform:aiplatform@postgres:5432/aiplatform
```

### 4. Set Up Redis (Optional)

```bash
# Install and start Redis
# On macOS: brew install redis && brew services start redis
# On Ubuntu: sudo apt-get install redis-server

# Update .env
REDIS_URL=redis://localhost:6379/0
```

### 5. Initialize Database

```bash
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Create Admin User

```bash
flask create-admin
```

### 7. Run Development Server

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## ⚠️ Troubleshooting

Having issues? See **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** for solutions to common problems:

- Database connection errors
- Redis connection errors  
- Model loading issues
- Port conflicts
- Permission errors
- And more...

## Environment Configuration

### Environment Files

**For Docker:** Use `.env.example`
```bash
cp .env.example .env
# Uses 'postgres' and 'redis' service names
```

**For Local Development:** Use `.env.local.example`
```bash
cp .env.local.example .env
# Uses 'localhost' or SQLite
```

### Required Environment Variables

**For Docker (.env.example):**

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-change-in-production
DEBUG=False

# Database - uses Docker service name 'postgres'
DATABASE_URL=postgresql://aiplatform:aiplatform@postgres:5432/aiplatform

# Redis - uses Docker service name 'redis'
REDIS_URL=redis://redis:6379/0

# Email (Postfix SMTP)
MAIL_SERVER=localhost
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=noreply@aiplatform.com

# Midtrans Payment
MIDTRANS_SERVER_KEY=your-midtrans-server-key
MIDTRANS_CLIENT_KEY=your-midtrans-client-key
MIDTRANS_IS_PRODUCTION=False

# Rate Limiting
RATE_LIMIT_FREE_TIER=10
RATE_LIMIT_PREMIUM_TIER=100
RATE_LIMIT_ADMIN_TIER=1000

# Admin
ADMIN_EMAIL=admin@aiplatform.com
ADMIN_PASSWORD=change-this-password
```

**For Local Development (.env.local.example):**

```bash
# Use localhost for database and redis
DATABASE_URL=postgresql://aiplatform:aiplatform@localhost:5432/aiplatform
# Or use SQLite (no PostgreSQL required):
# DATABASE_URL=sqlite:///app.db

REDIS_URL=redis://localhost:6379/0
# Or leave empty for in-memory rate limiting:
# REDIS_URL=
```

## Database Migrations

### Create New Migration

```bash
flask db migrate -m "Description of changes"
```

### Apply Migrations

```bash
flask db upgrade
```

### Rollback Migration

```bash
flask db downgrade
```

## Model Configuration

### Automatic Model Download (Recommended)

Use the provided download script to automatically download all required models:

```bash
# Download all standard models (~16 GB)
python download_models.py

# OR download lite versions (~1.6 GB) for limited resources
python download_models.py --lite

# OR download specific models only
python download_models.py --models deepseek-coder gpt4all
```

**See [docs/MODELS.md](MODELS.md) for complete model documentation.**

### Manual Model Download

If you prefer to download manually:

1. Download model files from sources listed in `models_config.py`
2. Place them in the `models/` directory
3. Update `app/services/model_service.py` to configure model paths
4. Restart the application

### Supported Models

- **DeepSeek Coder**: For coding and programming tasks
- **Llama 2**: For documents and large files
- **Vicuna**: For images and videos
- **GPT4All**: For general chat

**Available in both standard (7B parameters) and lite (1-2B parameters) versions.**

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres
```

### Redis Connection Issues

```bash
# Check Redis is running
docker-compose ps redis

# Test connection
redis-cli ping
```

### Application Errors

```bash
# View application logs
docker-compose logs web

# Access container shell
docker-compose exec web sh
```

### Port Conflicts

If port 5000 is already in use, modify `docker-compose.yml`:

```yaml
ports:
  - "8000:5000"  # Change host port
```

## Testing

### Run Tests

```bash
# With Docker
docker-compose exec web pytest

# Local
pytest

# With coverage
pytest --cov=app tests/
```

## Next Steps

- [Deployment Guide](DEPLOY.md)
- [API Documentation](API.md)
- Configure email settings for production
- Set up Midtrans payment gateway
- Configure GPU support for AI models
