# Base image
FROM python:3.10

# Set working directory
WORKDIR /code

# Install system dependencies and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nano \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies and uWSGI
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install uwsgi

# Copy the project files
COPY . .

# Expose the port
EXPOSE 8000

# Start uWSGI
CMD ["uwsgi", "--ini", "uwsgi.ini"]