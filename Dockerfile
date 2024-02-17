# first stage: build the frontend application
FROM node:21 as frontend

# Set the working directory for the build process
WORKDIR /app

# copy the frontend directory
COPY packages/frontend /app/packages/frontend

# Build the frontend
WORKDIR /app/packages/frontend
RUN yarn install && yarn build

# second stage: build the python builder image
FROM python:3.11-slim as builder

# no interactive frontend during docker build
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and clean up in one layer to keep image small
RUN apt-get update && apt-get install -y --no-install-recommends \
    pipx \
    && pipx ensurepath \
    && pipx install poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ensure pipx bin directory is in PATH
ENV PATH="/root/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1

# third stage: build the backend application
FROM builder as backend

# copy the backend directory
COPY packages/backend /app/packages/backend

# Build the Python package using poetry
WORKDIR /app/packages/backend
RUN poetry install --no-dev && poetry build

# final stage: prepare the runtime image
FROM builder as runtime

# Ensure pipx bin directory is in PATH
ENV PATH="/root/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1

# Set up environment variables
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Set the working directory
WORKDIR /app

# Copy only the necessary artifacts from the frontend stage
COPY --from=frontend /app/packages/frontend/dist /app/packages/frontend/dist
# Copy the built Python package distributions from the dist/ directory
COPY --from=backend /app/packages/backend/dist /app/packages/backend/dist
# copy the run file from the local backend directory
COPY packages/backend/main.py /app/packages/backend/main.py

# Install the built Python package
WORKDIR /app/packages/backend
RUN pip install dist/*.whl

# Set the working directory to where your CMD will be executed
WORKDIR /app/packages/backend

# Define the command to run your application
CMD ["python", "main.py"]
