import cv2
from cvzone.HandTrackingModule import HandDetector as CVHandDetector
import math

class HandDetector:
    def __init__(self, max_hands=2):
        # CVZone HandDetector
        self.detector = CVHandDetector(maxHands=max_hands, detectionCon=0.6, trackCon=0.6)
        self.hands_data = []

    # ----------------------------------------------------------
    def detect(self, frame):
        """Detectează mâini folosind CVZone"""
        frame, self.hands_data = self.detector.findHands(frame)
        return self.hands_data

    # ----------------------------------------------------------
    def get_biggest_hand(self, hands_data):
        """Returnează DOAR mâna cea mai apropiată de cameră (cea mai mare)"""
        if not hands_data:
            return None

        max_size = 0
        biggest_hand = None

        for hand in hands_data:
            # hand este dict cu keys: 'lmList' (lista de landmarks), 'bbox' (bounding box)
            bbox = hand["bbox"]
            width, height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            area = width * height

            if area > max_size:
                max_size = area
                biggest_hand = hand

        return biggest_hand

    # ----------------------------------------------------------
    def draw_hands(self, frame, hand):
        """Desenează DOAR mâna selectată"""
        if hand:
            lmList = hand["lmList"]
            # Desenează puncte și conexiuni
            for i, lm in enumerate(lmList):
                cv2.circle(frame, (int(lm[0]), int(lm[1])), 5, (0, 255, 0), -1)
        return frame

    # ----------------------------------------------------------
    def classify_gesture(self, hand):

        if hand is None:
            return "NONE"

        lmList = hand["lmList"]  # Lista de coordonate [x, y, z]

        # FUNCȚIE UTILĂ – verifică dacă degetul este ridicat
        def finger_up(tip, pip):
            return lmList[tip][1] < lmList[pip][1] - 10  # diferență în pixeli

        # Deget mare (indici 3, 4)
        thumb_up = lmList[4][1] < lmList[3][1] - 5
        thumb_down = lmList[4][1] > lmList[3][1] + 5

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
