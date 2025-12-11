import cv2
import mediapipe as mp

class FaceProcessor:
    def __init__(self):
        # Detectare față
        self.mp_face = mp.solutions.face_detection
        self.face_detector = self.mp_face.FaceDetection(
            model_selection=1,
            min_detection_confidence=0.5
        )

        # Face Mesh (landmark-uri invizibile)
        self.mp_mesh = mp.solutions.face_mesh
        self.mesh = self.mp_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=3,                  # detectează mai multe fețe, alegem doar una
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Utilitar pentru desenare (chenar față)
        self.drawer = mp.solutions.drawing_utils

    # ----------------------------------------------------------------------
    def process(self, frame):
        """
        Procesează frame-ul și returnează:
        - DOAR fața cea mai aproape de cameră (biggest face)
        - mesh-ul complet (pentru orientarea capului)
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectăm toate fețele
        detections = self.face_detector.process(rgb)

        # Mesh pentru toate fețele
        mesh_results = self.mesh.process(rgb)

        # Dacă nu există fețe
        if not detections.detections:
            return None, mesh_results

        # Selectăm fața cea mai mare (cea mai aproape)
        biggest_face = None
        biggest_area = 0

        for det in detections.detections:
            bbox = det.location_data.relative_bounding_box
            area = bbox.width * bbox.height  # aria normalizată

            if area > biggest_area:
                biggest_area = area
                biggest_face = det

        return biggest_face, mesh_results

    # ----------------------------------------------------------------------
    def draw_face_box(self, frame, detection):
        """
        Desenează DOAR chenarul feței celei mai apropiate.
        """
        if detection:
            self.drawer.draw_detection(frame, detection)
        return frame

    # ----------------------------------------------------------------------
    def get_head_turn(self, mesh_results, frame_width):
        """
        Determină orientarea capului: LEFT / RIGHT / CENTER.
        Folosește landmark-urile:
        - 33  = obraz stâng
        - 263 = obraz drept
        - 1   = vârful nasului
        """
        if not mesh_results.multi_face_landmarks:
            return "NO_FACE"

        # Alegem primul mesh (corespondent cu cea mai mare față, deoarece mediapipe ordonează după proximity)
        face = mesh_results.multi_face_landmarks[0].landmark

        # Extragem punctele necesare
        left = face[33].x * frame_width      # obraz stâng
        right = face[263].x * frame_width    # obraz drept
        nose = face[1].x * frame_width       # vârful nasului

        # Distanțe relative
        dist_left = nose - left
        dist_right = right - nose

        sensitivity = 1.15  # prag pentru stabilitate

        if dist_left > dist_right * sensitivity:
            return "RIGHT"
        elif dist_right > dist_left * sensitivity:
            return "LEFT"
        else:
            return "CENTER"
