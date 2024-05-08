#!/bin/bash

# Function to handle SIGTERM - pod shutdown
graceful_shutdown() {
    echo "SIGTERM received, shutting down gracefully..."

    # Gracefully shut down Celery worker
    echo "Shutting down Celery..."
    celery -A app.celery_app.app.app control shutdown
    wait $CELERY_PID  # Wait for the Celery process to exit
}

# Trap SIGTERM
trap 'graceful_shutdown' SIGTERM

# Start the celery worker with auto-scaling of 1 to 100 workers in the background per pod
echo "Starting Celery app..."
celery -A app.celery_app.app.app worker --loglevel=info --autoscale=1,100 &
CELERY_PID=$! # Store the process ID of the Celery worker
echo "Celery app started with PID: $CELERY_PID"

# Wait for all background processes to exit
wait $CELERY_PID
