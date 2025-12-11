import cv2
import mediapipe as mp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex

# --- CONFIGURARE CULORI ---
CYAN = (0/255, 204/255, 255/255, 1)
MAGENTA = (255/255, 105/255, 180/255, 1)
DARK_NAVY = (20/255, 20/255, 40/255, 0.8)
PURPLE = (142/255, 36/255, 170/255, 0.9)
HIGHLIGHT_ALPHA = (255/255, 255/255, 255/255, 0.3) 

# --- DATA ---
questions = [
    {"question": "Dacă ar fi să alegi, ai prefera să fii un supererou al...",
     "options": ["Calculatoarelor și codului magic", "Luminilor și cablurilor electrice"]},
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
    "Calculatoarelor și codului magic": ["Calculatoare si Tehnologia Informatiei - Calculatoare", "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Rețele și Software de Telecomunicații"],
    "Luminilor și cablurilor electrice": ["Ingineria Sistemelor - Automatica si Informatica Aplicata", "Inginerie Electrică - Electromecanică", "Inginerie Electrică - Electronică de putere și acționări electrice", "Inginerie Electrică - Inginerie Electrică și Calculatoare", "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Electronică Aplicată"],
    "Stând la birou cu tastatura și cafeaua": ["Calculatoare si Tehnologia Informatiei - Calculatoare"],
    "Jucându-te cu roboți și circuite": ["Ingineria Sistemelor - Automatica si Informatica Aplicata", "Inginerie Electrică - Electromecanică", "Inginerie Electrică - Electronică de putere și acționări electrice"],
    "Puterea de a controla software-ul lumii": ["Calculatoare si Tehnologia Informatiei - Calculatoare", "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Rețele și Software de Telecomunicații"],
    "Puterea de a controla electronii și circuitele": ["Inginerie Electrică - Electromecanică", "Inginerie Electrică - Electronică de putere și acționări electrice", "Inginerie Electrică - Inginerie Electrică și Calculatoare", "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Electronică Aplicată"],
    "Hackathon cu prietenii": ["Calculatoare si Tehnologia Informatiei - Calculatoare", "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Rețele și Software de Telecomunicații"],
    "Construirea unui gadget nebunesc": ["Ingineria Sistemelor - Automatica si Informatica Aplicata", "Inginerie Electrică - Electromecanică", "Inginerie Electrică - Electronică de putere și acționări electrice", "Inginerie Electronică și Telecomunicații și Tehnologii informaționale - Electronică Aplicată"],
    "Mare (relaxare, cod și Wi-Fi)": ["Calculatoare si Tehnologia Informatiei - Calculatoare"],
    "Munte (provocări și circuite)": ["Ingineria Sistemelor - Automatica si Informatica Aplicata", "Inginerie Electrică - Electromecanică", "Inginerie Electrică - Electronică de putere și acționări electrice"]
}

