# Use the official AWS Lambda Python runtime as the base image
FROM public.ecr.aws/lambda/python:3.11 as base
# FROM python:3.11-slim as base

# make lambda directory
RUN mkdir /lambda

# Set non-interactive frontend during docker build
ENV DEBIAN_FRONTEND=noninteractive

# Set python/poetry environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_NO_INTERACTION 1
# Disable poetry's virtual environment creation
ENV POETRY_VENV_CREATE false

# Install system dependencies and clean up in one layer to keep image small
RUN apt-get update && apt-get install -y --no-install-recommends \
    pipx \
    python3-venv \
    && pipx ensurepath \
    && pipx install poetry \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ensure pipx bin directory is in PATH
ENV PATH="/root/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1

WORKDIR /lambda

# copy the main directory
COPY packages/lambda/functions/ .

# copy over poetry and pyproject.toml related files
COPY ./packages/lambda/pyproject.toml .
COPY ./packages/lambda/poetry.lock .
COPY ./packages/lambda/README.md .

# Build the Python package using poetry
RUN poetry config virtualenvs.create false && poetry install --only main

# Activate the virtual environment
ENV PYTHONPATH "${PYTHONPATH}:/"

# Copy the entrypoint script
COPY ./packages/lambda/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
