# Use official Python 3.11 slim image
FROM python:3.11-slim 

# Set environmental variables to prevent python from writeing .pyc files and enable buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install system dependencies (PosgreSQL client + build tools)
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get install -y postgresql-client && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . .

# Wait scripts
COPY wait-for-service.sh /wait-for-service.sh 
RUN chmod +x /wait-for-service.sh

# Expose the port the app will run on
EXPOSE 5000

# Default command: run Gunicorn with configs
CMD ["gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]