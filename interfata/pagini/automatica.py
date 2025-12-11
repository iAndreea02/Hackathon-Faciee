from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import get_color_from_hex
import os

# Definim culorile global pentru consistență
COLOR_BG = get_color_from_hex("#050E23")      # Navy
COLOR_CYAN = get_color_from_hex("#00B5CC")    # Cyan
COLOR_MAGENTA = get_color_from_hex("#E62B90") # Magenta
COLOR_WHITE = (1, 1, 1, 1)

class AutomaticaPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 1. Fundal Consistent
        with self.canvas.before:
            Color(*COLOR_BG)
            self.bg = Rectangle(pos=self.pos, size=self.size)
            # Element decorativ: Linie fină jos
            Color(*COLOR_CYAN)
            self.line = Line(points=[0, 100, 480, 100], width=1.2)
            
        self.bind(size=self._update_bg, pos=self._update_bg)

        layout = FloatLayout()
        self.add_widget(layout)

        # 2. Titlu Mare
        layout.add_widget(Label(
            text="AUTOMATICĂ ȘI\nINFORMATICĂ APLICATĂ",
            halign='center',
            font_size='26sp',
            bold=True,
            color=COLOR_CYAN,
            pos_hint={'center_x': 0.5, 'top': 0.92}
        ))

        # 3. Imagine Centrală (Specifică departamentului)
        # Asigură-te că imaginea automatica.png există în ../imagini/
        img_path = os.path.join("imagini", "automatica.png") 
        self.img = Image(
            source=img_path,
            size_hint=(0.5, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        layout.add_widget(self.img)

        # 4. Text Descriere
        desc_text = "Ingineria sistemelor complexe,\nroboți și control inteligent."
        layout.add_widget(Label(
            text=desc_text,
            halign='center',
            font_size='18sp',
            color=COLOR_WHITE,
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        ))

        # 5. Buton "ÎNAPOI" (Stil Cyber)
        btn_back = Button(
            text="< Meniu",
            size_hint=(0.35, 0.08),
            pos_hint={'x': 0.05, 'y': 0.03},
            background_normal='', # Elimină fundalul default
            background_color=COLOR_MAGENTA, # Buton Roz Neon
            color=COLOR_WHITE,
            font_size='18sp',
            bold=True
        )
        btn_back.bind(on_release=self.go_back)
        layout.add_widget(btn_back)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
        # Actualizăm linia decorativă să fie cât ecranul
        self.line.points = [0, self.height * 0.15, self.width, self.height * 0.15]

    def go_back(self, instance):
        # Tranziție inversă (dreapta) pentru efect natural
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'