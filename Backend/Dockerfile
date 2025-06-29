FROM python:3.11.9-slim

# System packages for packet capture
RUN apt-get update && apt-get install -y --no-install-recommends \
        tcpdump \
        iproute2 \
        libpcap0.8 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create non-root user first
RUN useradd -u 1001 -m appuser

# App source
COPY --chown=appuser:appuser . .

# Drop root inside container
USER appuser

EXPOSE 8000

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]