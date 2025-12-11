from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.graphics import Rectangle, Color

class StartPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # FUNDAL ALBASTRU BLEU-MARIN (#050E23)
        with self.canvas:
            Color(0.02, 0.06, 0.14, 1)   # culoarea exactă #050E23
            self.bg = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # LOGO SUS STÂNGA
        self.logo = Image(
            source="logo.png",
            size_hint=(None, None),
            size=(120, 120),             # suficient pentru tabletă
            pos_hint={"x": 0.02, "top": 0.98},
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.logo)

        # TITLU (cyan neon #00B5CC)
        self.title = Label(
            text="Hello, viitor student!",
            font_size="42sp",
            bold=True,
            color=(0, 181/255, 204/255, 1),     # #00B5CC
            size_hint=(1, None),
            height=140,
            pos_hint={"center_x": 0.5, "top": 0.8}
        )
        self.add_widget(self.title)

        # SUBTITLU (cyan / magenta?)
        self.subtitle = Label(
            text="Facultatea ACIEE te așteaptă!",
            font_size="24sp",
            color=(230/255, 43/255, 144/255, 1),   # magenta #E62B90
            size_hint=(1, None),
            height=80,
            pos_hint={"center_x": 0.5, "top": 0.73}
        )
        self.add_widget(self.subtitle)

        # ROBOT ANIMAT (în centru)
        self.robot = Image(
            source="robo.png",
            size_hint=(None, None),
            size=(300, 300),
            pos_hint={"center_x": 0.5, "center_y": 0.46},
            allow_stretch=True,
            keep_ratio=True
        )
        self.add_widget(self.robot)

        # BUTON (magenta neon #E62B90)
        self.start_btn = Button(
            text="Intră în aplicație",
            size_hint=(0.7, None),
            height=80,
            pos_hint={"center_x": 0.5, "y": 0.08},
            background_normal="",
            background_color=(230/255, 43/255, 144/255, 1),  # #E62B90
            font_size=26
        )
        self.add_widget(self.start_btn)

        # Animație robot
        self._animate_robot()

    def _animate_robot(self):
        anim_up = Animation(pos_hint={"center_y": 0.49}, duration=2, t='in_out_quad')
        anim_down = Animation(pos_hint={"center_y": 0.46}, duration=2, t='in_out_quad')
        anim_up += anim_down
        anim_up.repeat = True
        anim_up.start(self.robot)

    def _update_bg(self, *args):
        self.bg.size = self.size
        self.bg.pos = self.pos
