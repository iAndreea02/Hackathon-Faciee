from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation
from kivy.graphics import Color, Rectangle


class StartPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # ---- BACKGROUND SOLID COLOR (FĂRĂ gradient) ----
        with self.canvas.before:
            Color(0/255, 14/255, 26/255, 1)  # #0A0E1A
            self.bg_rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self.update_bg, pos=self.update_bg)

        # ---- TITLE ----
        self.title = Label(
            text="Hello, viitor student!",
            font_size=38,
            color=(226/255, 26/255, 219/255, 1),
            size_hint=(1, None),
            height=50,
            pos_hint={"top": 0.92}
        )
        self.add_widget(self.title)

        # ---- SUBTITLE ----
        self.subtitle = Label(
            text="Facultatea ACIEE te așteaptă!",
            font_size=18,
            color=(0, 224/255, 255/255, 1),
            size_hint=(1, None),
            height=30,
            pos_hint={"top": 0.86}
        )
        self.add_widget(self.subtitle)

        # ---- ROBOT IMAGE ----
        self.robot = Image(
            source="robo.png",
            size_hint=(None, None),
            size=(250, 250),
            pos_hint={"center_x": 0.5},
            y=320
        )
        self.add_widget(self.robot)

        # ---- FLOATING ANIMATION ----
        self.animate_robot()

        # ---- BUTTON ----
        self.start_button = Button(
            text="Intră în aplicație",
            size_hint=(0.6, None),
            height=60,
            pos_hint={"center_x": 0.5, "y": 0.1},
            background_color=(226/255, 26/255, 219/255, 1),
            font_size=22,
            bold=True
        )
        self.add_widget(self.start_button)

    def update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def animate_robot(self):
        anim_up = Animation(y=self.robot.y + 25, duration=2.0, t="in_out_quad")
        anim_down = Animation(y=self.robot.y - 25, duration=2.0, t="in_out_quad")
        anim = anim_up + anim_down
        anim.repeat = True
        anim.start(self.robot)


class StartApp(App):
    def build(self):
        return StartPage()


if __name__ == "__main__":
    StartApp().run()
