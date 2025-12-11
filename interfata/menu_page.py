from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse
from kivy.animation import Animation
from kivy.clock import Clock
import math

class MenuPage(FloatLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # --- BACKGROUND ---
        with self.canvas:
            Color(0.02, 0.05, 0.14, 1)  # dark navy ACIEE
            self.bg = Ellipse(size=self.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)

        # --- CERC CENTRAL (sigla facultatii) ---
        self.center_circle = Image(
            source="logo.png",
            size_hint=(None, None),
            size=(200, 200),
            pos_hint={"center_x": 0.5, "center_y": 0.55}
        )
        self.add_widget(self.center_circle)

        # --- 4 CERCURI ROTITOARE (specializari) ---
        self.departments = [
            ("Calculatoare", "#00B5CC"),
            ("Automatică", "#E62B90"),
            ("Inginerie Electrică", "#8E24AA"),
            ("Telecomunicații", "#00B5CC")
        ]

        self.angle = 0
        self.circles = []
        self.radius = 250  # distanța față de centrul siglei

        for name, color_hex in self.departments:
            r, g, b = self.hex_to_rgb(color_hex)

            with self.canvas:
                Color(r, g, b, 1)
                circle = Ellipse(size=(120, 120))
            
            self.circles.append(circle)

        # actualizare poziție cercuri în fiecare frame
        Clock.schedule_interval(self.rotate_circles, 1/60)

    def rotate_circles(self, dt):
        """
        Roate cele 4 cercuri în jurul celui central
        """
        self.angle += 0.5
        cx = self.width / 2
        cy = self.height / 2 + 100

        for i, circle in enumerate(self.circles):
            angle_deg = self.angle + i * 90
            rad = math.radians(angle_deg)
            circle.pos = (
                cx + self.radius * math.cos(rad) - circle.size[0] / 2,
                cy + self.radius * math.sin(rad) - circle.size[1] / 2,
            )

    def update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos

    def hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) / 255 for i in (0, 2, 4))
