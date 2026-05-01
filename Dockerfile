# Quran Reel Maker - Dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    imagemagick \
    fonts-noto \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY Telegram_Bot/ ./Telegram_Bot/
COPY Web_Dashboard/ ./Web_Dashboard/
COPY Assets/ ./Assets/

# Create data directories
RUN mkdir -p data/videos data/vision data/temp data/cache

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Expose port
EXPOSE 7860

# Default command (runs bot by default)
CMD ["python", "Telegram_Bot/bot_quran_v1.py"]