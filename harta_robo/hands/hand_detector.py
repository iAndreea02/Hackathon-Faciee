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

        # pentru stabilizarea pinch-zoom
        self.prev_pinch = None

    # ----------------------------------------------------------
    def detect(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return self.hands.process(rgb)

    # ----------------------------------------------------------
    def get_biggest_hand(self, results):
        if not results.multi_hand_landmarks:
            return None

        max_size = 0
        biggest_hand = None

        for hand in results.multi_hand_landmarks:
            xs = [lm.x for lm in hand.landmark]
            ys = [lm.y for lm in hand.landmark]
            area = (max(xs)-min(xs)) * (max(ys)-min(ys))

            if area > max_size:
                max_size = area
                biggest_hand = hand

        return biggest_hand

    # ----------------------------------------------------------
    def draw_hands(self, frame, hand):
        if hand:
            self.drawer.draw_landmarks(
                frame, hand, self.mp_hands.HAND_CONNECTIONS
            )
        return frame

    # ----------------------------------------------------------
    # PINCH DISTANCE (mare + arătător)
    # ----------------------------------------------------------
    def pinch_distance(self, hand):
        if hand is None:
            return None

        lm = hand.landmark
        x1, y1 = lm[4].x, lm[4].y     # deget mare
        x2, y2 = lm[8].x, lm[8].y     # arătător

        dist = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        return dist

    # ----------------------------------------------------------
    # GESTURE + PINCH-ZOOM
    # ----------------------------------------------------------
    def classify_gesture(self, hand):

        pinch = self.pinch_distance(hand)

        # ============================
        #  PINCH-ZOOM DETECTION
        # ============================
        # if pinch is not None:
        #     if self.prev_pinch is None:
        #         self.prev_pinch = pinch
        #     else:
        #         diff = pinch - self.prev_pinch

        #         if diff > 0.015:      # depărtezi degetele
        #             self.prev_pinch = pinch
        #             return "ZOOM_IN"

        #         elif diff < -0.015:   # apropii degetele
        #             self.prev_pinch = pinch
        #             return "ZOOM_OUT"

        # dacă nu există zoom, continuăm cu gesturile normale
        if hand is None:
            return "NONE"

        lm = hand.landmark

        def finger_up(tip, pip):
            return lm[tip].y < lm[pip].y - 0.02

        thumb_up   = lm[4].y < lm[3].y - 0.01
        thumb_down = lm[4].y > lm[3].y + 0.01

        index_up  = finger_up(8, 6)
        middle_up = finger_up(12, 10)
        ring_up   = finger_up(16, 14)
        pinky_up  = finger_up(20, 18)

        fingers = [thumb_up, index_up, middle_up, ring_up, pinky_up]

        # GESTURI CLASICE
        if fingers == [True, True, True, True, True]:
            return "PALM"

        if fingers == [False, False, False, False, False]:
            return "FIST"

        if thumb_up and not any([index_up, middle_up, ring_up, pinky_up]):
            return "LIKE"

        if thumb_down and not any([index_up, middle_up, ring_up, pinky_up]):
            return "DISLIKE"

        if index_up and middle_up and not ring_up and not pinky_up:
            return "PEACE"

        if index_up and pinky_up and not middle_up and not ring_up:
            return "ROCK"

        if index_up and middle_up and ring_up and not pinky_up:
            return "BACK"

        return "NONE"
