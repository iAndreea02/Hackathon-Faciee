import cv2
from cvzone.FaceDetectionModule import FaceDetector

class FaceProcessor:
    def __init__(self):
        # CVZone FaceDetector
        self.face_detector = FaceDetector(minDetectionCon=0.5)

    # ----------------------------------------------------------------------
    def process(self, frame):
        """
        Procesează frame-ul și returnează:
        - DOAR fața cea mai aproape de cameră (biggest face)
        - frame-ul cu detecțiile desenate
        """
        frame, bboxs = self.face_detector.findFaces(frame, draw=False)
        
        if not bboxs:
            return None, frame

        # Selectăm fața cea mai mare (cea mai aproape)
        biggest_face = None
        biggest_area = 0

        for bbox in bboxs:
            # bbox format: [x, y, w, h]
            area = bbox[2] * bbox[3]  # width * height

            if area > biggest_area:
                biggest_area = area
                biggest_face = bbox

        return biggest_face, frame

    # ----------------------------------------------------------------------
    def draw_face_box(self, frame, detection):
        """
        Desenează DOAR chenarul feței celei mai apropiate.
        """
        if detection:
            x, y, w, h = detection
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return frame

    # ----------------------------------------------------------------------
    def get_head_turn(self, frame, face_bbox):
        """
        Determină orientarea capului: LEFT / RIGHT / CENTER.
        Folosește detecția simplificată din CVZone.
        """
        if face_bbox is None:
            return "NO_FACE"

        x, y, w, h = face_bbox
        center_x = x + w // 2
        frame_width = frame.shape[1]
        frame_center = frame_width // 2

        # Prag de sensibilitate
        sensitivity = frame_width * 0.15

        if center_x < frame_center - sensitivity:
            return "RIGHT"
        elif center_x > frame_center + sensitivity:
            return "LEFT"
        else:
            return "CENTER"
