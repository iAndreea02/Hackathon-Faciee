from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image as KivyImage
from kivy.graphics.texture import Texture
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.core.window import Window
import os, sys, threading, time, cv2

# Ajustare path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(os.path.join(PROJECT_ROOT, "HARTA"))

from face.face_processor import FaceProcessor
from hands.hand_detector import HandDetector

# Variabile globale
shared_frame = None
shared_gesture = "NONE"
frame_lock = threading.Lock()
stop_camera_thread = threading.Event()

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
        cv2.putText(frame, f"GESTURE: {gesture}", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
        with frame_lock:
            shared_frame = frame
            shared_gesture = gesture
        time.sleep(1/30)
    cap.release()
    print("Camera thread oprit.")

class MapPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hand_detector = HandDetector()
        self.face_detector = FaceProcessor()
        self.camera_thread_instance = None
        self.camera_is_running = False

        self.bg_color = get_color_from_hex("#050E23")
        with self.canvas.before:
            Color(*self.bg_color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg, size=self._update_bg)

        layout = FloatLayout()
        self.add_widget(layout)

        # Harta (zoom păstrat)
        harta_img_path = os.path.join(PROJECT_ROOT, "HARTA", "assets", "harta_buna1.png")
        self.map_image = KivyImage(source=harta_img_path, size_hint=(2.0,2.0), pos=(0,0), allow_stretch=True)
        layout.add_widget(self.map_image)

        # Robot (poziție logică)
        self.robot_pos_x = self.map_image.width / 2
        self.robot_pos_y = self.map_image.height / 2

        robot_img_path = os.path.join(PROJECT_ROOT, "HARTA", "assets", "robot_fata.png")
        self.robot_widget = KivyImage(source=robot_img_path, size_hint=(None,None), size=('80dp','80dp'),
                                      center_x=Window.width/2, center_y=Window.height/2, allow_stretch=True)
        layout.add_widget(self.robot_widget)

        # Widget video
        self.image_widget = KivyImage(size_hint=(0.4,0.3), pos_hint={'right':0.98,'top':0.98}, allow_stretch=True)
        layout.add_widget(self.image_widget)

        # Label gesturi
        self.gesture_label = Label(text="GEST: NONE\nROBOT: Centrat", font_size='18sp', halign='center',
                                   size_hint=(1,0.1), pos_hint={'y':0.05}, color=get_color_from_hex("#00B5CC"))
        layout.add_widget(self.gesture_label)

        # Buton back
        btn = Button(text="Înapoi la Meniu", size_hint=(0.3,0.08), pos_hint={'left':0.02,'y':0.02})
        btn.bind(on_release=lambda x: self.change_to_menu())
        layout.add_widget(btn)

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
        if gesture in ["OPEN_PALM","NONE"]:
            pass
        elif gesture == "BACK":
            self.robot_pos_y -= map_step
        elif gesture == "LIKE":
            self.robot_pos_y += map_step
        elif gesture == "PEACE":
            self.robot_pos_x += map_step
        elif gesture == "ROCK":
            self.robot_pos_x -= map_step

        # Limite robot în coordonate hărții (restricții fixe)
        self.robot_pos_x = max(0, min(self.robot_pos_x, 600))   # dreapta maxim
        self.robot_pos_y = max(250, min(self.robot_pos_y, 750)) # jos/sus

        # Zoom pentru map + follow camera
        zoom_x = self.map_image.size[0] / Window.width
        zoom_y = self.map_image.size[1] / Window.height
        zoom_factor = min(zoom_x, zoom_y)

        # Poziția hărții astfel încât robotul să rămână centrat, dar să nu se vadă zone goale
        map_x = Window.width/2 - self.robot_pos_x*zoom_factor
        map_y = Window.height/2 - self.robot_pos_y*zoom_factor

        # Limite pentru a nu ieși cu harta
        map_x = min(0, max(map_x, Window.width - self.map_image.width*zoom_factor))
        map_y = min(0, max(map_y, Window.height - self.map_image.height*zoom_factor))

        self.map_image.pos = (map_x, map_y)

        # Robotul vizual centrat
        self.robot_widget.center_x = Window.width/2
        self.robot_widget.center_y = Window.height/2

        # Label
        self.gesture_label.text = f"GEST: {gesture}\nPOS X: {self.robot_pos_x:.0f} Y: {self.robot_pos_y:.0f}"

        # Video camera
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
