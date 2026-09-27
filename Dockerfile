FROM python:3.10-slim

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create uploads directory
RUN mkdir -p uploads && chmod 777 uploads

# Default to port 10000 (Render default)
ENV HOST=0.0.0.0
ENV PORT=10000
ENV ENVIRONMENT=production
EXPOSE 10000

# Start FastAPI server
CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port "]
