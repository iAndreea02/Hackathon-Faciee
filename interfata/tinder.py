# COD COMPLET CU CULORI VIDEO REPARATE

import cv2
import mediapipe as mp
import time
import numpy as np
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

print("[DEBUG] Încerc importarea Picamera2...")
try:
    from picamera2 import Picamera2
    HAS_PICAMERA = True
    print("[DEBUG] Picamera2 importat cu SUCCES!")
except ImportError as e:
    print(f"[DEBUG] Picamera2 NU a fost găsit: {e}")
    HAS_PICAMERA = False

COLOR_BG = get_color_from_hex("#050E23")
COLOR_DARK_NAVY = get_color_from_hex("#050E23") 
COLOR_CYAN = get_color_from_hex("#00B5CC")
COLOR_MAGENTA = get_color_from_hex("#E62B90")
COLOR_WHITE = get_color_from_hex("#FFFFFF")
COLOR_PURPLE = get_color_from_hex("#8E24AA")
COLOR_GREEN = get_color_from_hex("#00FF00")

questions = [
    {"question": "Daca ar fi sa alegi, ai prefera sa fii un supererou al...",
     "options": ["Calculatorelor si codului magic", "Luminilor si cablurilor electrice"]},
    {"question": "Cand te gandesti la o zi de munca perfecta, ce vezi?",
     "options": ["Stand la birou cu tastatura", "Jucandu-te cu roboti si circuite"]},
    {"question": "Ce tip de puteri vrei sa ai?",
     "options": ["Sa controlezi software-ul", "Sa controlezi electronii"]},
    {"question": "Weekendul ideal ar fi...",
     "options": ["Hackathon cu prietenii", "Construirea unui gadget"]},
    {"question": "Cand esti pus la o alegere: mare sau munte, tu alegi...",
     "options": ["Mare (relaxare & cod)", "Munte (provocari tehnice)"]}
]

specializari = [
    "Ingineria Sistemelor - Automatica si Informatica Aplicata",
    "Calculatoare si Tehnologia Informatiei - Calculatoare",
    "Inginerie Electrica - Electromecanica",
    "Inginerie Electrica - Electronica de putere",
    "Inginerie Electrica - Inginerie Electrica si Calculatoare",
    "Inginerie Electronica si Telecomunicatii - Electronica Aplicata",
    "Inginerie Electronica si Telecomunicatii - Retele si Software"
]

answers_map = {
    "Calculatorelor si codului magic": [
        "Calculatoare si Tehnologia Informatiei - Calculatoare",
        "Inginerie Electronica si Telecomunicatii - Retele si Software"
    ],
    "Luminilor si cablurilor electrice": [
        "Ingineria Sistemelor - Automatica si Informatica Aplicata",
        "Inginerie Electrica - Electromecanica",
        "Inginerie Electrica - Electronica de putere"
    ],
    "Stand la birou cu tastatura": [
        "Calculatoare si Tehnologia Informatiei - Calculatoare"
    ],
    "Jucandu-te cu roboti si circuite": [
        "Ingineria Sistemelor - Automatica si Informatica Aplicata",
        "Inginerie Electrica - Electromecanica"
    ],
    "Sa controlezi software-ul": [
        "Calculatoare si Tehnologia Informatiei - Calculatoare"
    ],
    "Sa controlezi electronii": [
        "Inginerie Electrica - Electromecanica",
        "Inginerie Electronica si Telecomunicatii - Electronica Aplicata"
    ],
    "Hackathon cu prietenii": [
        "Calculatoare si Tehnologia Informatiei - Calculatoare"
    ],
    "Construirea unui gadget": [
        "Ingineria Sistemelor - Automatica si Informatica Aplicata",
        "Inginerie Electrica - Electromecanica"
    ],
    "Mare (relaxare & cod)": [
        "Calculatoare si Tehnologia Informatiei - Calculatoare"
    ],
    "Munte (provocari tehnice)": [
        "Ingineria Sistemelor - Automatica si Informatica Aplicata",
        "Inginerie Electrica - Electromecanica"
    ]
}

screen_map = {
    "Ingineria Sistemelor - Automatica si Informatica Aplicata": "automatica",
    "Calculatoare si Tehnologia Informatiei - Calculatoare": "cti",
    "Inginerie Electrica - Electromecanica": "electrica",
    "Inginerie Electrica - Electronica de putere": "electrica",
    "Inginerie Electrica - Inginerie Electrica si Calculatoare": "electrica",
    "Inginerie Electronica si Telecomunicatii - Electronica Aplicata": "etc",
    "Inginerie Electronica si Telecomunicatii - Retele si Software": "etc"
}

