import cv2
import mediapipe as mp
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

# Culori
COLOR_BG = get_color_from_hex("#050E23")
COLOR_CYAN = get_color_from_hex("#00B5CC")
COLOR_MAGENTA = get_color_from_hex("#E62B90")

# Întrebări și mapping
questions = [
    {"question": "Dacă ar fi să alegi, ai prefera să fii un supererou al...",
     "options": ["Calculatorelor și codului magic", "Luminilor și cablurilor electrice"]},
    {"question": "Când te gândești la o zi de muncă perfectă, ce vezi?",
     "options": ["Stând la birou cu tastatura și cafeaua", "Jucându-te cu roboți și circuite"]},
    {"question": "Ce tip de puteri vrei să ai?",
     "options": ["Puterea de a controla software-ul lumii", "Puterea de a controla electronii și circuitele"]},
    {"question": "Weekendul ideal ar fi...",
     "options": ["Hackathon cu prietenii", "Construirea unui gadget nebunesc"]},
    {"question": "Când ești pus la o alegere: mare sau munte, tu alegi...",
     "options": ["Mare (relaxare, cod și Wi-Fi)", "Munte (provocări și circuite)"]}
]

specializari = [
    "Ingineria Sistemelor - Automatica si Informatica Aplicata",
    "Calculatoare si Tehnologia Informatiei - Calculatoare",
    "Inginerie Electrică - Electromecanică",
    "Inginerie Electrică - Electronică de putere și acționări electrice",
    "Inginerie Electrică - Inginerie Electrică și Calculatoare",
    "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Electronică Aplicată",
    "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Rețele și Software de Telecomunicații"
]

answers_map = {
    "Calculatorelor și codului magic": [
        "Calculatoare si Tehnologia Informatiei - Calculatoare",
        "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Rețele și Software de Telecomunicații"
    ],
    "Luminilor și cablurilor electrice": [
        "Ingineria Sistemelor - Automatica si Informatica Aplicata",
        "Inginerie Electrică - Electromecanică",
        "Inginerie Electrică - Electronică de putere și acționări electrice",
        "Inginerie Electrică - Inginerie Electrică și Calculatoare",
        "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Electronică Aplicată"
    ],
    "Stând la birou cu tastatura și cafeaua": [
        "Calculatoare si Tehnologia Informatiei - Calculatoare"
    ],
    "Jucându-te cu roboți și circuite": [
        "Ingineria Sistemelor - Automatica si Informatica Aplicata",
        "Inginerie Electrică - Electromecanică",
        "Inginerie Electrică - Electronică de putere și acționări electrice"
    ],
    "Puterea de a controla software-ul lumii": [
        "Calculatoare si Tehnologia Informatiei - Calculatoare",
        "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Rețele și Software de Telecomunicații"
    ],
    "Puterea de a controla electronii și circuitele": [
        "Inginerie Electrică - Electromecanică",
        "Inginerie Electrică - Electronică de putere și acționări electrice",
        "Inginerie Electrică - Inginerie Electrică și Calculatoare",
        "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Electronică Aplicată"
    ],
    "Hackathon cu prietenii": [
        "Calculatoare si Tehnologia Informatiei - Calculatoare",
        "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Rețele și Software de Telecomunicații"
    ],
    "Construirea unui gadget nebunesc": [
        "Ingineria Sistemelor - Automatica si Informatica Aplicata",
        "Inginerie Electrică - Electromecanică",
        "Inginerie Electrică - Electronică de putere și acționări electrice",
        "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Electronică Aplicată"
    ],
    "Mare (relaxare, cod și Wi-Fi)": [
        "Calculatoare si Tehnologia Informatiei - Calculatoare"
    ],
    "Munte (provocări și circuite)": [
        "Ingineria Sistemelor - Automatica si Informatica Aplicata",
        "Inginerie Electrică - Electromecanică",
        "Inginerie Electrică - Electronică de putere și acționări electrice"
    ]
}

# -------------------------
# Face Processor
# -------------------------
class FaceProcessor:
    def __init__(self):
        self.mp_face = mp.solutions.face_detection
        self.face_detector = self.mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5)
        self.mp_mesh = mp.solutions.face_mesh
        self.mesh = self.mp_mesh.FaceMesh(static_image_mode=False, max_num_faces=3,
                                          refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawer = mp.solutions.drawing_utils

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = self.face_detector.process(rgb)
        mesh_results = self.mesh.process(rgb)
        if not detections.detections:
            return None, mesh_results
        biggest_face = max(detections.detections, key=lambda d: d.location_data.relative_bounding_box.width *
                           d.location_data.relative_bounding_box.height)
        return biggest_face, mesh_results

    def get_head_turn(self, mesh_results, frame_width):
        if not mesh_results.multi_face_landmarks:
            return "NO_FACE"
        face = mesh_results.multi_face_landmarks[0].landmark
        left = face[33].x * frame_width
        right = face[263].x * frame_width
        nose = face[1].x * frame_width
        dist_left = nose - left
        dist_right = right - nose
        sensitivity = 1.15
        if dist_left > dist_right * sensitivity:
            return "RIGHT"
        elif dist_right > dist_left * sensitivity:
            return "LEFT"
        else:
            return "CENTER"

# -------------------------
# TinderPage
# -------------------------
class TinderPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Atribute necesare
        self.result_widget = None
        self.index = 0
        self.selected_answers = []

        self.face_processor = FaceProcessor()
        self.cap = None
        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

        with self.root_layout.canvas.before:
            Color(*COLOR_BG)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)

        # Interval de actualizare (camera)
        self._camera_event = None

    def update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def on_enter(self):
        # Pornim camera când intrăm în ecran
        if not self.cap:
            self.cap = cv2.VideoCapture(0)
        if not self._camera_event:
            self._camera_event = Clock.schedule_interval(self.update, 0.2)

    def on_leave(self):
        # Oprim camera când părăsim ecranul
        if self.cap:
            self.cap.release()
            self.cap = None
        if self._camera_event:
            self._camera_event.cancel()
            self._camera_event = None

    def update(self, dt):
        if self.index >= len(questions):
            return

        ret, frame = self.cap.read()
        if not ret:
            return
        height, width, _ = frame.shape
        face, mesh = self.face_processor.process(frame)
        turn = self.face_processor.get_head_turn(mesh, width)

        # Alegere răspuns în funcție de orientarea capului
        if turn == "LEFT":
            self.select_answer(questions[self.index]["options"][0])
        elif turn == "RIGHT":
            self.select_answer(questions[self.index]["options"][1])

    def select_answer(self, answer):
        if self.index >= len(questions):
            return
        self.selected_answers.append(answer)
        self.index += 1
        if self.index >= len(questions):
            self.show_results()

    def show_results(self):
        # Ștergem vechiul widget dacă există
        if self.result_widget:
            self.root_layout.remove_widget(self.result_widget)

        self.result_widget = BoxLayout(orientation='vertical', spacing=20, padding=40)
        label = Label(text="Specializarea potrivită pentru tine:", font_size=24, color=COLOR_CYAN)
        self.result_widget.add_widget(label)

        # Calcul match
        match_counts = {spec: 0 for spec in specializari}
        for ans in self.selected_answers:
            for spec in answers_map.get(ans, []):
                match_counts[spec] += 1

        best_spec = max(match_counts, key=match_counts.get)
        percent = int((match_counts[best_spec] / len(self.selected_answers)) * 100)

        result_label = Label(text=f"{best_spec}\nProcent match: {percent}%", font_size=22, color=COLOR_MAGENTA)
        self.result_widget.add_widget(result_label)

        self.root_layout.add_widget(self.result_widget)
