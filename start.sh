#!/bin/bash
# Start ollama in the background
ollama serve &

# Wait for ollama to be ready
sleep 5

# Run the main application
python main.py