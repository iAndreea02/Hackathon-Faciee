from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex

class MapPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Fundal
        with self.canvas.before:
            Color(*get_color_from_hex("#050E23"))
            Rectangle(pos=self.pos, size=self.size)
            
        layout = FloatLayout()
        self.add_widget(layout)
        
        layout.add_widget(Label(text="Harta Campusului\n(În dezvoltare)", font_size='24sp', halign='center'))

        # Buton Back la Meniu
        btn = Button(text="Înapoi la Meniu", size_hint=(0.5, 0.1), pos_hint={'center_x':0.5, 'y':0.1})
        btn.bind(on_release=lambda x: setattr(self.manager, 'current', 'menu'))
        layout.add_widget(btn)