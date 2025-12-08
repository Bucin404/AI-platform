# AI Platform - Deployment Guide

## Production Deployment on Ubuntu

### Prerequisites

- Ubuntu 22.04 LTS (recommended)
- Docker and Docker Compose
- Domain name with DNS configured
- SSL certificate (Let's Encrypt recommended)
- GPU support (optional, for better AI model performance)

## Step 1: Server Setup

### Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker --version
docker-compose --version
```

### Install Nginx (Reverse Proxy)

```bash
sudo apt install nginx -y
```

## Step 2: Application Setup

### Clone Repository

```bash
cd /opt
sudo git clone https://github.com/Bucin404/AI-platform.git
cd AI-platform
```

### Configure Environment

```bash
sudo cp .env.example .env
sudo nano .env
```

Update the following for production:

```bash
# Flask
SECRET_KEY=<generate-strong-random-key>
DEBUG=False
FLASK_ENV=production

# Database
DATABASE_URL=postgresql://aiplatform:STRONG_PASSWORD@postgres:5432/aiplatform

# Email (Configure Postfix)
MAIL_SERVER=smtp.yourdomain.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=noreply@yourdomain.com
MAIL_PASSWORD=your-email-password
MAIL_DEFAULT_SENDER=noreply@yourdomain.com

# Midtrans (Production)
MIDTRANS_SERVER_KEY=your-production-server-key
MIDTRANS_CLIENT_KEY=your-production-client-key
MIDTRANS_IS_PRODUCTION=True

# Security
SESSION_COOKIE_SECURE=True
```

### Update docker-compose.yml for Production

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: aiplatform_postgres
    environment:
      POSTGRES_USER: aiplatform
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: aiplatform
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - aiplatform_network
    restart: always

  redis:
    image: redis:7-alpine
    container_name: aiplatform_redis
    volumes:
      - redis_data:/data
    networks:
      - aiplatform_network
    restart: always

  web:
    build: .
    container_name: aiplatform_web
    command: gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 run:app
    volumes:
      - ./models:/app/models
      - ./uploads:/app/uploads
    environment:
      - FLASK_ENV=production
    env_file:
      - .env
    depends_on:
      - postgres
      - redis
    networks:
      - aiplatform_network
    restart: always

networks:
  aiplatform_network:
    driver: bridge

volumes:
  postgres_data:
  redis_data:
```

## Step 3: Nginx Configuration

### Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/aiplatform
```

Add the following configuration:

```nginx
upstream aiplatform {
    server localhost:5000;
}

# HTTP to HTTPS redirect
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # Max upload size
    client_max_body_size 100M;

    # Proxy settings
    location / {
        proxy_pass http://aiplatform;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
        proxy_buffering off;
    }

    # WebSocket support (if needed)
    location /ws {
        proxy_pass http://aiplatform;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # Static files (if serving directly)
    location /static {
        alias /opt/AI-platform/app/static;
        expires 30d;
    }
}
```

### Enable Site and Restart Nginx

```bash
sudo ln -s /etc/nginx/sites-available/aiplatform /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 4: SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

## Step 5: Deploy Application

```bash
cd /opt/AI-platform

# Build and start containers
sudo docker-compose up -d --build

# Initialize database
sudo docker-compose exec web flask db upgrade

# Create admin user
sudo docker-compose exec web flask create-admin
```

## Step 6: Configure Postfix (Email)

### Install Postfix

```bash
sudo apt install postfix -y
# Select "Internet Site" during installation
```

### Configure Postfix

```bash
sudo nano /etc/postfix/main.cf
```

Add/modify:

```
myhostname = yourdomain.com
mydestination = yourdomain.com, localhost
relayhost =
inet_interfaces = all
```

### Restart Postfix

```bash
sudo systemctl restart postfix
sudo systemctl enable postfix
```

## Step 7: GPU Support (Optional)

### Install NVIDIA Docker Runtime

```bash
# Install NVIDIA drivers
sudo apt install nvidia-driver-525 -y

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt update && sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Update docker-compose.yml for GPU

```yaml
web:
  # ... other config ...
  deploy:
    resources:
      reservations:
        devices:
          - driver: nvidia
            count: 1
            capabilities: [gpu]
```

## Step 8: Backup Strategy

### Database Backup Script

```bash
sudo nano /opt/backup-db.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/backup/postgres"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
docker exec aiplatform_postgres pg_dump -U aiplatform aiplatform > $BACKUP_DIR/backup_$DATE.sql
find $BACKUP_DIR -type f -mtime +7 -delete
```

### Schedule Backup (Cron)

```bash
sudo chmod +x /opt/backup-db.sh
sudo crontab -e

# Add line for daily backup at 2 AM
0 2 * * * /opt/backup-db.sh
```

## Step 9: Monitoring

### Health Check Endpoint

Application provides `/api/health` endpoint for monitoring.

### Prometheus Integration (Optional)

```bash
# Add prometheus exporter to docker-compose.yml
prometheus:
  image: prom/prometheus
  volumes:
    - ./prometheus.yml:/etc/prometheus/prometheus.yml
  ports:
    - "9090:9090"
```

### Basic Monitoring Script

```bash
#!/bin/bash
# monitor.sh - Simple health check
curl -f http://localhost:5000/api/health || echo "Service is down!" | mail -s "AI Platform Alert" admin@yourdomain.com
```

## Step 10: Load Balancer (Optional)

For high-traffic deployments, use Nginx as a load balancer:

```nginx
upstream aiplatform {
    least_conn;
    server server1:5000;
    server server2:5000;
    server server3:5000;
}
```

## Maintenance

### View Logs

```bash
docker-compose logs -f web
docker-compose logs -f postgres
docker-compose logs -f redis
```

### Update Application

```bash
cd /opt/AI-platform
sudo git pull
sudo docker-compose down
sudo docker-compose up -d --build
sudo docker-compose exec web flask db upgrade
```

### Restart Services

```bash
sudo docker-compose restart web
```

## Security Checklist

- [ ] Strong SECRET_KEY set
- [ ] Database password changed from default
- [ ] Admin password changed
- [ ] SSL certificate installed
- [ ] Firewall configured (UFW)
- [ ] Regular backups scheduled
- [ ] Security headers configured in Nginx
- [ ] Rate limiting enabled
- [ ] CSRF protection enabled
- [ ] SSH key authentication only
- [ ] Fail2ban installed and configured

## Troubleshooting

### Check Service Status

```bash
sudo docker-compose ps
sudo systemctl status nginx
```

### View Detailed Logs

```bash
sudo docker-compose logs --tail=100 web
```

### Database Connection Issues

```bash
sudo docker-compose exec postgres psql -U aiplatform -d aiplatform
```

## Performance Tuning

### Gunicorn Workers

Adjust workers in docker-compose.yml:

```yaml
command: gunicorn -w 8 -b 0.0.0.0:5000 --timeout 120 run:app
# Formula: (2 x CPU cores) + 1
```

### PostgreSQL Tuning

Update PostgreSQL configuration for better performance based on your server specs.

## Support

For issues and support:
- GitHub Issues: https://github.com/Bucin404/AI-platform/issues
- Documentation: https://github.com/Bucin404/AI-platform/tree/main/docs
