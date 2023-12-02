# Copyright (c) 2023 Mikheil Tabidze
FROM python:3.11.6-slim-bookworm

# Set the working directory
WORKDIR /application_root

# Copy project files
COPY app ./app
COPY ai_models ./ai_models
COPY tools/healthcheck.py ./
COPY pyproject.toml poetry.lock ./

# Install the application dependencies
RUN pip install poetry && export POETRY_VIRTUALENVS_CREATE=false && poetry install --no-root --no-dev

# Expose the application port
EXPOSE 8080/tcp

# Set up a non-root user for the container
RUN addgroup --system user && adduser --system --group user

# Specify the user for the HEALTHCHECK command
HEALTHCHECK CMD python healthcheck.py "http://localhost:8080/v1/health-check/"

# Start the application
CMD ["uvicorn", "app.main:create_app", "--host", "0.0.0.0", "--port", "8080"]

# Switch to the non-root user for running the application
USER user