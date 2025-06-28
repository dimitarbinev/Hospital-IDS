FROM python:3.11.9-slim

# System packages for packet capture
RUN apt-get update && apt-get install -y --no-install-recommends \
        tcpdump iproute2 libpcap0.8 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App source
COPY . .

# Drop root inside container
RUN useradd -u 1001 -m appuser
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]