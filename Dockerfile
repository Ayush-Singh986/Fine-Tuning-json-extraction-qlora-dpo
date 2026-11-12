# Base image for Finr-Tuning
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    wget \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.in .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.in

# Copy application code
COPY src/ src/
COPY configs/ configs/

# Set Python path
ENV PYTHONPATH=/app/src

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Default command
CMD ["python3", "-m", "finrtuning"]