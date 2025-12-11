from kivy.config import Config
# Setările grafice trebuie să fie primele
Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '750')
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'fullscreen', '0')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition

# Importăm paginile principale
from start_page import StartPage
from menu_page import MenuPage
from tinder import TinderPage

# Importăm paginile departamentelor din folderul 'pagini'
from pagini.automatica import AutomaticaPage
from pagini.cti import CtiPage
from pagini.ieti import IetiPage
from pagini.electrica import ElectricaPage
from pagini.harta import MapPage

class MyApp(App):
    def build(self):
        # Folosim FadeTransition pentru un efect elegant
        sm = ScreenManager(transition=FadeTransition(duration=0.5))

        # Adăugăm paginile în ordinea logică
        sm.add_widget(StartPage(name="start"))
        sm.add_widget(MenuPage(name="menu"))
        
        # Paginile de departament
        # Numele ("automatica", "cti") trebuie să fie identice cu cele din menu_page.py -> self.specs
        sm.add_widget(AutomaticaPage(name="automatica"))
        sm.add_widget(CtiPage(name="cti"))
        sm.add_widget(IetiPage(name="ieti"))
        sm.add_widget(ElectricaPage(name="electrica"))

        sm.add_widget(TinderPage(name="tinder"))

        
        sm.add_widget(MapPage(name="harta"))

        return sm

if __name__ == "__main__":
    MyApp().run()