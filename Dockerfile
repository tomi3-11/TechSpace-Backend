# Use official Python 3.11 slim image
FROM python:3.11-slim

# Prevent python from writing .pyc files and enable buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

COPY requirements.txt .
RUN apt-get update && \
    apt-get install -y gcc libpq-dev postgresql-client redis-tools curl && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Copy wait script and make it executable
COPY wait-for-service.sh /wait-for-service.sh
RUN chmod +x /wait-for-service.sh

# Expose application port
EXPOSE 5000

# Entrypoint runs the wait script before starting the app
ENTRYPOINT ["/wait-for-service.sh"]

# CMD runs Gunicorn once services are ready
CMD ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]
