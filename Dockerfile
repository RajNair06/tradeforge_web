# Use an official Python runtime
FROM python:3.11-slim

# Avoid interactive prompts during builds
ENV DEBIAN_FRONTEND=noninteractive

# Workdir inside container
WORKDIR /app



# Copy only requirements first to leverage Docker cache
COPY backend/requirements.txt /app/requirements.txt

# Upgrade pip and install Python deps
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install -r /app/requirements.txt

# Copy the backend app
COPY backend/ /app/



# Default PORT (Railway will provide $PORT at runtime). Keep a default for local runs.
ENV PORT=8000

# Run uvicorn; use sh -c so $PORT is expanded
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