# --- CLASE LOGICĂ ---
class FaceProcessor:
    def __init__(self):
        self.mp_face = mp.solutions.face_detection
        self.face_detector = self.mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5)
        self.mp_mesh = mp.solutions.face_mesh
        self.mesh = self.mp_mesh.FaceMesh(
            static_image_mode=False, max_num_faces=1, refine_landmarks=True,
            min_detection_confidence=0.5, min_tracking_confidence=0.5
        )

    def process(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        detections = self.face_detector.process(rgb)
        mesh_results = self.mesh.process(rgb)
        if not detections.detections:
            return None, mesh_results
        biggest_face = detections.detections[0]
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
        sensitivity = 1.15 # Sensibilitate ajustabilă
        if dist_left > dist_right * sensitivity: return "RIGHT" 
        elif dist_right > dist_left * sensitivity: return "LEFT"
        else: return "CENTER"
            
    def get_face_center_normalized(self, face_detection):
        if not face_detection: return None
        bbox = face_detection.location_data.relative_bounding_box
        return (bbox.xmin + bbox.width / 2, bbox.ymin + bbox.height / 2)

# --- CLASE UI ---
class OptionBox(BoxLayout):
    text = StringProperty("")
    color_hint = ListProperty([0, 0, 0, 0])
    is_highlighted = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.35, 0.12) # Ușor mai lat
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 2
        
        with self.canvas.before:
            Color(*DARK_NAVY)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size, radius=[10]) 
            self.highlight_color = Color(*HIGHLIGHT_ALPHA, a=0)
            self.highlight_rect = Rectangle(pos=self.pos, size=self.size, radius=[10])
            
        self.bind(pos=self._update_rect, size=self._update_rect)
        self.label = Label(text=self.text, halign='center', valign='middle', font_size='11sp', 
                           color=self.color_hint, markup=True, bold=True)
        self.bind(text=lambda i, v: setattr(self.label, 'text', v))
        self.add_widget(self.label)
        self.bind(is_highlighted=self.animate_highlight)

    def _update_rect(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.highlight_rect.pos = self.pos
        self.highlight_rect.size = self.size

    def animate_highlight(self, instance, value):
        anim = Animation(a=0.8 if value == 1 else 0.0, duration=0.2)
        anim.start(self.highlight_color)

class ResultBox(BoxLayout):
    def __init__(self, result_text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.7, 0.2)
        self.orientation = 'vertical'
        self.padding = 10
        with self.canvas.before:
            Color(*PURPLE)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=lambda *x: setattr(self.bg_rect, 'pos', self.pos),
                  size=lambda *x: setattr(self.bg_rect, 'size', self.size))

        self.label = Label(
            text=result_text,
            halign='center',
            valign='middle',
            font_size='16sp',
            color=CYAN,
            markup=True,
            bold=True
        )
        self.add_widget(self.label)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

