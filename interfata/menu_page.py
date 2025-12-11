from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.core.image import Image as CoreImage
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
import random
import os
import math

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "imagini")

# --- CULORI ---
COLOR_BG = get_color_from_hex("#050E23")
COLOR_CYAN = get_color_from_hex("#00B5CC")
COLOR_MAGENTA = get_color_from_hex("#E62B90")
COLOR_WHITE = (1, 1, 1, 1)

# --- CLASĂ PENTRU PARTICULE (Fundal stelat) ---
class Star:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, int(screen_width))
        self.y = random.randint(0, int(screen_height))
        self.size = random.uniform(1, 3)
        self.speed = random.uniform(0.2, 0.8)
        self.alpha = random.uniform(0.3, 0.8)

    def move(self, height):
        self.y += self.speed
        if self.y > height:
            self.y = 0
            self.x = random.randint(0, int(Window.width))

# --- BUTON CIRCULAR CU GLOW SI PULS ---
class CircleButton(ButtonBehavior, FloatLayout):
    def __init__(self, img_source, diameter_px, border_color=COLOR_CYAN, with_pulse=False, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (diameter_px, diameter_px)
        self.base_diameter = diameter_px
        self.with_pulse = with_pulse

        with self.canvas.before:
            Color(*border_color, 0.3)
            self._glow = Ellipse(pos=self.pos, size=self.size)

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

        if self.with_pulse:
            self.start_pulse()

    def _update(self, *args):
        self._ellipse.pos = self.pos
        self._ellipse.size = self.size
        radius = self.size[0] / 2
        self._border.circle = (self.center_x, self.center_y, radius + 2)
        glow_size = (self.size[0] * 1.2, self.size[1] * 1.2)
        self._glow.size = glow_size
        self._glow.pos = (self.center_x - glow_size[0]/2, self.center_y - glow_size[1]/2)

    def start_pulse(self):
        anim = Animation(size=(self.base_diameter * 1.1, self.base_diameter * 1.1), duration=1.5, t='in_out_sine') + \
               Animation(size=(self.base_diameter, self.base_diameter), duration=1.5, t='in_out_sine')
        anim.repeat = True
        anim.start(self)

# --- BUTON NAVIGARE STILIZAT ---
class NavButton(ButtonBehavior, BoxLayout):
    def __init__(self, text, icon_source=None, is_active=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [0, 10, 0, 10]
        self.spacing = 5
        
        txt_color = COLOR_MAGENTA if is_active else (0.6, 0.8, 0.9, 1)
        
        with self.canvas.before:
            if is_active:
                Color(*COLOR_MAGENTA)
                self.indicator = Line(points=[self.x, self.y, self.width, self.y], width=2)
        
        self.lbl = Label(text=text, font_size='13sp', color=txt_color, bold=True)
        self.add_widget(self.lbl)
        
        if is_active:
            self.bind(pos=self.update_indicator, size=self.update_indicator)

    def update_indicator(self, *args):
        line_w = self.width * 0.5
        center_x = self.x + self.width / 2
        self.indicator.points = [center_x - line_w/2, self.y + 5, center_x + line_w/2, self.y + 5]


class MenuPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.root = FloatLayout()
        self.add_widget(self.root)

        # 1. FUNDAL + PARTICULE
        self.stars = []
        with self.root.canvas.before:
            Color(*COLOR_BG)
            self._bg = Rectangle(size=self.size, pos=self.pos)
            Color(1, 1, 1, 0.6)
            self.star_instructions = []
            for i in range(30):
                self.star_instructions.append(Ellipse(size=(2,2)))
        
        # Orbita
        with self.root.canvas.before:
            Color(*COLOR_CYAN, 0.4)
            self._orbit_line = Line(width=1.5)

        self.bind(size=self._update_layout, pos=self._update_layout)

        # --- AICI AM ADĂUGAT TEXTUL DE BUN VENIT ---
        self.lbl_welcome = Label(
            text="BUN VENIT, VIITOR STUDENT!", 
            font_size='24sp', 
            bold=True, 
            color=COLOR_CYAN,
            size_hint=(1, 0.1),
            pos_hint={'top': 0.95} # Poziționat sus
        )
        self.root.add_widget(self.lbl_welcome)
        # -------------------------------------------

        # 2. SISTEMUL ORBITAL
        self.center_btn = CircleButton(os.path.join(IMAGES_DIR, "logo.png"), 120, border_color=COLOR_MAGENTA, with_pulse=True)
        self.root.add_widget(self.center_btn)

        self.specs = [
            ("automatica.png", "automatica"),
            ("cti.png", "cti"),
            ("inginerie_electrica.png", "electrica"),
            ("ieti.png", "ieti"),
        ]
        self.buttons = []
        for img, screen_name in self.specs:
            btn = CircleButton(os.path.join(IMAGES_DIR, img), 80, border_color=COLOR_CYAN)
            btn.bind(on_release=lambda x, s=screen_name: self.change_screen(s))
            self.root.add_widget(btn)
            self.buttons.append(btn)

        self.orbit_radius = 200
        self.angle_offset = 0
        Clock.schedule_interval(self.animate_all, 1/60)

        # 3. BARA NAVIGARE
        self.create_navbar()

    def create_navbar(self):
        navbar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'bottom': 1})
        with navbar.canvas.before:
            Color(0.02, 0.05, 0.1, 0.95)
            Rectangle(pos=navbar.pos, size=navbar.size)
            Color(*COLOR_CYAN)
            Line(points=[0, navbar.height, navbar.width, navbar.height], width=1)

        btn_spec = NavButton("Specializări", is_active=True)
        btn_map = NavButton("Hartă Campus")
        btn_map.bind(on_release=lambda x: self.change_screen('harta'))
        btn_quiz = NavButton("Ghid (Quiz)")
        btn_quiz.bind(on_release=lambda x: self.change_screen('tinder'))

        navbar.add_widget(btn_spec)
        navbar.add_widget(btn_map)
        navbar.add_widget(btn_quiz)
        
        self.root.add_widget(navbar)
        
        def update_navbar_bg(instance, value):
            navbar.canvas.before.clear()
            with navbar.canvas.before:
                Color(0.02, 0.05, 0.1, 0.95)
                Rectangle(pos=instance.pos, size=instance.size)
                Color(*COLOR_CYAN, 0.6)
                Line(points=[instance.x, instance.y + instance.height, instance.width, instance.y + instance.height], width=1.5)
        navbar.bind(pos=update_navbar_bg, size=update_navbar_bg)

    def _update_layout(self, *args):
        self._bg.size = self.size
        self._bg.pos = self.pos
        
        if not self.stars:
            for _ in range(len(self.star_instructions)):
                self.stars.append(Star(Window.width, Window.height))

        # Centrare buton soare (puțin mai jos pentru a face loc titlului)
        self.center_btn.center = (self.width/2, self.height/2 + 20)
        self._orbit_line.circle = (self.center_btn.center_x, self.center_btn.center_y, self.orbit_radius)

    def animate_all(self, dt):
        self.angle_offset += dt * 25
        cx, cy = self.center_btn.center
        for i, btn in enumerate(self.buttons):
            angle = math.radians(self.angle_offset + i * 90)
            btn.center_x = cx + math.cos(angle) * self.orbit_radius
            btn.center_y = cy + math.sin(angle) * self.orbit_radius

        if self.stars:
            for i, star in enumerate(self.stars):
                star.move(self.height)
                instr = self.star_instructions[i]
                instr.pos = (star.x, star.y)
                instr.size = (star.size, star.size)

    def change_screen(self, screen_name):
        if self.manager:
            self.manager.transition.direction = 'left'
            self.manager.current = screen_name