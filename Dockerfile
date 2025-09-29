# Base image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /RCOMMENDATION

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /application

# Expose port
EXPOSE 8080

# Run FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
