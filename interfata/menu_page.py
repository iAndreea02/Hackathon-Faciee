from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import StringProperty, NumericProperty
from kivy.utils import get_color_from_hex

import os
import math

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "imagini")

# --- PALETA DE CULORI (ACIEE STYLE) ---
COLOR_BG = get_color_from_hex("#050E23")      # Dark Navy
COLOR_CYAN = get_color_from_hex("#00B5CC")    # Neon Cyan
COLOR_MAGENTA = get_color_from_hex("#E62B90") # Neon Magenta
COLOR_PURPLE = get_color_from_hex("#8E24AA")  # Accent Purple

class CircleButton(ButtonBehavior, FloatLayout):
    """Buton circular cu textură și bordură neon."""
    img_source = StringProperty("")
    
    def __init__(self, img_source, diameter_px, border_color=COLOR_CYAN, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (diameter_px, diameter_px)
        self.img_source = img_source

        with self.canvas:
            # 1. Imaginea butonului
            Color(1, 1, 1, 1) # Reset culoare pentru textură
            self._ellipse = Ellipse(pos=self.pos, size=self.size)
            
            # 2. Bordură Neon
            Color(*border_color) 
            self._border = Line(circle=(self.center_x, self.center_y, diameter_px/2 + 2), width=1.5)

        self.bind(pos=self._refresh, size=self._refresh)

        # Încărcare textură
        try:
            texture = CoreImage(self.img_source).texture
            self._ellipse.texture = texture
        except Exception as e:
            print(f"Eroare incarcare imagine {self.img_source}: {e}")

    def _refresh(self, *a):
        self._ellipse.pos = self.pos
        self._ellipse.size = self.size
        # Actualizare poziție bordură
        radius = self.size[0] / 2
        self._border.circle = (self.center_x, self.center_y, radius + 2)


class MenuPage(Screen):
    """Meniu central stilizat Cyberpunk/ACIEE."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.root = FloatLayout()
        self.add_widget(self.root)

        # 1. FUNDAL (Dark Navy)
        with self.root.canvas.before:
            Color(*COLOR_BG)
            self._bg = Rectangle(size=self.size, pos=self.pos)
            
            # Decor: Inel orbital subtil
            Color(*COLOR_CYAN, 0.3) # Cyan cu transparență
            self._orbit_ring = Line(circle=(self.center_x, self.center_y, 1), width=1.2)

        self.bind(size=self._update_bg, pos=self._update_bg)

        # 2. LOGO CENTRAL
        logo_size = 160 
        logo_path = os.path.join(IMAGES_DIR, "logo.png")
        # Logo are bordură Magenta pentru contrast
        self.center_logo = CircleButton(logo_path, logo_size, border_color=COLOR_MAGENTA)
        self.root.add_widget(self.center_logo)

        # Animație "Heartbeat" pentru logo
        pulse = (
            Animation(size=(logo_size * 1.05, logo_size * 1.05), d=1.5, t='in_out_sine') +
            Animation(size=(logo_size, logo_size), d=1.5, t='in_out_sine')
        )
        pulse.repeat = True
        pulse.start(self.center_logo)

        # 3. BUTOANE SPECIALIZĂRI
        self.specs = [
            ("automatica.png", "automatica"),
            ("cti.png", "cti"),
            ("inginerie_electrica.png", "electrica"), # Corectat ordinea sau numele fisierelor daca e cazul
            ("ieti.png", "ieti"), # Asumand ca acesta e fisierul pt electronica
        ]

        diameter = 90
        self.buttons = []
        
        # Plasăm butoanele
        for imgname, screen_name in self.specs:
            path = os.path.join(IMAGES_DIR, imgname)
            # Butoanele satelit au bordură Cyan
            btn = CircleButton(path, diameter, border_color=COLOR_CYAN)
            btn.screen_name = screen_name
            btn.bind(on_press=lambda i, n=screen_name: self._go(n))
            self.root.add_widget(btn)
            self.buttons.append(btn)

        # Setări orbită
        self.orbit_radius = 220 # Raza orbitei
        self.angles = [0, 90, 180, 270] # Distribuție egală
        self._time = 0
        
        # Pornire buclă de animație
        Clock.schedule_interval(self._update_positions, 1/60)

    def _update_bg(self, *a):
        """Redimensionează fundalul și inelul orbital la schimbarea ferestrei."""
        self._bg.size = self.size
        self._bg.pos = self.pos
        # Updatăm inelul decorativ să fie centrat
        self._orbit_ring.circle = (self.center_x, self.center_y, self.orbit_radius)

    def _go(self, name):
        if self.manager:
            self.manager.transition.direction = 'left'
            self.manager.current = name

    def _update_positions(self, dt):
        self._time += dt
        
        # CENTRARE DINAMICĂ (folosim self.width/height)
        cx = self.width / 2
        cy = self.height / 2

        # 1. Poziționare Logo Central
        self.center_logo.center = (cx, cy)

        # 2. Poziționare Sateliți
        # Viteza de rotație (mai mic = mai lent)
        omega = 360 / 12.0 

        for idx, btn in enumerate(self.buttons):
            # Calcul unghi curent
            angle = (self.angles[idx] + self._time * omega) % 360
            rad = math.radians(angle)

            # Calcul poziție pe cerc
            btn.center_x = cx + self.orbit_radius * math.cos(rad)
            btn.center_y = cy + self.orbit_radius * math.sin(rad)