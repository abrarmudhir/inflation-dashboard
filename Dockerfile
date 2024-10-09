FROM python:3.12.4-slim-bookworm as dependencies

ARG PROJECT_DIR=.
ARG POETRY_VERSION=1.8.3

RUN useradd --create-home app

ENV POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=${POETRY_VERSION}

# Update pip
RUN pip install --upgrade pip

# Install poetry
COPY install-poetry.py .
RUN python ./install-poetry.py
ENV PATH="$PATH:$POETRY_HOME/bin"


COPY ${PROJECT_DIR}/pyproject.toml ${PROJECT_DIR}/poetry.lock ./


RUN poetry install --no-root --no-cache --no-interaction --no-ansi

COPY ${PROJECT_DIR}/app ./app

RUN poetry install --only main

EXPOSE 8050
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8050", "--proxy-headers", "--forwarded-allow-ips", "*"]