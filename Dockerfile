# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set up a working directory
WORKDIR /app

# Install necessary packages
RUN apt-get update && \
    apt-get install -y curl procps && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -L https://ollama.com/install.sh | sh && \
    mkdir -p /root/.ollama

# Verify Ollama installation and download model
RUN ollama --version && \
    OLLAMA_HOST=0.0.0.0:11434 ollama serve > /var/log/ollama.log 2>&1 & \
    sleep 15 && \
    ollama pull mistral && \
    pkill ollama

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Pre-download the OpenJourney model
RUN python download_models.py

# Start Ollama service and run the application
RUN chmod +x start.sh

# Run the start script
CMD ["./start.sh"]