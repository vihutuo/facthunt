# Dockerfile — optimized for Flet on Fly (fast cold starts)
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install system dependencies needed for building wheels (only if you need them)
# Remove build-essential if all packages have wheels available.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies at build time (fast, deterministic).
COPY requirements.txt ./
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY . .

# Create a non-root user and chown the app dir (optional, avoids pip-as-root warnings at runtime)
RUN useradd --create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Run the application
CMD ["python", "main.py"]
