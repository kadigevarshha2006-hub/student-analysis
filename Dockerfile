FROM python:3.10-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt

# Copy project files
COPY . .

# Create uploads directory
RUN mkdir -p uploads && chmod 777 uploads

# Expose port (default 7860 for Hugging Face Spaces, 8000 for standard)
ENV HOST=0.0.0.0
ENV PORT=7860
ENV ENVIRONMENT=production
EXPOSE 7860 8000

# Start FastAPI server
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
