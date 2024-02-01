FROM python:3.11-slim-bullseye
# Intentionally do not include the patch version pinning to allow newer pathes to be introduced
ARG PROJECT_NAME=example_dbt_airflow

RUN mkdir /app

RUN groupadd -r appuser && useradd -r -s /bin/false -g appuser appuser

RUN python3 -m pip install --upgrade pip poetry

# No need for a virtual environment when the container is it's own isolated environment.
RUN poetry config virtualenvs.create false
WORKDIR /app

# Copy over bare minimum files for poetry to install
COPY pyproject.toml .
COPY poetry.lock .
COPY "./src/${PROJECT_NAME}/__init__.py" "/app/${PROJECT_NAME}/__init__.py"
COPY README.md .

# Install dependencies
RUN poetry install --only main
# List folder contents in build process as a sanity check
RUN ls -la


COPY "./src/${PROJECT_NAME}/" "/app/${PROJECT_NAME}/"
# List folder contents in build process as a sanity check
RUN ls -la
RUN ls -la "${PROJECT_NAME}/"

# NOTE: Why Your Dockerized Application Isn’t Receiving Signals
# https://hynek.me/articles/docker-signals/
ENTRYPOINT exec hypercorn ${PROJECT_NAME}.app:app --bind '0.0.0.0:5000' --keep-alive 60 --log-level info
