from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Rectangle, Line, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.core.window import Window
import os, sys, threading, time, cv2
import numpy as np

# =========================================================================
# 1. PATH FIX
# =========================================================================
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
HARTA_ROOT = os.path.join(ROOT_DIR, "HARTA")
ASSETS_DIR = os.path.join(HARTA_ROOT, "assets")

if HARTA_ROOT not in sys.path:
    sys.path.append(HARTA_ROOT)

HARTA_PATH = os.path.join(ASSETS_DIR, "harta_buna1.png")
ROBOT_PATH = os.path.join(ASSETS_DIR, "robot_fata.png")

print(f"[PATH DEBUG] Harta path: {HARTA_PATH}")
print(f"[PATH DEBUG] Exista?: {os.path.exists(HARTA_PATH)}")

# =========================================================================

# --- IMPORTS ---
try:
    from face.face_processor import FaceProcessor
    from hands.hand_detector import HandDetector
except ImportError:
    class HandDetector: 
        def detect(self, img): return None
        def get_biggest_hand(self, res): return None
        def classify_gesture(self, hand): return "NONE"
    class FaceProcessor: pass

try:
    from picamera2 import Picamera2
    HAS_PICAMERA = True
except ImportError:
    HAS_PICAMERA = False

# --- GLOBALS ---
shared_frame = None
shared_gesture = "NONE"
frame_lock = threading.Lock()
stop_camera_thread = threading.Event()

# --- CULORI ---
COLOR_CYAN      = get_color_from_hex("#00B5CC")
COLOR_MAGENTA   = get_color_from_hex("#E62B90")
COLOR_DARK_NAVY = get_color_from_hex("#050E23")
COLOR_WHITE     = (1, 1, 1, 1)

# --- UI CLASS ---
class RoundedCard(BoxLayout):
    def __init__(self, bg_color, radius=15, padding_val=[10,10,10,10], 
                 has_border=False, border_color=None, **kwargs):
        super().__init__(**kwargs)
        self.padding = padding_val
        self.bg_color_rgba = bg_color
        self.radius_val = radius
        with self.canvas.before:
            Color(*self.bg_color_rgba)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
            if has_border and border_color:
                Color(*border_color)
                self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, radius), width=1.5)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = [self.radius_val]
        if hasattr(self, 'border'):
            self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius_val)

