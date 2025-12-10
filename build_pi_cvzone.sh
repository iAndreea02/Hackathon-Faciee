#!/bin/bash
# Build script for Raspberry Pi 4 with CVZone (optimized, no MediaPipe)
# Run this on your Raspberry Pi

echo "🎮 Building for Raspberry Pi 4 with CVZone..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python 3 and pip
echo "🐍 Installing Python 3..."
sudo apt-get install -y python3 python3-pip python3-venv

# Create virtual environment
echo "🔧 Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install libcamera (for Pi camera module)
echo "📷 Installing libcamera dependencies..."
sudo apt-get install -y libcamera-dev libcamera-tools

# Install OpenCV dependencies
echo "📚 Installing OpenCV dependencies..."
sudo apt-get install -y libatlas-base-dev libjasper-dev libtiff5 libjasper1 libharfbuzz0b libwebp6 libtiff5 libjasper1 libharfbuzz0b libwebp6 libopenjp2-7 libtiff5-dev zlib1g-dev

# Install Pygame dependencies
echo "🎮 Installing Pygame dependencies..."
sudo apt-get install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev

# Install Python requirements
echo "📥 Installing Python packages from requirements_rpi.txt..."
pip install -r requirements_rpi.txt

echo "✅ Build complete! Your Raspberry Pi is ready to run the app."
echo "Run: source venv/bin/activate && python3 Recunostere/main.py"
