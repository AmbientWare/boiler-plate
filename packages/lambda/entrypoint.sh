#!/bin/sh

# Check if FUNCTION_NAME is provided as an argument
if [ -z "$FUNCTION_NAME" ]; then
  echo "No FUNCTION_NAME environment variable provided"
  exit 1
fi

# Log which function is being run
echo "Running function $FUNCTION_NAME"

# Set the function handler
export AWS_LAMBDA_FUNCTION_HANDLER="${FUNCTION_NAME}.lambda_handler"

# Execute the AWS Lambda runtime
exec /var/runtime/bootstrap