# --- THREAD CAMERA (COLOR FIX APPLIED) ---
def camera_control_thread(detector_h, detector_f):
    global shared_frame, shared_gesture, stop_camera_thread
    
    picam2 = None
    cap = None
    using_picamera = False

    # 1. Configurare Picamera2
    if HAS_PICAMERA:
        try:
            print("[CAM] Inițializare Picamera2...")
            picam2 = Picamera2()
            config = picam2.create_video_configuration(
                main={"size": (640, 480), "format": "BGR888"} 
            )
            picam2.configure(config)
            picam2.start()
            try:
                picam2.set_controls({"AwbMode": 0, "AeExposureMode": 0})
            except: pass
            time.sleep(2)
            using_picamera = True
            print("[CAM] Picamera2 pornită (Natural).")
        except Exception as e:
            print(f"[CAM ERROR] Picamera2 a eșuat: {e}. Trec pe OpenCV.")
            using_picamera = False
            if picam2: picam2.stop()

    # 2. Fallback OpenCV
    if not using_picamera:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return

    # --- LOOP ---
    while not stop_camera_thread.is_set():
        frame_bgr = None

        # Capture
        try:
            if using_picamera:
                frame_bgr = picam2.capture_array()
            else:
                ret, img = cap.read()
                if ret:
                    frame_bgr = img
        except:
            time.sleep(0.1)
            continue

        if frame_bgr is None:
            time.sleep(0.01)
            continue

        # BGR -> RGB corect
        frame_rgb = np.ascontiguousarray(frame_bgr[..., ::-1])

        # Flip orizontal (oglindă)
        frame_rgb = cv2.flip(frame_rgb, 1)

        # Procesare gesture
        try:
            results = detector_h.detect(frame_rgb)
            hand = detector_h.get_biggest_hand(results)
            gesture = detector_h.classify_gesture(hand)
        except:
            gesture = "NONE"

        # Debug vizual
        cv2.putText(frame_rgb, f"GEST: {gesture}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Trimite către UI
        with frame_lock:
            shared_frame = frame_rgb
            shared_gesture = gesture

        time.sleep(0.03)

    if using_picamera and picam2:
        try:
            picam2.stop()
            picam2.close()
        except: pass
    if cap: cap.release()

# --- PAGINA PRINCIPALĂ ---
class MapPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hand_detector = HandDetector()
        self.face_detector = FaceProcessor()
        self.camera_thread_instance = None
        self.camera_is_running = False

        with self.canvas.before:
            Color(*COLOR_DARK_NAVY)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size) 
            self.bind(pos=self._update_bg, size=self._update_bg)

        layout = FloatLayout()
        self.add_widget(layout)

        # 1. HARTA
        if os.path.exists(HARTA_PATH):
            self.map_image = KivyImage(source=HARTA_PATH, size_hint=(None, None), size=(1200, 1000), pos=(0,0))
        else:
            self.map_image = Label(text=f"HARTA NOT FOUND", color=COLOR_MAGENTA)
            
        self.map_image.size_hint = (2.0, 2.0) 
        self.map_image.allow_stretch = True
        self.map_image.keep_ratio = True
        layout.add_widget(self.map_image)

        # 2. ROBOT
        if os.path.exists(ROBOT_PATH):
            self.robot_widget = KivyImage(source=ROBOT_PATH, size_hint=(None,None), size=('80dp','80dp'), allow_stretch=True)
        else:
            self.robot_widget = Label(text="[R]", color=COLOR_CYAN)

        self.robot_pos_x = 1000 
        self.robot_pos_y = 1000
        self.robot_widget.center_x = Window.width / 2
        self.robot_widget.center_y = Window.height / 2
        layout.add_widget(self.robot_widget)

        # 3. UI
        legend_card = RoundedCard(bg_color=(0.02, 0.05, 0.14, 0.90), radius=15,
                                  has_border=True, border_color=COLOR_CYAN,
                                  size_hint=(None, None), size=(200, 170),
                                  pos_hint={'x': 0.02, 'top': 0.98})
        legend_card.orientation = 'vertical'
        legend_card.padding = [15, 15, 15, 15]
        legend_card.add_widget(Label(text="LISTA COMENZI", bold=True, font_size='12sp', 
                                     color=COLOR_CYAN, size_hint_y=None, height=20, halign='left', text_size=(170, None)))
        
        grid = GridLayout(cols=2, spacing=5, size_hint_y=1)
        def add_row(g, a):
            lbl_g = Label(text=g, color=COLOR_MAGENTA, bold=True, font_size='11sp', halign='left')
            lbl_g.bind(size=lambda *x: lbl_g.setter('text_size')(lbl_g, (lbl_g.width, None)))
            grid.add_widget(lbl_g)
            lbl_a = Label(text=a, color=COLOR_WHITE, font_size='11sp', halign='left')
            lbl_a.bind(size=lambda *x: lbl_a.setter('text_size')(lbl_a, (lbl_a.width, None)))
            grid.add_widget(lbl_a)

        add_row("ROCK", "Stânga")
        add_row("PEACE", "Dreapta")
        add_row("LIKE", "Sus")
        add_row("3 DEGETE", "Jos")
        add_row("PALMĂ", "Stop")
        legend_card.add_widget(grid)
        layout.add_widget(legend_card)

        info_card = RoundedCard(bg_color=COLOR_DARK_NAVY, radius=15,
                                has_border=True, border_color=COLOR_MAGENTA,
                                size_hint=(None, None), size=(200, 60),
                                pos_hint={'x': 0.02, 'top': 0.76})
        self.gesture_label = Label(text="AȘTEPTARE...", font_size='14sp', 
                                   bold=True, color=COLOR_WHITE, halign='center', valign='middle')
        info_card.add_widget(self.gesture_label)
        layout.add_widget(info_card)

        cam_card = RoundedCard(bg_color=(0,0,0,1), radius=15,
                               has_border=True, border_color=COLOR_CYAN,
                               size_hint=(0.35, 0.25), 
                               pos_hint={'right': 0.98, 'top': 0.98})
        self.image_widget = KivyImage(allow_stretch=True, keep_ratio=True)
        cam_card.add_widget(self.image_widget)
        layout.add_widget(cam_card)

        btn_back = Button(text="Înapoi", 
                          background_normal='', background_color=COLOR_MAGENTA,
                          color=COLOR_WHITE, bold=True, font_size='14sp',
                          size_hint=(None, None), size=(120, 45),
                          pos_hint={'center_x': 0.5, 'y': 0.03})
        btn_back.bind(on_release=lambda x: self.change_to_menu())
        layout.add_widget(btn_back)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_enter(self, *args):
        if not self.camera_is_running:
            stop_camera_thread.clear()
            self.camera_thread_instance = threading.Thread(
                target=camera_control_thread, 
                args=(self.hand_detector, self.face_detector), 
                daemon=True
            )
            self.camera_thread_instance.start()
            self.camera_is_running = True
            Clock.schedule_interval(self.update_kivy_ui, 1/30)

    def update_kivy_ui(self, dt):
        global shared_frame, shared_gesture

        # Gesturi + poziție robot
        gesture = shared_gesture
        map_step = 300 * dt
        if gesture == "ROCK": self.robot_pos_x -= map_step
        elif gesture == "PEACE": self.robot_pos_x += map_step
        elif gesture == "LIKE": self.robot_pos_y += map_step
        elif gesture == "BACK": self.robot_pos_y -= map_step
        self.robot_pos_x = max(100, min(self.robot_pos_x, 1900))
        self.robot_pos_y = max(100, min(self.robot_pos_y, 1900))
        center_x, center_y = Window.width / 2, Window.height / 2
        self.map_image.pos = (center_x - self.robot_pos_x, center_y - self.robot_pos_y)
        self.robot_widget.center = (center_x, center_y)

        # Update label
        gest_color = "00B5CC"
        self.gesture_label.markup = True
        display_gest = {"ROCK":"ROCK (STANGA)", "PEACE":"PEACE (DREAPTA)",
                        "LIKE":"LIKE (SUS)", "BACK":"3 DEGETE (JOS)",
                        "OPEN_PALM":"PALMA (STOP)"}.get(gesture, gesture)
        self.gesture_label.text = f"GEST: [color={gest_color}]{display_gest}[/color]"

        # Update imagine camera
        with frame_lock:
            if shared_frame is None: return
            frame = shared_frame.copy()
        # Convert RGB -> BGR, flip Y-axis, then back to RGB for Kivy display
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_flipped = np.ascontiguousarray(cv2.flip(frame_bgr, 0))
        frame_rgb = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)
        buf = frame_rgb.tobytes()
        texture = Texture.create(size=(frame_rgb.shape[1], frame_rgb.shape[0]), colorfmt='rgb')
        texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')
        self.image_widget.texture = texture

    def on_leave(self, *args):
        self.stop_camera_logic()

    def change_to_menu(self):
        self.stop_camera_logic()
        if self.manager:
            self.manager.transition.direction = 'right'
            self.manager.current = 'menu'

    def stop_camera_logic(self, *args):
        if self.camera_is_running:
            Clock.unschedule(self.update_kivy_ui)
            stop_camera_thread.set()
            if self.camera_thread_instance:
                self.camera_thread_instance.join(timeout=1.0)
            self.camera_is_running = False
            stop_camera_thread.clear()
            print("[GUI] Camera oprită.")
