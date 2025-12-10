# Dockerfile for building the application on Raspberry Pi
# Use: docker build -t faciee-rpi -f docker_rpi.dockerfile .
# Run: docker run --rm -it --device /dev/video0 faciee-rpi

FROM arm32v7/python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies for Raspberry Pi
RUN apt-get update && apt-get install -y \
    libopenblas0 \
    libatlas-base-dev \
    libjasper-dev \
    libtiff5 \
    libjasper1 \
    libharfbuzz0b \
    libwebp6 \
    libopenjp2-7 \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    python3-gst-1.0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_rpi.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_rpi.txt

# Copy application
COPY Recunostere ./Recunostere
COPY assets ./assets

# Set environment variables
ENV DISPLAY=:0
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python3", "Recunostere/main.py"]
