FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the simulator code
COPY simulator.py /app/

# Run the simulator
CMD ["python", "simulator.py"]