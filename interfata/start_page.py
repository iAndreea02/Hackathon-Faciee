from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.graphics import Rectangle, Color
from kivy.utils import get_color_from_hex
import os

# Definim calea către imagini
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "imagini")

class StartPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 1. FUNDAL (Navy: #050E23)
        with self.canvas.before:
            Color(*get_color_from_hex("#050E23"))
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # 2. LOGO - COLȚ STÂNGA SUS (Fără animație)
        self.logo = Image(
            source=os.path.join(IMAGES_DIR, "logo.png"),
            size_hint=(None, None),
            size=(100, 100),
            pos_hint={"x": 0.02, "top": 0.98},
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.logo)

        # 3. TEXT PREZENTARE (Cu culori diferite folosind Markup)
        # Magenta: #E62B90 | Cyan: #00B5CC
        mesaj = (
            f"[color=#E62B90]Hello, viitor student![/color]\n\n"
            f"[color=#00B5CC]Facultatea de Automatică, Calculatoare,\n"
            f"Inginerie Electrică și Electronică[/color]"
        )

        self.label_msg = Label(
            text=mesaj,
            markup=True,         # Activăm interpretarea culorilor din text
            halign='center',     # Aliniere centru orizontal
            font_size="22sp",
            bold=True,
            line_height=1.2,     # Spațiere între rânduri
            size_hint=(0.9, None),
            pos_hint={"center_x": 0.5, "top": 0.85}
        )
        self.add_widget(self.label_msg)

        # 4. ROBOT ANIMAT (Centru, ușor mai jos)
        self.robot = Image(
            source=os.path.join(IMAGES_DIR, "robo.png"),
            size_hint=(None, None),
            size=(280, 280),
            pos_hint={"center_x": 0.5, "center_y": 0.48},
            allow_stretch=True
        )
        self.add_widget(self.robot)
        self._animate_robot()

        # 5. BUTON START (Magenta Neon)
        self.start_btn = Button(
            text="Intră în aplicație",
            size_hint=(0.6, None),
            height=70,
            pos_hint={"center_x": 0.5, "y": 0.1},
            background_normal="",  # Elimină fundalul gri implicit
            background_color=get_color_from_hex("#E62B90"),
            font_size="20sp",
            bold=True,
            color=get_color_from_hex("#050E23") # Textul butonului închis la culoare pentru contrast
        )
        # Legăm funcția de navigare
        self.start_btn.bind(on_release=self.go_next)
        self.add_widget(self.start_btn)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def _animate_robot(self):
        # Mișcare ușoară sus-jos (plutire)
        anim = Animation(pos_hint={"center_y": 0.50}, duration=1.5, t='in_out_sine') + \
               Animation(pos_hint={"center_y": 0.48}, duration=1.5, t='in_out_sine')
        anim.repeat = True
        anim.start(self.robot)

    def go_next(self, instance):
        if self.manager:
            self.manager.transition.direction = 'left'
            self.manager.current = 'menu'