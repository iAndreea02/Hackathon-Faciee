from kivy.uix.screenmanager import Screen

class IetiPage(Screen):
    pass
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout


class IetiPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Pagina: IETI", font_size="40sp"))
        self.add_widget(layout)
