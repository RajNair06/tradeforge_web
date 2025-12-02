FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install minimal system deps (keep if you have compiled packages)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential gcc libpq-dev ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for cache
COPY backend/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install -r /app/requirements.txt

# Copy app code into /app so main.py and db/ are siblings
COPY backend/ /app/

# Make sure /app is on Python module search path
ENV PYTHONPATH=/app

# Run as non-root (optional)
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

ENV PORT=8080
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info --access-log"]
