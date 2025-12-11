from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class ElectricaPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(
            Label(
                text="Pagina: Inginerie Electrică",
                font_size="40sp",
                halign="center",
                valign="middle"
            )
        )

        self.add_widget(layout)
