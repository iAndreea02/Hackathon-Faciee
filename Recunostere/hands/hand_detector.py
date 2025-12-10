import cv2
import mediapipe as mp
import math

class HandDetector:
    def __init__(self, max_hands=2):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=max_hands,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        )
        self.drawer = mp.solutions.drawing_utils

    # ----------------------------------------------------------
    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        return results

    # ----------------------------------------------------------
    def get_biggest_hand(self, results):
        """Returnează DOAR mâna cea mai apropiată de cameră (cea mai mare)"""
        if not results.multi_hand_landmarks:
            return None

        max_size = 0
        biggest_hand = None

        for idx, hand in enumerate(results.multi_hand_landmarks):
            # calculăm bounding box normalizat
            xs = [lm.x for lm in hand.landmark]
            ys = [lm.y for lm in hand.landmark]

            width = max(xs) - min(xs)
            height = max(ys) - min(ys)
            area = width * height

            if area > max_size:
                max_size = area
                biggest_hand = hand

        return biggest_hand

    # ----------------------------------------------------------
    def draw_hands(self, frame, hand):
        """Desenează DOAR mâna selectată"""
        if hand:
            self.drawer.draw_landmarks(
                frame,
                hand,
                self.mp_hands.HAND_CONNECTIONS
            )
        return frame

    # ----------------------------------------------------------
    def classify_gesture(self, hand):

        if hand is None:
            return "NONE"

        lm = hand.landmark

        # FUNCȚIE UTILĂ – verifică dacă degetul este ridicat
        def finger_up(tip, pip):
            return lm[tip].y < lm[pip].y - 0.02  # mică rezervă pentru stabilitate

        # Deget mare
        thumb_up = lm[4].y < lm[3].y - 0.01
        thumb_down = lm[4].y > lm[3].y + 0.01

        # Degetele normale
        index_up  = finger_up(8, 6)
        middle_up = finger_up(12, 10)
        ring_up   = finger_up(16, 14)
        pinky_up  = finger_up(20, 18)

        # Listă pentru simplificare
        fingers = [thumb_up, index_up, middle_up, ring_up, pinky_up]
        # ordine: [T, I, M, R, P]

        # -----------------------------------------
        # GESTURI
        # -----------------------------------------

        # ✋ PALM – toate sus
        if fingers == [True, True, True, True, True]:
            return "PALM"

        # ✊ FIST – toate jos
        if fingers == [False, False, False, False, False]:
            return "FIST"

        # 👍 LIKE – doar thumb-up
        if thumb_up and not index_up and not middle_up and not ring_up and not pinky_up:
            return "LIKE"

        # 👎 DISLIKE – doar thumb-down
        if thumb_down and not index_up and not middle_up and not ring_up and not pinky_up:
            return "DISLIKE"

        # ✌️ PEACE – index + middle sus
        if index_up and middle_up and not ring_up and not pinky_up:
            return "PEACE"

        # 🤘 ROCK – index + pinky sus
        if index_up and pinky_up and not middle_up and not ring_up:
            return "ROCK"

        # 🆕 BACK – index + middle + ring sus (pinky jos)
        if index_up and middle_up and ring_up and not pinky_up:
            return "BACK"

        return "NONE"
