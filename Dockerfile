# Use the official Python 3.11 image as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_HOME "/root/.local"
ENV PATH "$POETRY_HOME/bin:$PATH"

# Set the working directory in the container to /app
WORKDIR /app

# Install system dependencies required for Poetry and psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl gcc libpq-dev \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false

COPY . /app

# Install the project dependencies using Poetry
RUN poetry install --only main


# The command to run your application
CMD ["poetry", "run", "python", "app.py"]
