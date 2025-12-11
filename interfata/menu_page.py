from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
import os
import math

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "imagini")

# --- CULORI ---
COLOR_BG = get_color_from_hex("#050E23")
COLOR_CYAN = get_color_from_hex("#00B5CC")
COLOR_MAGENTA = get_color_from_hex("#E62B90")
COLOR_WHITE = (1, 1, 1, 1)

class CircleButton(ButtonBehavior, FloatLayout):
    """(Codul vechi pentru butoanele orbitale rămâne neschimbat aici)"""
    def __init__(self, img_source, diameter_px, border_color=COLOR_CYAN, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (diameter_px, diameter_px)

        with self.canvas:
            Color(1, 1, 1, 1)
            self._ellipse = Ellipse(pos=self.pos, size=self.size)
            Color(*border_color)
            self._border = Line(circle=(self.center_x, self.center_y, diameter_px/2 + 2), width=2)
        
        self.bind(pos=self._update, size=self._update)
        try:
            if os.path.exists(img_source):
                self._ellipse.texture = CoreImage(img_source).texture
        except: pass

    def _update(self, *args):
        self._ellipse.pos = self.pos
        self._ellipse.size = self.size
        radius = self.size[0] / 2
        self._border.circle = (self.center_x, self.center_y, radius + 2)

class NavButton(ButtonBehavior, BoxLayout):
    """Buton personalizat pentru bara de jos (Icon + Text)"""
    def __init__(self, text, icon_source=None, is_active=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 5
        
        # Culoare text: Magenta dacă e activ, Cyan dacă nu
        txt_color = COLOR_MAGENTA if is_active else COLOR_CYAN
        
        self.lbl = Label(text=text, font_size='14sp', color=txt_color, bold=True)
        self.add_widget(self.lbl)

class MenuPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = FloatLayout()
        self.add_widget(self.root)

        # 1. FUNDAL
        with self.root.canvas.before:
            Color(*COLOR_BG)
            self._bg = Rectangle(size=self.size, pos=self.pos)
            Color(*COLOR_CYAN, 0.2)
            self._orbit_line = Line(width=1.5)

        self.bind(size=self._update_layout, pos=self._update_layout)

        # 2. SISTEMUL ORBITAL (Butoane departamente)
        self.center_btn = CircleButton(os.path.join(IMAGES_DIR, "logo.png"), 120, border_color=COLOR_MAGENTA)
        self.root.add_widget(self.center_btn)

        self.specs = [
            ("automatica.png", "automatica"),
            ("cti.png", "cti"),
            ("electrica.png", "electrica"),
            ("ieti.png", "ieti"),
        ]
        self.buttons = []
        for img, screen_name in self.specs:
            btn = CircleButton(os.path.join(IMAGES_DIR, img), 80)
            btn.bind(on_release=lambda x, s=screen_name: self.change_screen(s))
            self.root.add_widget(btn)
            self.buttons.append(btn)

        self.orbit_radius = 200
        self.angle_offset = 0
        Clock.schedule_interval(self.animate_orbit, 1/60)

        # 3. BARA DE NAVIGARE JOS (NOU)
        self.create_navbar()

    def create_navbar(self):
        # Container bară
        navbar = BoxLayout(
            orientation='horizontal', 
            size_hint=(1, 0.1), # 10% din înălțime
            pos_hint={'bottom': 1}
        )
        
        # Desenăm fundalul barei
        with navbar.canvas.before:
            Color(0.02, 0.05, 0.1) # Un Navy foarte închis
            Rectangle(pos=navbar.pos, size=navbar.size)
            Color(*COLOR_CYAN) # Linie separatoare sus
            Line(points=[0, navbar.height, navbar.width, navbar.height], width=1)
            
        # --- BUTON 1: Specializări (Activ curent) ---
        btn_spec = NavButton("Specializări", is_active=True)
        # Nu face nimic, suntem deja aici
        
        # --- BUTON 2: Hartă ---
        btn_map = NavButton("Hartă Campus")
        btn_map.bind(on_release=lambda x: self.change_screen('harta'))
        
        # --- BUTON 3: Quiz/Tinder ---
        btn_quiz = NavButton("Ghid (Quiz)")
        btn_quiz.bind(on_release=lambda x: self.change_screen('tinder'))

        navbar.add_widget(btn_spec)
        navbar.add_widget(btn_map)
        navbar.add_widget(btn_quiz)
        
        self.root.add_widget(navbar)
        
        # Hack mic pentru a redesena fundalul barei la resize
        def update_navbar_bg(instance, value):
            navbar.canvas.before.clear()
            with navbar.canvas.before:
                Color(0.02, 0.05, 0.1, 1)
                Rectangle(pos=instance.pos, size=instance.size)
                Color(*COLOR_CYAN)
                Line(points=[instance.x, instance.y + instance.height, instance.width, instance.y + instance.height], width=1.5)
        navbar.bind(pos=update_navbar_bg, size=update_navbar_bg)

    def _update_layout(self, *args):
        self._bg.size = self.size
        self._bg.pos = self.pos
        self.center_btn.center = (self.width/2, self.height/2 + 50) # Ușor mai sus pentru a face loc barei
        self._orbit_line.circle = (self.center_btn.center_x, self.center_btn.center_y, self.orbit_radius)

    def animate_orbit(self, dt):
        self.angle_offset += dt * 25
        cx, cy = self.center_btn.center
        for i, btn in enumerate(self.buttons):
            angle = math.radians(self.angle_offset + i * 90)
            btn.center_x = cx + math.cos(angle) * self.orbit_radius
            btn.center_y = cy + math.sin(angle) * self.orbit_radius

    def change_screen(self, screen_name):
        self.manager.current = screen_name