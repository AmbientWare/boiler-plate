#!/bin/bash

# Function to handle SIGTERM - pod shutdown
graceful_shutdown() {
    echo "SIGTERM received, shutting down gracefully..."

    # kill FastAPI application
    echo "Shutting down the Application..."
    kill $FASTAPI_PID
}

# Trap SIGTERM
trap 'graceful_shutdown' SIGTERM

# Start the FastAPI application in the background and store the process ID
echo "Starting Application..."
python main.py &
FASTAPI_PID=$! # Store the process ID of the FastAPI application
echo "Application started with PID: $FASTAPI_PID"

# Wait for all background processes to exit
wait $FASTAPI_PID
