FROM docker.io/python:3.9-slim

ENV PATH "/root/.local/bin:$PATH"

ENV AIRCON_HOSTS "aircon1.local aircon2.local"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/* && \
    curl -sSL https://install.python-poetry.org | python3 - --version 1.4.2

COPY app.py poetry.lock pyproject.toml .

RUN poetry install --no-dev

CMD ["poetry", "run", "python", "app.py"]
