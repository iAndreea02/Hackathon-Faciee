import cv2
from face.face_processor import FaceProcessor

processor = FaceProcessor()
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    h, w = frame.shape[:2]

    detection, mesh = processor.process(frame)

    frame = processor.draw_face_box(frame, detection)

    head = processor.get_head_turn(mesh, w)

    cv2.putText(frame, f"HEAD: {head}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Face Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
