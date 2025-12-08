# AI Platform

Full-stack AI chat platform with intelligent model routing built with Flask, Tailwind CSS, and open-source AI models.

## Features

### 🤖 Intelligent Model Routing
- **DeepSeek Coder**: Specialized for coding, debugging, and programming tasks
- **Llama.cpp**: Optimized for document processing, PDFs, and large files
- **Vicuna**: Multimodal AI for images, videos, and rich media content
- **GPT4All**: General-purpose conversational AI for everyday tasks
- **Auto-Select**: Automatically routes queries to the best model based on content type

### ✨ Core Features
- User authentication with registration, login, and password reset
- Rate limiting by tier (Free: 10/hour, Premium: 100/hour, Admin: 1000/hour)
- Chat history with message persistence
- Admin panel for user management and analytics
- Payment integration with Midtrans
- Email notifications via Postfix SMTP
- Dark/light mode toggle
- Markdown rendering with code syntax highlighting
- RESTful API for programmatic access

### 🛡️ Security
- CSRF protection
- Secure password hashing (Werkzeug)
- Session management with secure cookies
- Rate limiting (Redis-backed)
- Input sanitization
- Security headers (CSP, X-Frame-Options, etc.)

## Quick Start

### Using Docker (Recommended)

```bash
# Clone repository
git clone https://github.com/Bucin404/AI-platform.git
cd AI-platform

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Download AI models (optional, uses mock by default)
python download_models.py

# Start services
docker-compose up -d

# Initialize database
docker-compose exec web flask db upgrade

# Create admin user
docker-compose exec web flask create-admin

# Access at http://localhost:5000
```

### Using Docker on MacBook M4 (Apple Silicon)

```bash
# Use M4-optimized configuration
docker-compose -f docker-compose.m4.yml up -d

# Initialize database
docker-compose -f docker-compose.m4.yml exec web flask db upgrade

# Create admin user
docker-compose -f docker-compose.m4.yml exec web flask create-admin

# See full M4 setup guide: docs/SETUP_M4.md
```

### Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Download AI models (optional)
python download_models.py --lite  # Use --lite for smaller models

# Initialize database
export FLASK_APP=run.py
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Create admin user
flask create-admin

# Run application
python run.py
```

## Documentation

- [Installation Guide](docs/INSTALL.md) - Detailed installation instructions
- [MacBook M4 Setup](docs/SETUP_M4.md) - Optimized setup for Apple Silicon (NEW)
- [Model Download Guide](docs/MODELS.md) - How to download and configure AI models
- [Deployment Guide](docs/DEPLOY.md) - Production deployment on Ubuntu
- [API Documentation](docs/API.md) - REST API reference

## Tech Stack

**Backend:**
- Flask (Python web framework)
- PostgreSQL (Database)
- Redis (Caching & rate limiting)
- SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Flask-WTF (Forms & CSRF)
- Flask-Mail (Email)
- Flask-Limiter (Rate limiting)
- Flask-Migrate (Database migrations)

**Frontend:**
- Tailwind CSS (Styling)
- Vanilla JavaScript
- Marked.js (Markdown rendering)
- Highlight.js (Code syntax highlighting)

**AI Models:**
- DeepSeek Coder
- Llama.cpp
- Vicuna
- GPT4All

**Infrastructure:**
- Docker & Docker Compose
- Nginx (Reverse proxy)
- Postfix (Email)
- Midtrans (Payments)

## Project Structure

```
AI-platform/
├── app/
│   ├── blueprints/          # Flask blueprints
│   │   ├── auth/            # Authentication routes
│   │   ├── chat/            # Chat routes
│   │   ├── admin/           # Admin panel routes
│   │   ├── payments/        # Payment routes
│   │   └── api/             # API routes
│   ├── models/              # Database models
│   ├── services/            # Business logic services
│   │   ├── model_service.py # AI model adapters
│   │   ├── email_service.py # Email service
│   │   └── payment_service.py # Payment service
│   ├── templates/           # HTML templates
│   ├── static/              # Static files (CSS, JS)
│   └── utils/               # Utility functions
├── tests/                   # Unit tests
├── docs/                    # Documentation
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── Dockerfile               # Docker configuration
└── docker-compose.yml       # Docker Compose configuration
```

## Environment Variables

See `.env.example` for all required environment variables. Key variables:

```bash
# Flask
SECRET_KEY=your-secret-key
DEBUG=False

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/aiplatform

# Redis
REDIS_URL=redis://localhost:6379/0

# Email (Postfix)
MAIL_SERVER=localhost
MAIL_PORT=587
MAIL_USERNAME=
MAIL_PASSWORD=

# Midtrans Payment
MIDTRANS_SERVER_KEY=your-server-key
MIDTRANS_CLIENT_KEY=your-client-key
MIDTRANS_IS_PRODUCTION=False

# Admin
ADMIN_EMAIL=admin@aiplatform.com
ADMIN_PASSWORD=changeme
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py
```

## API Usage

```python
import requests

# Login
session = requests.Session()
session.post('http://localhost:5000/auth/login', data={
    'email': 'user@example.com',
    'password': 'password'
})

# Send chat message with auto model selection
response = session.post('http://localhost:5000/api/chat', json={
    'message': 'Write a Python function to sort a list',
    'model': 'auto'  # Will automatically use DeepSeek for coding
})

print(response.json())
```

## Model Routing Logic

The platform intelligently routes queries based on content detection:

| Query Type | Model | Example Keywords |
|-----------|-------|------------------|
| Coding | DeepSeek Coder | code, function, debug, python, javascript |
| Documents | Llama.cpp | pdf, document, file, csv |
| Images/Videos | Vicuna | image, photo, video, analyze |
| General | GPT4All | weather, explain, tell me |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Support

- GitHub Issues: https://github.com/Bucin404/AI-platform/issues
- Email: support@aiplatform.com

## Credits

Built with ❤️ using open-source AI models and modern web technologies.