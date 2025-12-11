import cv2
import threading
import time
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

# --- Folosit DOAR pe Raspberry Pi ---
try:
    from picamera2 import Picamera2
    PICAMERA_AVAILABLE = True
except:
    PICAMERA_AVAILABLE = False


class CameraWidget(Image):
    pass


class CameraApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.frame_rgb = None
        self.capture_thread = None
        self.running = True

    def build(self):
        self.image_widget = CameraWidget()
        Clock.schedule_interval(self.update_kivy_ui, 1/30)
        self.start_camera_thread()
        return self.image_widget

    # -------------------------------------------------------------
    # THREAD CAMERA (OpenCV sau Picamera2)
    # -------------------------------------------------------------
    def start_camera_thread(self):
        self.capture_thread = threading.Thread(target=self.camera_loop, daemon=True)
        self.capture_thread.start()

    def camera_loop(self):
        if PICAMERA_AVAILABLE:
            # === PICAMERA2 (produce deja RGB corect!) ===
            cam = Picamera2()
            config = cam.create_preview_configuration(main={"format": "RGB888"})
            cam.configure(config)
            cam.start()
        else:
            # === WEBCAM OPENCV (produce BGR → trebuie convertit) ===
            cam = cv2.VideoCapture(0)

        while self.running:
            if PICAMERA_AVAILABLE:
                frame = cam.capture_array()
                # Picamera2 → DEJA în RGB (nu convertim)
                rgb = frame

            else:
                ret, frame = cam.read()
                if not ret:
                    continue

                # CONVERSIE CORECTĂ — OpenCV dă BGR
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # partajat către UI
            self.frame_rgb = rgb
            time.sleep(0.01)

        if not PICAMERA_AVAILABLE:
            cam.release()

    # -------------------------------------------------------------
    # UPDATE UI (convertim corect RGB → textura Kivy)
    # -------------------------------------------------------------
    def update_kivy_ui(self, dt):
        if self.frame_rgb is None:
            return

        frame = self.frame_rgb

        # Kivy necesită flip vertical!!!
        frame_flipped = cv2.flip(frame, 0)

        # textura RGB
        texture = Texture.create(size=(frame_flipped.shape[1],
                                       frame_flipped.shape[0]),
                                 colorfmt='rgb')

        texture.blit_buffer(frame_flipped.tobytes(),
                            colorfmt='rgb',
                            bufferfmt='ubyte')

        self.image_widget.texture = texture

    def on_stop(self):
        self.running = False



