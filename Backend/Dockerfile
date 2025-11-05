FROM python:3.11.9-slim

WORKDIR /app

# System packages for packet capture
RUN apt-get update && apt-get install -y --no-install-recommends \
        tcpdump \
        iproute2 \
        libpcap0.8 \
        curl \
        postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY Backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user first
RUN useradd -u 1001 -m appuser

# Ap    p source
COPY --chown=appuser:appuser . .

# Drop root inside container
USER appuser

ENV PYTHONPATH=/app

EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the ASGI server
CMD ["uvicorn", "Backend.rest.rest_main:app", "--host", "0.0.0.0", "--port", "8000"]