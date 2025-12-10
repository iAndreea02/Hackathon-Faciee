FROM arm32v7/python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (libcamera + OpenCV + Pygame)
RUN apt-get update && apt-get install -y \
    libcamera-dev \
    libcamera-tools \
    libopencv-dev \
    python3-opencv \
    libatlas-base-dev \
    libjasper-dev \
    libtiff5 \
    libharfbuzz0b \
    libwebp6 \
    libopenjp2-7 \
    libfreetype6-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements_rpi.txt .
RUN pip install --no-cache-dir -r requirements_rpi.txt

# Copy application code
COPY Recunostere/ /app/Recunostere/
COPY assets/ /app/assets/

# Set environment variables for libcamera
ENV LIBCAMERA_LOG_LEVELS=*:WARN

# Run the application
CMD ["python3", "Recunostere/main.py"]
