# syntax=docker/dockerfile:1

FROM python:3.11-slim AS base

# Set working directory
WORKDIR /app

FROM base AS builder

# Install build dependencies (if any needed, e.g. gcc, for native extensions)
# For now, we skip as requirements.txt is empty and no info on native deps

# Copy requirements.txt separately for better cache usage
COPY --link requirements.txt ./

# Create virtual environment and install dependencies
RUN python -m venv .venv \
    && .venv/bin/pip install --upgrade pip \
    && --mount=type=cache,target=/root/.cache/pip \
       .venv/bin/pip install -r requirements.txt

# Copy application code
COPY --link Rest ./Rest
COPY --link main.py ./main.py

FROM base AS final

# Create non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code from builder
COPY --from=builder /app/Rest ./Rest
COPY --from=builder /app/main.py ./main.py

# Set environment so venv is used
ENV PATH="/app/.venv/bin:$PATH"

USER appuser

# Expose port (FastAPI default is 8000)
EXPOSE 8000

# Start FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
