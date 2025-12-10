#!/bin/bash
# Setup script for Raspberry Pi 4
# Run this on your Raspberry Pi to install dependencies

echo "📦 Installing system dependencies for Raspberry Pi..."

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Python and pip
sudo apt-get install -y python3 python3-pip python3-dev

# OpenCV dependencies
sudo apt-get install -y \
    libjasper-dev \
    libtiff5 \
    libjasper1 \
    libharfbuzz0b \
    libwebp6 \
    libtiff5 \
    libjasper1 \
    libatlas-base-dev \
    libjasper-dev \
    libharfbuzz0b \
    libwebp6 \
    libopenjp2-7 \
    libtiff5 \
    libjasper1

# Pygame dependencies
sudo apt-get install -y \
    python3-pygame

# CVZone dependencies (lighter alternative to MediaPipe for hand/face detection)
sudo apt-get install -y \
    libatlas-base-dev \
    libjasper-dev \
    libtiff5 \
    libharfbuzz0b \
    libwebp6 \
    libopenjp2-7 \
    libfreetype6-dev

# GStreamer for camera (libcamera)
sudo apt-get install -y \
    libgstreamer1.0-0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-plugins-bad \
    python3-gst-1.0

echo "📦 Installing Python packages..."

# Create virtual environment (optional but recommended)
python3 -m venv ~/faciee_env
source ~/faciee_env/bin/activate

# Install Python dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements_rpi.txt

echo "✅ Setup complete! Your Raspberry Pi is ready to run the application."
echo "📝 Next steps:"
echo "   1. Clone/copy your project to the Pi"
echo "   2. Run: source ~/faciee_env/bin/activate"
echo "   3. Run: python3 main.py"
