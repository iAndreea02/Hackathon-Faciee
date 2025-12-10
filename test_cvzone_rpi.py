#!/usr/bin/env python3
"""
Quick test script for CVZone on Raspberry Pi
Tests: Hand detection, Face detection, and camera
"""

import cv2
import sys
import time
from hands.hand_detector import HandDetector
from face.face_processor import FaceProcessor

print("🚀 CVZone Test Suite for Raspberry Pi")
print("=" * 50)

# Test 1: Import test
print("\n✅ Testing imports...")
try:
    from cvzone.HandTrackingModule import HandDetector as CVZHandDetector
    from cvzone.FaceDetectionModule import FaceDetector
    print("   ✓ CVZone imports OK")
except ImportError as e:
    print(f"   ✗ CVZone import failed: {e}")
    sys.exit(1)

# Test 2: Initialize detectors
print("\n✅ Initializing detectors...")
try:
    hands = HandDetector(max_hands=2)
    faces = FaceProcessor()
    print("   ✓ Hand detector initialized")
    print("   ✓ Face detector initialized")
except Exception as e:
    print(f"   ✗ Detector initialization failed: {e}")
    sys.exit(1)

# Test 3: Camera test
print("\n✅ Testing camera...")
try:
    cap = cv2.VideoCapture(0)  # Try USB camera first
    if not cap.isOpened():
        print("   ⚠ USB camera not found, trying GStreamer...")
        gst_pipeline = (
            "libcamerasrc ! "
            "video/x-raw, width=640, height=480, framerate=30/1 ! "
            "videoconvert ! "
            "video/x-raw, format=BGR ! "
            "appsink drop=1"
        )
        cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
    
    if not cap.isOpened():
        print("   ✗ No camera found!")
        sys.exit(1)
    
    ret, frame = cap.read()
    if ret:
        print(f"   ✓ Camera working! Frame size: {frame.shape}")
    else:
        print("   ✗ Cannot read from camera")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ Camera test failed: {e}")
    sys.exit(1)

# Test 4: Detection test (10 frames)
print("\n✅ Testing detection (10 frames)...")
try:
    frame_count = 0
    fps_list = []
    
    while frame_count < 10:
        start = time.time()
        
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.resize(frame, (320, 240))
        
        # Test hand detection
        hand_data = hands.detect(frame)
        biggest_hand = hands.get_biggest_hand(hand_data)
        gesture = hands.classify_gesture(biggest_hand)
        
        # Test face detection
        face_bbox, frame_with_detections = faces.process(frame)
        
        fps = 1 / (time.time() - start)
        fps_list.append(fps)
        frame_count += 1
        
        print(f"   Frame {frame_count}: Gesture={gesture}, FPS={fps:.1f}")
    
    avg_fps = sum(fps_list) / len(fps_list)
    print(f"   ✓ Average FPS: {avg_fps:.1f}")
    
except Exception as e:
    print(f"   ✗ Detection test failed: {e}")
    sys.exit(1)
finally:
    cap.release()

print("\n" + "=" * 50)
print("✅ All tests passed! Ready for deployment.")
print("\nNext steps:")
print("  1. Run: python3 Recunostere/main.py")
print("  2. Use hand gestures to control the game")
print("  3. Press 'Q' or ESC to quit")
