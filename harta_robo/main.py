import cv2
import pygame
import threading
from hands.hand_detector import HandDetector
from face.face_processor import FaceProcessor
from game.game_engine import GameEngine

gesture_shared = "NONE"

def camera_thread():
    global gesture_shared

    cap = cv2.VideoCapture(0)
    hands = HandDetector()
    faces = FaceProcessor()

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        # detect hand
        results = hands.detect(frame)
        hand = hands.get_biggest_hand(results)
        gesture = hands.classify_gesture(hand)

        # update gesture shared
        gesture_shared = gesture

        # show cam
        frame_small = cv2.resize(frame, (320, 240))
        cv2.putText(frame_small, f"GESTURE: {gesture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

        cv2.imshow("Camera Control", frame_small)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


###############################
# GAME THREAD
###############################
game = GameEngine("assets/harta_buna1.png")

# start camera async
threading.Thread(target=camera_thread, daemon=True).start()

# game loop
while True:
    game.update(gesture_shared)
    game.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
