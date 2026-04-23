FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV HERMES_HOME=/opt/data

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential git curl nodejs npm && \
    rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /usr/local/bin/uv /usr/local/bin/uv

WORKDIR /opt/hermes

COPY pyproject.toml ./
RUN uv pip install --system --no-cache -e "." 2>/dev/null || \
    pip install --no-cache-dir -e "." 

COPY . .

RUN mkdir -p /opt/data

CMD ["python", "-m", "hermes_cli.gateway"]
