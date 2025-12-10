import cv2
import pygame
from hands.hand_detector import HandDetector
from face.face_processor import FaceProcessor
from game.game_engine import GameEngine

# Init pygame before OpenCV windows
pygame.init()

# Vision systems
hands = HandDetector()
faces = FaceProcessor()

# Game & Robot
game = GameEngine("assets/harta.png", "assets/move.gif")

# -------------------------------------------------------------
# Camera – Raspberry Pi via GStreamer (libcamera)
gst_pipeline = (
    "libcamerasrc ! "
    "video/x-raw, width=640, height=480, framerate=30/1 ! "
    "videoconvert ! "
    "video/x-raw, format=BGR ! "
    "appsink drop=1"
)

cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)
# -------------------------------------------------------------

# (opțional) dacă vrei totuși să reduci la 320x240 pentru viteză
TARGET_W, TARGET_H = 320, 240

running = True
while running:

    ok, frame = cap.read()
    if not ok:
        print("Camera nu poate fi citită!")
        break

    # Resize for speed (IMPORTANT for Pi)
    frame = cv2.resize(frame, (TARGET_W, TARGET_H))

    # Face processing
    detection, mesh = faces.process(frame)

    # Hand processing
    results = hands.detect(frame)
    hand = hands.get_biggest_hand(results)
    gesture = hands.classify_gesture(hand)

    # Update game → MOVE ROBOT WITH GESTURE
    game.update(gesture)
    game.draw()

    # Small preview
    preview = frame.copy()
    cv2.putText(preview, f"GESTURE: {gesture}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.imshow("Camera Control", preview)

    # Handle pygame quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Quit with Q or ESC
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        running = False

cap.release()
cv2.destroyAllWindows()
pygame.quit()
