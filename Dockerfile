# --- Stage 1: Builder ---
FROM python:3.12-slim AS builder

ARG UV_VERSION=0.9.25

ENV PATH="/root/.local/bin:$PATH" \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /build

# Install uv (add/remove curl which is required)
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && curl -LsSf https://astral.sh/uv/${UV_VERSION}/install.sh | sh \
    && apt-get purge -y curl \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependency configuration
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev

# Copy application code and install as package
COPY ./app ./app
RUN uv sync --frozen --no-dev


# --- Stage 2: Runtime ---
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Security: Non-root user
RUN groupadd -g 10001 appuser && \
    useradd -u 10000 -g appuser appuser

# Copy only venv and app from the builder
COPY --from=builder --chown=appuser:appuser /build/.venv /app/.venv
COPY --from=builder --chown=appuser:appuser /build/app /app/app

# Copy the pre-seeded database
COPY --chown=appuser:appuser ./data /app/data

USER appuser
EXPOSE 8000

# Start the application
CMD ["python", "-m", "app"]
