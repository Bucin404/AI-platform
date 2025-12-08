# Dockerfile optimized for MacBook M4 (Apple Silicon ARM64)
# Includes Metal acceleration support for AI models

ARG PYTHON_VERSION=3.11
FROM --platform=linux/arm64 python:${PYTHON_VERSION}-slim

WORKDIR /app

# Install system dependencies optimized for ARM64
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    cmake \
    git \
    curl \
    postgresql-client \
    libpq-dev \
    # For llama-cpp-python compilation
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .

# Install Python packages
# Note: llama-cpp-python with Metal support should be installed separately
# because it requires specific build flags that work on the host Mac
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install development tools for hot-reload
RUN pip install --no-cache-dir watchdog

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/models /app/uploads /app/instance

# Set environment variables for ARM64 optimization
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Enable Metal acceleration for AI models (when running on Mac)
ENV GGML_METAL=1
ENV LLAMA_METAL=1

# Expose port
EXPOSE 5000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Development mode by default (override in docker-compose)
CMD ["python", "run.py"]
