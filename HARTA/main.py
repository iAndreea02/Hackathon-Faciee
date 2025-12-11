import cv2
import pygame
import threading
import time
import numpy as np
from hands.hand_detector import HandDetector
from face.face_processor import FaceProcessor
from game.game_engine import GameEngine

# Încercăm să importăm Picamera2
try:
    from picamera2 import Picamera2
    print("Picamera2 importat cu succes.")
except ImportError:
    print("Eroare: Picamera2 nu este instalat. Acest cod va crăpa pe PC.")

gesture_shared = "NONE"

def camera_thread():
    global gesture_shared

    # --- INITIALIZARE PICAMERA2 ---
    picam2 = Picamera2()

    # Configurația video (RGB888 este bun pentru MediaPipe, dar OpenCV vrea BGR la afisare)
    # Folosim 640x480 pentru performanță mai bună în timp real cu MediaPipe
    config = picam2.create_video_configuration(
        main={"size": (640, 480), "format": "RGB888"}, 
    )
    picam2.configure(config)
    picam2.start()
    
    # Așteaptă puțin să se inițializeze senzorul
    time.sleep(1)

    print("Camera Raspberry Pi pornită.")

    # Detectori
    hands = HandDetector()
    faces = FaceProcessor()

    while True:
        try:
            # Capturăm frame-ul ca array (NumPy)
            # Deoarece am configurat "RGB888", frame-ul este RGB
            frame = picam2.capture_array()
        except Exception as e:
            print(f"Eroare captură: {e}")
            continue

        if frame is None:
            continue

        # --- PROCESARE (MediaPipe lucrează nativ cu RGB) ---
        # Nu mai e nevoie de cvtColor BGR2RGB pentru MediaPipe
        
        # Detectare mână
        results = hands.detect(frame)
        hand = hands.get_biggest_hand(results)
        gesture = hands.classify_gesture(hand)

        # Actualizare variabilă globală pentru joc
        gesture_shared = gesture

        # --- AFIȘARE (OpenCV) ---
        # OpenCV așteaptă BGR pentru a afișa culorile corect
        # Convertim RGB -> BGR doar pentru fereastra de preview
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Redimensionare pentru preview (opțional, dar bun pentru performanță GUI)
        frame_small = cv2.resize(frame_bgr, (320, 240))
        
        # Adăugare text
        cv2.putText(frame_small, f"GESTURE: {gesture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Camera Control (Pi)", frame_small)

        # Ieșire cu tasta 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Curățare resurse
    picam2.stop()
    picam2.close()
    cv2.destroyAllWindows()


###############################
# GAME THREAD
###############################
# Inițializare joc
game = GameEngine("assets/harta_buna1.png")

# Pornire thread cameră (daemon=True se închide odată cu programul principal)
threading.Thread(target=camera_thread, daemon=True).start()

# Game loop (Pygame trebuie să ruleze pe main thread)
while True:
    # Actualizează jocul cu gestul curent primit din celălalt thread
    game.update(gesture_shared)
    game.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()