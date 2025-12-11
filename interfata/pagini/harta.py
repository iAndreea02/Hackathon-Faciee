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

# --- AJUSTARE PATH ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(PROJECT_ROOT, "HARTA"))

from face.face_processor import FaceProcessor
from hands.hand_detector import HandDetector

# --- VARIABILE GLOBALE ---
shared_frame = None
shared_gesture = "NONE"
frame_lock = threading.Lock()
stop_camera_thread = threading.Event()

# --- PALETA DE CULORI ---
COLOR_CYAN      = get_color_from_hex("#00B5CC")
COLOR_MAGENTA   = get_color_from_hex("#E62B90")
COLOR_DARK_NAVY = get_color_from_hex("#050E23")
COLOR_PURPLE    = get_color_from_hex("#8E24AA")
COLOR_WHITE     = (1, 1, 1, 1)

# --- CLASA ROUNDED CARD ---
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

# --- THREAD CAMERA ---
def camera_control_thread(detector_h, detector_f):
    global shared_frame, shared_gesture, stop_camera_thread
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera nu poate fi deschisă!")
        stop_camera_thread.set()
        return
    while not stop_camera_thread.is_set():
        ret, frame = cap.read()
        if not ret: 
            time.sleep(0.01)
            continue
        
        frame = cv2.flip(frame, 1)
        results = detector_h.detect(frame)
        hand = detector_h.get_biggest_hand(results)
        gesture = detector_h.classify_gesture(hand)
        
        # Debug pe frame (opțional)
        cv2.putText(frame, f"GESTURE: {gesture}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        
        with frame_lock:
            shared_frame = frame
            shared_gesture = gesture
        
        time.sleep(1/30)
    cap.release()
    print("Camera thread oprit.")

# --- PAGINA HARTA ---
class MapPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hand_detector = HandDetector()
        self.face_detector = FaceProcessor()
        self.camera_thread_instance = None
        self.camera_is_running = False

        # Fundal
        with self.canvas.before:
            Color(*COLOR_DARK_NAVY)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg, size=self._update_bg)

        layout = FloatLayout()
        self.add_widget(layout)

        # 1. LAYER HARTA
        harta_img_path = os.path.join(PROJECT_ROOT, "HARTA", "assets", "harta_buna1.png")
        self.map_image = KivyImage(source=harta_img_path, size_hint=(None, None), size=(1200, 1000), pos=(0,0))
        self.map_image.size_hint = (2.0, 2.0) 
        self.map_image.allow_stretch = True
        layout.add_widget(self.map_image)

        # 2. LAYER ROBOT
        self.robot_pos_x = self.map_image.width / 2
        self.robot_pos_y = self.map_image.height / 2

        robot_img_path = os.path.join(PROJECT_ROOT, "HARTA", "assets", "robot_fata.png")
        self.robot_widget = KivyImage(source=robot_img_path, size_hint=(None,None), size=('80dp','80dp'),
                                      allow_stretch=True)
        self.robot_widget.center_x = Window.width / 2
        self.robot_widget.center_y = Window.height / 2
        layout.add_widget(self.robot_widget)

        # 3. UI (HUD)

        # --- A. LEGENDA GESTURI (Stânga Sus - Fără simboluri) ---
        legend_card = RoundedCard(bg_color=(0.02, 0.05, 0.14, 0.90), radius=15,
                                  has_border=True, border_color=COLOR_CYAN,
                                  size_hint=(None, None), size=(200, 170),
                                  pos_hint={'x': 0.02, 'top': 0.98})
        legend_card.orientation = 'vertical'
        legend_card.padding = [15, 15, 15, 15]
        legend_card.spacing = 5 
        
        # Titlu Legendă
        legend_card.add_widget(Label(text="LISTA COMENZI", bold=True, font_size='12sp', 
                                     color=COLOR_CYAN, size_hint_y=None, height=20, halign='left',
                                     text_size=(170, None)))
        
        # Grid Layout
        grid = GridLayout(cols=2, spacing=5, size_hint_y=1)
        
        def add_legend_row(gesture_name, action_name):
            # Col 1: Gestul (Magenta)
            lbl_g = Label(text=gesture_name, color=COLOR_MAGENTA, bold=True, font_size='11sp', 
                          halign='left', valign='middle')
            lbl_g.bind(size=lambda *x: lbl_g.setter('text_size')(lbl_g, (lbl_g.width, None)))
            grid.add_widget(lbl_g)
            
            # Col 2: Acțiunea (Alb) - FĂRĂ SĂGEATĂ
            lbl_a = Label(text=action_name, color=COLOR_WHITE, font_size='11sp', 
                          halign='left', valign='middle')
            lbl_a.bind(size=lambda *x: lbl_a.setter('text_size')(lbl_a, (lbl_a.width, None)))
            grid.add_widget(lbl_a)

        # Adăugăm rândurile curate
        add_legend_row("ROCK", "Stânga")
        add_legend_row("PEACE", "Dreapta")
        add_legend_row("LIKE", "Sus")
        add_legend_row("3 DEGETE", "Jos")
        add_legend_row("PALMĂ", "Stop")
        
        legend_card.add_widget(grid)
        layout.add_widget(legend_card)

        # --- B. CAMERA FEED (Dreapta Sus) ---
        cam_card = RoundedCard(bg_color=(0,0,0,1), radius=15,
                               has_border=True, border_color=COLOR_CYAN,
                               size_hint=(0.35, 0.25), 
                               pos_hint={'right': 0.98, 'top': 0.98})
        self.image_widget = KivyImage(allow_stretch=True, keep_ratio=True)
        cam_card.add_widget(self.image_widget)
        layout.add_widget(cam_card)

        # --- C. INFO PANEL (Jos Centru - Doar GEST) ---
        info_card = RoundedCard(bg_color=COLOR_DARK_NAVY, radius=20,
                                has_border=True, border_color=COLOR_MAGENTA,
                                size_hint=(0.6, 0.10),
                                pos_hint={'center_x': 0.5, 'y': 0.02})
        info_card.orientation = 'vertical'
        
        self.gesture_label = Label(text="AȘTEPTARE...", font_size='18sp', 
                                   bold=True, color=COLOR_WHITE, halign='center', valign='middle')
        self.gesture_label.bind(size=lambda *x: self.gesture_label.setter('text_size')(self.gesture_label, (self.gesture_label.width, None)))
        
        info_card.add_widget(self.gesture_label)
        layout.add_widget(info_card)

        # --- D. BUTON BACK (Stânga Jos) ---
        btn_back = Button(text="Înapoi", 
                          background_normal='', background_color=COLOR_MAGENTA,
                          color=COLOR_WHITE, bold=True, font_size='14sp',
                          size_hint=(None, None), size=(100, 40),
                          pos_hint={'x': 0.02, 'y': 0.02})
        btn_back.bind(on_release=lambda x: self.change_to_menu())
        layout.add_widget(btn_back)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_enter(self, *args):
        if not self.camera_is_running:
            stop_camera_thread.clear()
            self.camera_thread_instance = threading.Thread(target=camera_control_thread, args=(self.hand_detector, self.face_detector), daemon=True)
            self.camera_thread_instance.start()
            self.camera_is_running = True
            Clock.schedule_interval(self.update_kivy_ui, 1/30)

    def update_kivy_ui(self, dt):
        global shared_frame, shared_gesture
        gesture = shared_gesture
        map_step = 200*dt

        # Logica gesturi
        if gesture == "ROCK":       # Stânga
            self.robot_pos_x -= map_step
        elif gesture == "PEACE":    # Dreapta
            self.robot_pos_x += map_step
        elif gesture == "LIKE":     # Sus
            self.robot_pos_y += map_step
        elif gesture == "BACK":     # Jos
            self.robot_pos_y -= map_step
        elif gesture == "OPEN_PALM": # Stop
            pass

        # Limite robot
        self.robot_pos_x = max(0, min(self.robot_pos_x, 600))
        self.robot_pos_y = max(250, min(self.robot_pos_y, 750))

        # Zoom & Pan
        zoom_x = self.map_image.size[0] / Window.width
        zoom_y = self.map_image.size[1] / Window.height
        zoom_factor = min(zoom_x, zoom_y)

        map_x = Window.width/2 - self.robot_pos_x*zoom_factor
        map_y = Window.height/2 - self.robot_pos_y*zoom_factor

        map_x = min(0, max(map_x, Window.width - self.map_image.width*zoom_factor))
        map_y = min(0, max(map_y, Window.height - self.map_image.height*zoom_factor))

        self.map_image.pos = (map_x, map_y)
        self.robot_widget.center_x = Window.width/2
        self.robot_widget.center_y = Window.height/2

        # Update Label Gest
        gest_color = "00B5CC" # Cyan
        self.gesture_label.markup = True
        
        display_gest = gesture
        if gesture == "ROCK": display_gest = "ROCK (STANGA)"
        elif gesture == "PEACE": display_gest = "PEACE (DREAPTA)"
        elif gesture == "LIKE": display_gest = "LIKE (SUS)"
        elif gesture == "BACK": display_gest = "3 DEGETE (JOS)"
        elif gesture == "OPEN_PALM": display_gest = "PALMA (STOP)"
        
        self.gesture_label.text = f"GEST: [color={gest_color}]{display_gest}[/color]"

        # Update Camera
        with frame_lock:
            if shared_frame is None: return
            frame = shared_frame
        
        frame_flipped = cv2.flip(frame, 0)
        buf = frame_flipped.tobytes()
        texture = Texture.create(size=(frame_flipped.shape[1], frame_flipped.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
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
                self.camera_thread_instance.join(timeout=1)
            self.camera_is_running = False
            stop_camera_thread.clear()
            print("Camera oprită.")