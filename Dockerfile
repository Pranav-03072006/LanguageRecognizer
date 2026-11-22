# ==============================================================================
# PolyGlot AI - Production Dockerfile
# Multi-stage lightweight Python container for Django + Scikit-Learn + LLM SDKs
# ==============================================================================

FROM python:3.10-slim

# Prevent Python from writing .pyc files and enable unbuffered output for live logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install system dependencies (curl for container healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Verify or generate the model artifact if not present
RUN if [ ! -f /app/artifacts/language_recognizer.joblib ]; then \
        if [ -f /app/data/language.csv ]; then \
            python train_model.py --data-path data/language.csv --output-path artifacts/language_recognizer.joblib; \
        elif [ -f /app/data/sample_dataset.csv ]; then \
            python train_model.py --data-path data/sample_dataset.csv --output-path artifacts/language_recognizer.joblib; \
        fi \
    fi

# Collect static assets for WhiteNoise
RUN python manage.py collectstatic --noinput

# Expose HTTP port
EXPOSE 8000

# Health check probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/api/health/ || exit 1

# Launch application using production Gunicorn WSGI server
CMD ["sh", "-c", "python manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2"]
