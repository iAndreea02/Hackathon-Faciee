import cv2
from hands.hand_detector import HandDetector

detector = HandDetector()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Detectăm mâinile
    results = detector.detect(frame)

    # Selectăm doar mâna cea mai apropiată
    hand = detector.get_biggest_hand(results)

    # Dacă există o mână
    if hand:
        gesture = detector.classify_gesture(hand)

        cv2.putText(frame, f"GESTURE: {gesture}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Desenăm DOAR această mână
        frame = detector.draw_hands(frame, hand)

    cv2.imshow("Hand Gesture Test", frame)

    # Ieșire cu tasta Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
