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

# Copy the built Python package distributions from the dist/ directory
COPY --from=backend /app/packages/backend/dist /app/packages/backend/dist
# copy the run file from the local backend directory
COPY packages/backend/worker_entrypoint.sh /app/packages/backend/worker_entrypoint.sh

# Install the built Python package
WORKDIR /app/packages/backend
RUN pip install dist/*.whl

# Set the working directory to where your CMD will be executed
WORKDIR /app/packages/backend

# Define the command to run your application
CMD ["./worker_entrypoint.sh"]