class RoundedCard(BoxLayout):
    def __init__(self, bg_color, radius=20, padding_val=[10,10,10,10], has_border=False, border_color=None, **kwargs):
        super().__init__(**kwargs)
        self.padding = padding_val
        self.bg_color_rgba = bg_color
        self.radius_val = radius
        self.border_color_rgba = border_color if border_color else [0,0,0,0]
        
        with self.canvas.before:
            Color(*self.bg_color_rgba)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
            if has_border:
                self.border_color_instruction = Color(*self.border_color_rgba)
                self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, radius), width=3)
        
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = [self.radius_val]
        if hasattr(self, 'border'):
            self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius_val)
            
    def update_border_color(self, color):
        if hasattr(self, 'border_color_instruction'):
            self.border_color_instruction.rgba = color

class FaceProcessor:
    def __init__(self):
        self.mp_face = mp.solutions.face_detection
        self.mp_mesh = mp.solutions.face_mesh
        self.mesh = self.mp_mesh.FaceMesh(static_image_mode=False, max_num_faces=1,
                                          refine_landmarks=True, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def process(self, frame_rgb):
        frame_rgb.flags.writeable = False
        mesh_results = self.mesh.process(frame_rgb)
        frame_rgb.flags.writeable = True
        return mesh_results

    def get_head_turn(self, mesh_results, frame_width):
        if not mesh_results.multi_face_landmarks:
            return "NO_FACE"
        face = mesh_results.multi_face_landmarks[0].landmark
        left_eye = face[33].x * frame_width
        right_eye = face[263].x * frame_width
        nose = face[1].x * frame_width
        
        dist_left = nose - left_eye
        dist_right = right_eye - nose
        
        sensitivity = 1.3
        if dist_left > dist_right * sensitivity:
            return "RIGHT"
        elif dist_right > dist_left * sensitivity:
            return "LEFT"
        else:
            return "CENTER"

class TinderPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.face_processor = FaceProcessor()
        
        self.picam2 = None
        self.cap = None
        self.using_picamera = False
        self._camera_event = None
        
        self.index = 0
        self.selected_answers = []
        self.can_answer = True
        self.hold_start_time = 0
        self.last_turn = "CENTER"
        self.required_hold_time = 2.0

        with self.canvas.before:
            Color(*COLOR_BG)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(size=self.update_bg, pos=self.update_bg)

        self.main_layout = BoxLayout(orientation='vertical', spacing=20, padding=[20, 20, 20, 20])
        self.add_widget(self.main_layout)

        self.question_card = RoundedCard(bg_color=COLOR_DARK_NAVY, radius=20, 
                                         has_border=True, border_color=COLOR_CYAN,
                                         size_hint_y=0.25)
        self.lbl_question = Label(text="Se incarca...", font_size='20sp', bold=True, 
                                  color=COLOR_WHITE, halign='center', valign='middle')
        self.lbl_question.bind(size=lambda *x: self.lbl_question.setter('text_size')(self.lbl_question, (self.lbl_question.width - 20, None)))
        self.question_card.add_widget(self.lbl_question)
        self.main_layout.add_widget(self.question_card)

        self.camera_container = FloatLayout(size_hint_y=0.55)
        
        self.camera_card = RoundedCard(bg_color=(0,0,0,1), radius=20, 
                                       has_border=True, border_color=COLOR_MAGENTA,
                                       size_hint=(0.8, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.camera_image = Image(allow_stretch=True, keep_ratio=True)
        self.camera_card.add_widget(self.camera_image)
        self.camera_container.add_widget(self.camera_card)

        self.card_left = RoundedCard(bg_color=(0, 0, 0, 0.6), radius=15, 
                                     has_border=True, border_color=COLOR_CYAN,
                                     size_hint=(0.35, 0.3), pos_hint={'x': 0.02, 'center_y': 0.5})
        self.card_left.orientation = 'vertical'
        self.lbl_left_title = Label(text="STANGA", font_size='12sp', color=COLOR_CYAN, bold=True, size_hint_y=0.3)
        self.card_left.add_widget(self.lbl_left_title)
        self.lbl_left = Label(text="", font_size='14sp', bold=True, color=COLOR_WHITE,
                              halign='center', valign='middle')
        self.lbl_left.bind(size=lambda *x: self.lbl_left.setter('text_size')(self.lbl_left, (self.lbl_left.width, None)))
        self.card_left.add_widget(self.lbl_left)
        self.camera_container.add_widget(self.card_left)

        self.card_right = RoundedCard(bg_color=(0, 0, 0, 0.6), radius=15, 
                                      has_border=True, border_color=COLOR_CYAN,
                                      size_hint=(0.35, 0.3), pos_hint={'right': 0.98, 'center_y': 0.5})
        self.card_right.orientation = 'vertical'
        self.lbl_right_title = Label(text="DREAPTA", font_size='12sp', color=COLOR_CYAN, bold=True, size_hint_y=0.3)
        self.card_right.add_widget(self.lbl_right_title)
        self.lbl_right = Label(text="", font_size='14sp', bold=True, color=COLOR_WHITE,
                               halign='center', valign='middle')
        self.lbl_right.bind(size=lambda *x: self.lbl_right.setter('text_size')(self.lbl_right, (self.lbl_right.width, None)))
        self.card_right.add_widget(self.lbl_right)
        self.camera_container.add_widget(self.card_right)

        self.main_layout.add_widget(self.camera_container)

        self.lbl_status = Label(text="Intoarce capul si MENTINE 2 secunde", 
                                font_size='14sp', color=COLOR_WHITE, size_hint_y=0.1)
        self.main_layout.add_widget(self.lbl_status)

        self.btn_back = Button(text="Inapoi la Meniu", size_hint=(1, None), height=50,
                               background_normal='', background_color=COLOR_MAGENTA, bold=True)
        self.btn_back.bind(on_release=self.go_back)

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_enter(self):
        self.main_layout.clear_widgets()
        self.main_layout.add_widget(self.question_card)
        self.main_layout.add_widget(self.camera_container)
        self.main_layout.add_widget(self.lbl_status)
        
        self.index = 0
        self.selected_answers = []
        self.can_answer = True
        self.hold_start_time = 0
        self.last_turn = "CENTER"
        self.card_left.update_border_color(COLOR_CYAN)
        self.card_right.update_border_color(COLOR_CYAN)
        self.lbl_status.text = "Initializare camera..."
        
        self.update_question_ui()
        Clock.schedule_once(self.start_camera_sequence, 0.1)

    def start_camera_sequence(self, dt):
        if HAS_PICAMERA:
            try:
                self.picam2 = Picamera2()
                config = self.picam2.create_video_configuration(
                    main={"size": (640, 480), "format": "RGB888"}
                )
                self.picam2.configure(config)
                self.picam2.start()
                time.sleep(2)
                self.using_picamera = True
            except:
                self.using_picamera = False
                self.picam2 = None
        else:
            self.using_picamera = False

        if not self.using_picamera:
            self.cap = cv2.VideoCapture(0)

        self.lbl_status.text = "Intoarce capul si MENTINE 2 secunde"
        self._camera_event = Clock.schedule_interval(self.update, 1.0/30.0)

    def on_leave(self):
        if self.using_picamera and self.picam2:
            try:
                self.picam2.stop()
                self.picam2.close()
            except:
                pass
            self.picam2 = None
            self.using_picamera = False
        
        if self.cap:
            self.cap.release()
            self.cap = None
        
        if self._camera_event:
            self._camera_event.cancel()

    def update_question_ui(self):
        if self.index < len(questions):
            q_data = questions[self.index]
            self.lbl_question.text = q_data["question"]
            self.lbl_left.text = q_data["options"][0]
            self.lbl_right.text = q_data["options"][1]
            
            self.card_left.update_border_color(COLOR_CYAN)
            self.card_right.update_border_color(COLOR_CYAN)
            self.lbl_status.text = "Intoarce capul si MENTINE 2 secunde"
            self.lbl_status.color = COLOR_WHITE
        else:
            self.show_results()

    def update(self, dt):
        if self.index >= len(questions): return

        frame_bgr = None
        frame_rgb_processing = None

        if self.using_picamera and self.picam2:
            try:
                frame_rgb_raw = self.picam2.capture_array()  # RGB888
            except:
                return
            frame_bgr = cv2.cvtColor(frame_rgb_raw, cv2.COLOR_RGB2BGR)
            frame_bgr = cv2.flip(frame_bgr, 1)
            frame_rgb_processing = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)

        elif self.cap:
            ret, cv_frame = self.cap.read()  # BGR
            if not ret:
                return
            frame_bgr = cv2.flip(cv_frame, 1)
            frame_rgb_processing = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        else:
            return

        h, w, _ = frame_rgb_processing.shape
        mesh_results = self.face_processor.process(frame_rgb_processing)
        current_turn = self.face_processor.get_head_turn(mesh_results, w)

        if current_turn != self.last_turn:
            self.hold_start_time = time.time()
            self.last_turn = current_turn
            if self.can_answer:
                self.card_left.update_border_color(COLOR_CYAN)
                self.card_right.update_border_color(COLOR_CYAN)
                self.lbl_status.text = "Mentine pozitia..."

        elapsed = time.time() - self.hold_start_time

        if self.can_answer:
            if current_turn == "LEFT":
                self.card_left.update_border_color(COLOR_MAGENTA)
                self.lbl_status.text = f"Mentine STANGA: {2.0 - elapsed:.1f}s"
                if elapsed >= self.required_hold_time:
                    self.card_left.update_border_color(COLOR_GREEN)
                    self.select_answer(questions[self.index]["options"][0])
                    self.can_answer = False

            elif current_turn == "RIGHT":
                self.card_right.update_border_color(COLOR_MAGENTA)
                self.lbl_status.text = f"Mentine DREAPTA: {2.0 - elapsed:.1f}s"
                if elapsed >= self.required_hold_time:
                    self.card_right.update_border_color(COLOR_GREEN)
                    self.select_answer(questions[self.index]["options"][1])
                    self.can_answer = False

            elif current_turn == "CENTER":
                self.lbl_status.text = "Intoarce capul spre optiune"
        else:
            if current_turn == "CENTER":
                self.can_answer = True

        magenta_bgr = (255, 0, 255)
        green_bgr = (0,255,0)

        if current_turn == "LEFT":
            cv2.line(frame_bgr, (0,0), (0,h), magenta_bgr, 10)
        elif current_turn == "RIGHT":
            cv2.line(frame_bgr, (w-1,0), (w-1,h), magenta_bgr, 10)
        elif current_turn == "CENTER" and self.can_answer:
            cv2.circle(frame_bgr, (w//2, 30), 10, green_bgr, -1)

        frame_rgb_display = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        buf = cv2.flip(frame_rgb_display, 0).tobytes()
        texture = Texture.create(size=(w,h), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.camera_image.texture = texture

    def select_answer(self, answer):
        self.selected_answers.append(answer)
        self.index += 1
        self.lbl_status.text = "Raspuns inregistrat!"
        self.lbl_status.color = COLOR_GREEN
        Clock.schedule_once(lambda dt: self.update_question_ui(), 0.5)

    def show_results(self):
        self.on_leave()
        self.main_layout.clear_widgets()
        
        match_counts = {spec: 0 for spec in specializari}
        for ans in self.selected_answers:
            for spec in answers_map.get(ans, []):
                match_counts[spec] += 1
        
        best_spec = max(match_counts, key=match_counts.get) if self.selected_answers else "Nedeterminat"
        percent = int((match_counts[best_spec] / len(self.selected_answers)) * 100) if self.selected_answers else 0

        res_card = RoundedCard(bg_color=COLOR_DARK_NAVY, radius=20, padding_val=[20,20,20,20],
                               has_border=True, border_color=COLOR_MAGENTA)
        res_card.orientation = 'vertical'
        res_card.spacing = 15
        
        res_card.add_widget(Label(text="SPECIALIZAREA TA:", font_size='16sp', color=COLOR_CYAN))
        
        lbl_spec = Label(text=best_spec, font_size='20sp', bold=True, color=COLOR_WHITE, 
                         halign='center', valign='middle')
        lbl_spec.bind(size=lambda *x: lbl_spec.setter('text_size')(lbl_spec, (lbl_spec.width, None)))
        res_card.add_widget(lbl_spec)
        
        res_card.add_widget(Label(text=f"Potrivire: {percent}%", font_size='16sp', color=COLOR_MAGENTA))

        target_screen_name = screen_map.get(best_spec)
        if target_screen_name:
            btn_details = Button(text="Vezi Detalii Specializare", 
                                 size_hint=(1, None), height=60,
                                 background_normal='', background_color=COLOR_CYAN, 
                                 color=COLOR_DARK_NAVY, bold=True)
            btn_details.bind(on_release=lambda x: self.go_to_spec_page(target_screen_name))
            res_card.add_widget(btn_details)

        self.main_layout.add_widget(res_card)
        self.main_layout.add_widget(self.btn_back)

    def go_to_spec_page(self, screen_name):
        if self.manager:
            self.manager.transition.direction = 'left'
            self.manager.current = screen_name

    def go_back(self, instance):
        if self.manager:
            self.manager.transition.direction = 'right'
            self.manager.current = 'menu'