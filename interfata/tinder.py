import cv2
import mediapipe as mp
from kivy.app import App
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

# Culori (Păstrate pentru stilul modern)
CYAN = (0/255, 204/255, 255/255, 1)
MAGENTA = (255/255, 105/255, 180/255, 1)
DARK_NAVY = (20/255, 20/255, 40/255, 0.8)
PURPLE = (142/255, 36/255, 170/255, 0.9)
HIGHLIGHT_ALPHA = (255/255, 255/255, 255/255, 0.3) 

# Întrebări amuzante
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

# Lista specializări și Mapping (Păstrate)
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


# --------------------------------------------------------------------
# FaceProcessor (Rămâne neschimbat)
# --------------------------------------------------------------------
class FaceProcessor:
    def __init__(self):
        self.mp_face = mp.solutions.face_detection
        self.face_detector = self.mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5)
        self.mp_mesh = mp.solutions.face_mesh
        self.mesh = self.mp_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.drawer = mp.solutions.drawing_utils

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
        sensitivity = 1.15
        if dist_left > dist_right * sensitivity:
            return "RIGHT" 
        elif dist_right > dist_left * sensitivity:
            return "LEFT"
        else:
            return "CENTER"
            
    def get_face_center_normalized(self, face_detection):
        if not face_detection:
            return None
        bbox = face_detection.location_data.relative_bounding_box
        center_x = bbox.xmin + bbox.width / 2
        center_y = bbox.ymin + bbox.height / 2
        return (center_x, center_y)

