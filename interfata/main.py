from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from start_page import StartPage
from menu_page import MenuPage

class StartScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.page = StartPage()
        self.add_widget(self.page)

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MenuPage())

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        start_screen = StartScreen(name="start")
        menu_screen = MenuScreen(name="menu")

        sm.add_widget(start_screen)
        sm.add_widget(menu_screen)

        # Legăm butonul de schimbarea ecranului
        start_screen.page.start_btn.bind(
            on_release=lambda *args: setattr(sm, "current", "menu")
        )

        return sm

if __name__ == "__main__":
    MyApp().run()
