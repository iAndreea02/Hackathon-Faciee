from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, LinearGradient
from kivy.animation import Animation
from kivy.core.window import Window

# Dimensiuni tip tabletă verticală
Window.size = (480, 800)

class GradientBackground(Widget):
    """Widget care desenează fundalul în gradient."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            self.grad = LinearGradient(
                (0, 0), (0, Window.height),
                (10/255, 14/255, 26/255, 1),   # #0A0E1A
                (0/255, 31/255, 48/255, 1)     # #001F30
            )
            self.rect = Rectangle(size=Window.size, pos=self.pos)

        self.bind(size=self._update, pos=self._update)

    def _update(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class StartPage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)

        # Fundal gradient
        self.bg = GradientBackground()
        self.add_widget(self.bg)

        # Layout de conținut peste fundal
        self.content = BoxLayout(orientation="vertical", spacing=10)
        self.add_widget(self.content)

        # TITLU
        title = Label(
            text="Hello, viitor student!",
            font_size=38,
            bold=True,
            color=(226/255, 26/255, 219/255, 1),  # #E21ADB
            size_hint=(1, None),
            height=60
        )
        self.content.add_widget(title)

        # SUBTITLU
        subtitle = Label(
            text="Facultatea ACIEE te așteaptă!",
            font_size=18,
            color=(0, 224/255, 255/255, 1),  # #00E0FF
            size_hint=(1, None),
            height=40
        )
        self.content.add_widget(subtitle)

        # ROBOT IMAGE
        self.robot = Image(
            source="robo.png",
            size_hint=(None, None),
            size=(260, 260),
            pos_hint={"center_x": 0.5}
        )
        self.content.add_widget(self.robot)

        # ANIMAȚIE FLOATING
        self.start_floating()

        # BUTON START
        start_btn = Button(
            text="Intră în aplicație",
            size_hint=(0.7, None),
            height=60,
            pos_hint={"center_x": 0.5},
            background_normal="",
            background_color=(226/255, 26/255, 219/255, 1),
            color=(1, 1, 1, 1),
            font_size=22,
            bold=True
        )
        self.content.add_widget(start_btn)

    def start_floating(self):
        """Robotul se ridică și coboară continuu."""
        anim_up = Animation(y=self.robot.y + 25, duration=2, t="in_out_quad")
        anim_down = Animation(y=self.robot.y - 25, duration=2, t="in_out_quad")
        anim = anim_up + anim_down
        anim.repeat = True
        anim.start(self.robot)


class MyApp(App):
    def build(self):
        return StartPage()


if __name__ == "__main__":
    MyApp().run()
