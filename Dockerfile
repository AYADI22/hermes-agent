FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV HERMES_HOME=/opt/data

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml .
COPY . .

RUN pip install --no-cache-dir -e ".[core]" || \
    pip install --no-cache-dir -e "."

RUN mkdir -p /opt/data

CMD ["python", "-m", "hermes_cli.gateway"]