# --------------------------------------------------------------------
# CameraQuizApp
# --------------------------------------------------------------------
class TinderPage(App):
    def build(self):
        self.index = 0
        self.selected_answers = []
        self.can_select = True
        self.quiz_finished = False
        self.result_widget = None

        self.face_processor = FaceProcessor()
        self.cap = None
        self.update_event = None

        # Layout Principal
        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

        # 1. Camera View
        self.camera_view = Image(size_hint=(1, 1), allow_stretch=True, keep_ratio=False)
        self.root_layout.add_widget(self.camera_view)
        
        # 2. Buton BACK (Foarte important pentru navigare)
        self.btn_back = Button(
            text="< Meniu",
            size_hint=(None, None), size=(100, 50),
            pos_hint={'x': 0.05, 'top': 0.95},
            background_normal='', background_color=MAGENTA
        )
        self.btn_back.bind(on_release=self.go_back)
        self.root_layout.add_widget(self.btn_back)

        # 3. Bottom Container
        self.bottom_container = BoxLayout(
            orientation='vertical', size_hint=(1, 0.25), 
            pos_hint={'bottom': 1}, padding=10, spacing=5
        )
        with self.bottom_container.canvas.before:
            Color(0, 0, 0, 0.7)
            self.bottom_rect = Rectangle(pos=self.bottom_container.pos, size=self.bottom_container.size)
        self.bottom_container.bind(pos=lambda *x: setattr(self.bottom_rect, 'pos', self.bottom_container.pos),
                                   size=lambda *x: setattr(self.bottom_rect, 'size', self.bottom_container.size))
        self.root_layout.add_widget(self.bottom_container)

        # Elemente UI
        self.progress_bar = ProgressBar(max=len(questions), value=0, size_hint=(1, None), height='10dp')
        self.bottom_container.add_widget(self.progress_bar)
        
        self.question_label = Label(text="Se încarcă...", font_size='18sp', color=CYAN, halign='center', bold=True)
        self.question_label.bind(size=self.question_label.setter('text_size')) # Text wrap
        self.bottom_container.add_widget(self.question_label)

        # Opțiuni Plutitoare
        self.option_left = OptionBox(text="Stanga", color_hint=CYAN)
        self.option_right = OptionBox(text="Dreapta", color_hint=MAGENTA)
        self.root_layout.add_widget(self.option_left)
        self.root_layout.add_widget(self.option_right)
        
        # Inițial ascunse
        self.option_left.pos = (-1000, -1000)
        self.option_right.pos = (-1000, -1000)
        self.result_widget = None

    def on_enter(self, *args):
        """Se apelează când utilizatorul intră pe această pagină."""
        self.index = 0
        self.selected_answers = []
        self.can_select = True
        self.quiz_finished = False
        
        # Resetare UI
        if self.result_widget:
            self.root_layout.remove_widget(self.result_widget)
            self.result_widget = None
        
        # Pornire Cameră
        self.cap = cv2.VideoCapture(0)
        
        # Pornire Loop
        self.update_event = Clock.schedule_interval(self.update, 1.0 / 30.0)
        Clock.schedule_once(self.start_quiz, 1)

    def on_leave(self, *args):
        """Se apelează când utilizatorul pleacă de pe pagină."""
        if self.update_event:
            self.update_event.cancel()
        if self.cap:
            self.cap.release()
            self.cap = None

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'

    def start_quiz(self, dt):
        self.show_question()

    def show_question(self):
        self.can_select = True
        self.progress_bar.value = self.index
        
        if self.index < len(questions):
            current_q = questions[self.index]
            self.question_label.text = current_q["question"]
            self.option_left.text = f"STÂNGA:\n{current_q['options'][0]}"
            self.option_right.text = f"DREAPTA:\n{current_q['options'][1]}"
            self.option_left.is_highlighted = 0
            self.option_right.is_highlighted = 0
        else:
            self.show_results()

    def update(self, dt):
        if not self.cap: return
        ret, frame = self.cap.read()
        if not ret: return
        
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape
        face, mesh = self.face_processor.process(frame)
        turn = self.face_processor.get_head_turn(mesh, width)
        face_center = self.face_processor.get_face_center_normalized(face)

        # UI Positioning Logic
        if face_center:
            face_x = face_center[0] * self.width
            face_y = (1.0 - face_center[1]) * self.height
            offset_y = 0.25 * self.height 
            pos_y = face_y + offset_y

            if self.quiz_finished and self.result_widget:
                 self.result_widget.center_x = face_x
                 self.result_widget.y = pos_y - self.result_widget.height / 2
            
            elif self.index < len(questions):
                spacing = 20
                self.option_left.right = face_x - spacing
                self.option_left.center_y = pos_y
                
                self.option_right.x = face_x + spacing
                self.option_right.center_y = pos_y
                
                if self.can_select:
                    current_q = questions[self.index]
                    if turn == "LEFT":
                        self.option_left.is_highlighted = 1
                        self.option_right.is_highlighted = 0
                        Clock.schedule_once(lambda x: self.select_answer(current_q["options"][0], "LEFT"), 1.2)
                    elif turn == "RIGHT":
                        self.option_right.is_highlighted = 1
                        self.option_left.is_highlighted = 0
                        Clock.schedule_once(lambda x: self.select_answer(current_q["options"][1], "RIGHT"), 1.2)
                    else:
                        self.option_left.is_highlighted = 0
                        self.option_right.is_highlighted = 0
                        Clock.unschedule(self.select_answer) # Oprește selecția dacă revine la centru
        else:
            # Hide if no face
            self.option_left.x = -1000
            self.option_right.x = -1000

        # Render Camera
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(width, height), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.camera_view.texture = texture

    def select_answer(self, answer, direction, dt=None): # dt e necesar pt Clock.schedule
        if not self.can_select: return
        
        # Verificare rapidă dacă capul e încă întors (opțional, pentru robustețe)
        self.can_select = False
        self.selected_answers.append(answer)
        self.index += 1
        Clock.schedule_once(lambda d: self.show_question(), 0.5)

    def show_results(self):
        self.quiz_finished = True
        self.option_left.x = -1000
        self.option_right.x = -1000
        self.question_label.text = "Gata! Vezi rezultatul deasupra capului."

        # Calcul Logică
        match_counts = {spec: 0 for spec in specializari}
        for ans in self.selected_answers:
            for spec in answers_map.get(ans, []):
                match_counts[spec] += 1
        
        best_spec = max(match_counts, key=match_counts.get) if match_counts else "Nedeterminat"
        percent = int((match_counts[best_spec] / len(questions)) * 100) if match_counts else 0
        
        final_txt = f"Ți se potrivește:\n[size=20sp]{best_spec}[/size]\n\nCompatibilitate: {percent}%"
        
        self.result_widget = ResultBox(final_txt)
        self.root_layout.add_widget(self.result_widget)