# --------------------------------------------------------------------
# OptionBox (Widget pentru opțiuni)
# --------------------------------------------------------------------
class OptionBox(BoxLayout):
    text = StringProperty("")
    color_hint = ListProperty([0, 0, 0, 0])
    is_highlighted = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.30, 0.12)
        self.orientation = 'vertical'
        self.padding = 5
        self.spacing = 2
        self.highlight_ref = None

        with self.canvas.before:
            Color(*DARK_NAVY)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size, radius=[10, 10, 10, 10]) 
            self.bind(pos=self._update_rect, size=self._update_rect)

            self.highlight_color = Color(*HIGHLIGHT_ALPHA, a=0)
            self.highlight_rect = Rectangle(pos=self.pos, size=self.size, radius=[10, 10, 10, 10])
            self.highlight_ref = self.highlight_color

        self.label = Label(
            text=self.text,
            halign='center',
            valign='middle',
            font_size='12sp', 
            color=self.color_hint,
            markup=True,
            bold=True
        )
        self.add_widget(self.label)
        self.bind(text=self.label_update)
        self.bind(is_highlighted=self.animate_highlight)

    def _update_rect(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.highlight_rect.pos = self.pos
        self.highlight_rect.size = self.size

    def label_update(self, instance, value):
        self.label.text = value

    def animate_highlight(self, instance, value):
        if value == 1:
            anim = Animation(a=0.8, duration=0.1)
        else:
            anim = Animation(a=0.0, duration=0.2)
        
        anim.start(self.highlight_ref)

# --------------------------------------------------------------------
# ResultBox (Widget pentru rezultat)
# --------------------------------------------------------------------
class ResultBox(BoxLayout):
    def __init__(self, result_text, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 0.15)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 5

        with self.canvas.before:
            Color(*PURPLE)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size, radius=[10, 10, 10, 10])
            self.bind(pos=self._update_rect, size=self._update_rect)

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
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Eroare: Nu s-a putut deschide camera video.")
            return Label(text="Eroare: Camera indisponibilă.")

        self.root_layout = FloatLayout()

        # Widget camera (FullScreen)
        self.camera_view = Image(
            size_hint=(1, 1),
            allow_stretch=True, 
            keep_ratio=False
        )
        self.root_layout.add_widget(self.camera_view)
        
        # ----------------------------------------------------------------
        # Container BOTTOM pentru Întrebare + Progres (FIX)
        # ----------------------------------------------------------------
        self.bottom_container = BoxLayout(
            orientation='vertical',
            size_hint=(1, 0.20), # Ocupă 20% din înălțimea de jos
            pos_hint={'bottom': 1}, 
            padding=[10, 10, 10, 10],
            spacing=5
        )
        with self.bottom_container.canvas.before:
            Color(0, 0, 0, 0.6)
            self.bottom_rect = Rectangle(pos=self.bottom_container.pos, size=self.bottom_container.size)
            self.bottom_container.bind(pos=lambda *x: setattr(self.bottom_rect, 'pos', self.bottom_container.pos), 
                                    size=lambda *x: setattr(self.bottom_rect, 'size', self.bottom_container.size))

        # 1. Bara de Progres 
        self.progress_bar = ProgressBar(
            max=len(questions),
            value=0,
            size_hint=(0.95, None),
            height='5dp'
        )
        self.bottom_container.add_widget(self.progress_bar)
        
        # 2. Label Întrebare 
        self.question_label = Label(
            text="Pregătește-te...",
            font_size='18sp',
            color=CYAN,
            halign='center',
            valign='middle',
            size_hint=(1, 1),
            bold=True
        )
        self.bottom_container.add_widget(self.question_label)
        self.root_layout.add_widget(self.bottom_container)
        
        # Opțiunile (Dynamic - deasupra capului)
        self.option_left = OptionBox(
            text="Opțiunea 1",
            color_hint=CYAN
        )
        self.option_right = OptionBox(
            text="Opțiunea 2",
            color_hint=MAGENTA
        )
        self.root_layout.add_widget(self.option_left)
        self.root_layout.add_widget(self.option_right)
        
        self.option_left.pos = (-1000, -1000)
        self.option_right.pos = (-1000, -1000)
        
        Clock.schedule_once(self.start_quiz, 1)
        Clock.schedule_interval(self.update, 1 / 20)

        return self.root_layout
    
    def start_quiz(self, dt):
        self.show_question()

    def show_question(self):
        self.can_select = True
        self.progress_bar.value = self.index
        
        if self.index < len(questions):
            current_q = questions[self.index]
            self.question_label.text = current_q["question"]
            self.option_left.text = f"[b]STÂNGA:[/b]\n{current_q['options'][0]}"
            self.option_right.text = f"[b]DREAPTA:[/b]\n{current_q['options'][1]}"
            self.option_left.is_highlighted = 0
            self.option_right.is_highlighted = 0
        else:
            self.show_results()

    def update(self, dt):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = cv2.flip(frame, 1)
        height, width, _ = frame.shape

        face, mesh = self.face_processor.process(frame)
        turn = self.face_processor.get_head_turn(mesh, width)
        face_center_normalized = self.face_processor.get_face_center_normalized(face)

        # --------------------------------------------------------------------
        # NOU: Poziționarea Opțiunilor / Rezultatului Final (Deasupra capului)
        # --------------------------------------------------------------------
        if face_center_normalized:
            face_x_kivy = face_center_normalized[0] * Window.width
            face_y_kivy = (1.0 - face_center_normalized[1]) * Window.height
            
            # Ajustare: Mărim offset_y (0.30) pentru distanță mai mare între cap și opțiuni
            offset_y = 0.30 * Window.height 
            pos_y = face_y_kivy + offset_y

            if self.quiz_finished:
                # Cazul 1: Quiz-ul s-a terminat, mișcăm doar widget-ul rezultat
                if self.result_widget:
                    result_width, result_height = self.result_widget.size
                    # Centrare deasupra feței
                    self.result_widget.pos = (
                        face_x_kivy - result_width / 2, 
                        pos_y - result_height / 2
                    )
            
            elif self.index < len(questions):
                # Cazul 2: Quiz-ul este în desfășurare, mișcăm opțiunile
                
                spacing_x = 30 
                center_x = face_x_kivy
                
                left_x = center_x - self.option_left.width - spacing_x / 2
                right_x = center_x + spacing_x / 2

                # Poziționare (ținând cont de punctul de ancorare jos-stânga al widgetului Kivy)
                self.option_left.pos = (left_x, pos_y - self.option_left.height / 2)
                self.option_right.pos = (right_x, pos_y - self.option_right.height / 2)

                # Logică Quiz 
                if self.can_select:
                    current_q = questions[self.index]
                    
                    if turn == "LEFT":
                        self.option_left.is_highlighted = 1
                        self.option_right.is_highlighted = 0
                        Clock.schedule_once(lambda x: self.select_answer(current_q["options"][0], "LEFT"), 1.0) 
                    elif turn == "RIGHT":
                        self.option_right.is_highlighted = 1
                        self.option_left.is_highlighted = 0
                        Clock.schedule_once(lambda x: self.select_answer(current_q["options"][1], "RIGHT"), 1.0)
                    else:
                        self.option_left.is_highlighted = 0
                        self.option_right.is_highlighted = 0
                        Clock.unschedule(lambda x: self.select_answer(current_q["options"][0], "LEFT"))
                        Clock.unschedule(lambda x: self.select_answer(current_q["options"][1], "RIGHT"))
            
        else:
            # Ascunde opțiunile / rezultatul dacă fața nu este detectată
            if self.quiz_finished and self.result_widget:
                self.result_widget.pos = (-1000, -1000)
            elif self.index < len(questions):
                 self.option_left.pos = (-1000, -1000)
                 self.option_right.pos = (-1000, -1000)

        # Afișare Camera (Continuă să ruleze)
        buf = cv2.flip(frame, 0).tobytes()
        texture = Texture.create(size=(width, height), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.camera_view.texture = texture

    def select_answer(self, answer, direction):
        # Logica de re-verificare a poziției capului
        try:
            ret, check_frame = self.cap.read()
            if not ret: return
            check_frame = cv2.flip(check_frame, 1)
            check_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            face, mesh = self.face_processor.process(check_frame)
            current_turn = self.face_processor.get_head_turn(mesh, check_width)
        except Exception:
            return
            
        if (direction == "LEFT" and current_turn != "LEFT") or \
           (direction == "RIGHT" and current_turn != "RIGHT") or \
           (not self.can_select) or \
           (self.index >= len(questions)):
            return

        self.can_select = False
        self.selected_answers.append(answer)
        self.index += 1
        
        Clock.schedule_once(lambda dt: self.show_question(), 0.5)

    def show_results(self):
        self.quiz_finished = True
        
        # Eliminăm elementele UI de quiz de jos
        if self.bottom_container in self.root_layout.children:
            self.root_layout.remove_widget(self.bottom_container)
            
        self.root_layout.remove_widget(self.option_left)
        self.root_layout.remove_widget(self.option_right)

        # Calculăm match-ul
        match_counts = {spec: 0 for spec in specializari}
        for ans in self.selected_answers:
            for spec in answers_map.get(ans, []):
                match_counts[spec] += 1
        
        result_text = "Nu s-a putut determina specializarea."
        if match_counts:
            best_spec = max(match_counts, key=match_counts.get)
            total_questions = len(questions)
            best_score = match_counts[best_spec]
            percent = int((best_score / total_questions) * 100)
            result_text = f"[b]Specializarea ta:[/b]\n{best_spec}\n[b]Match: {percent}%[/b]"
        
        # Creăm widget-ul de rezultat dinamic (va fi poziționat în `update`)
        self.result_widget = ResultBox(result_text=result_text)
        self.root_layout.add_widget(self.result_widget)

    def on_stop(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()

# --------------------------------------------------------------------
if __name__ == "__main__":
    CameraQuizApp().run()