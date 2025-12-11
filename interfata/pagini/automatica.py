from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle, Line
from kivy.utils import get_color_from_hex
import os

# --- DIMENSIUNE ECRAN (Testare) ---
# Window.size = (480, 850) # Poți decomenta pentru test pe PC

# --- CONFIGURARE CĂI (PATH FIX) ---
# 1. Aflăm unde este acest fișier (automatica.py -> în folderul 'pagini')
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Urcăm un nivel mai sus (în folderul 'interfata')
INTERFATA_DIR = os.path.dirname(CURRENT_DIR)

# 3. Construim calea către folderul 'imagini'
IMAGINI_DIR = os.path.join(INTERFATA_DIR, "imagini")

# --- DEBUG PATH ---
# print(f"Caut imagini in: {IMAGINI_DIR}")

# --- PALETA STRICTĂ ---
COLOR_CYAN = get_color_from_hex("#00B5CC")      # Titluri, Hero, Contururi
COLOR_MAGENTA = get_color_from_hex("#E62B90")   # Oportunități, Accente
COLOR_DARK_NAVY = get_color_from_hex("#050E23") # Fundal General
COLOR_PURPLE = get_color_from_hex("#8E24AA")    # Diplomă, Elemente secundare
COLOR_WHITE = (1, 1, 1, 1)

class RoundedCard(BoxLayout):
    """
    Card cu colțuri rotunjite. 
    Permite adăugarea unui contur (border) opțional.
    """
    def __init__(self, bg_color, radius=20, padding_val=[20, 20, 20, 20], has_border=False, border_color=None, **kwargs):
        super().__init__(**kwargs)
        self.padding = padding_val
        self.radius_val = radius
        self.bg_color_rgba = bg_color
        
        with self.canvas.before:
            Color(*self.bg_color_rgba)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[radius])
            
            # Desenare contur dacă este cerut
            if has_border and border_color:
                Color(*border_color)
                self.border = Line(rounded_rectangle=(self.x, self.y, self.width, self.height, radius), width=1.5)
        
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.rect.radius = [self.radius_val]
        
        # Actualizare contur dacă există
        if hasattr(self, 'border'):
            self.border.rounded_rectangle = (self.x, self.y, self.width, self.height, self.radius_val)

class AutomaticaPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # --- FUNDAL DARK NAVY ---
        with self.canvas.before:
            Color(*COLOR_DARK_NAVY)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[0])
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', spacing=10)
        self.add_widget(main_layout)

        # --- HEADER ---
        header = GridLayout(cols=2, size_hint_y=None, height=100, padding=[20, 20, 20, 0])
        
        # 1. Text Header
        text_box = BoxLayout(orientation='vertical', spacing=5)
        lbl_salut = Label(text="BUNĂ ZIUA,", font_size='14sp', color=COLOR_CYAN, halign='left', size_hint_y=None, height=20)
        lbl_salut.bind(size=lambda *x: lbl_salut.setter('text_size')(lbl_salut, (lbl_salut.width, None)))
        
        lbl_nume = Label(text="Viitor Inginer AIA", font_size='26sp', bold=True, color=COLOR_WHITE, halign='left')
        lbl_nume.bind(size=lambda *x: lbl_nume.setter('text_size')(lbl_nume, (lbl_nume.width, None)))
        
        text_box.add_widget(lbl_salut)
        text_box.add_widget(lbl_nume)
        header.add_widget(text_box)

        # 2. Logo Header (MODIFICAT)
        logo_container = BoxLayout(size_hint_x=None, width=80, padding=[0, 0, 0, 10])
        
        # Folosim calea absolută calculată sus
        img_path = os.path.join(IMAGINI_DIR, "automatica.png")
        
        if os.path.exists(img_path):
            logo = Image(source=img_path, allow_stretch=True, keep_ratio=True)
            logo_container.add_widget(logo)
        else:
            # Fallback text
            print(f"[EROARE] Nu gasesc imaginea la: {img_path}")
            logo_container.add_widget(Label(text="[AIA]", color=COLOR_CYAN, bold=True))
            
        header.add_widget(logo_container)
        main_layout.add_widget(header)

        # --- ZONA SCROLLABILĂ ---
        scroll = ScrollView(size_hint=(1,1), bar_width=0)
        content = BoxLayout(orientation='vertical', size_hint_y=None, padding=[20, 10, 20, 20], spacing=20)
        content.bind(minimum_height=content.setter('height'))
        scroll.add_widget(content)
        main_layout.add_widget(scroll)

        # --- 1. CARD DIPLOMĂ (PURPLE) ---
        info_card = RoundedCard(bg_color=COLOR_PURPLE, size_hint_y=None, height=110)
        info_card.orientation = 'vertical'
        info_card.spacing = 5
        
        info_card.add_widget(Label(text="SPECIALIZAREA TA", color=(1,1,1,0.7), font_size='12sp', bold=True, halign='left', size_hint_y=None, height=20))
        
        lbl_dip = Label(text="Inginer în Automatică și Informatică Aplicată", color=COLOR_WHITE, font_size='18sp', bold=True, halign='left', valign='top')
        lbl_dip.bind(size=lambda *x: lbl_dip.setter('text_size')(lbl_dip, (lbl_dip.width, None)))
        info_card.add_widget(lbl_dip)
        content.add_widget(info_card)

        # --- 2. HERO CARD (CYAN) ---
        hero_card = RoundedCard(bg_color=COLOR_CYAN, size_hint_y=None, height=180)
        hero_card.orientation = 'vertical'
        hero_card.spacing = 10
        
        lbl_hero_t = Label(text="Sisteme care gândesc singure", font_size='22sp', bold=True, color=COLOR_WHITE, halign='left', size_hint_y=None, height=35)
        lbl_hero_t.bind(size=lambda *x: lbl_hero_t.setter('text_size')(lbl_hero_t, (lbl_hero_t.width, None)))
        hero_card.add_widget(lbl_hero_t)
        
        hero_desc = "Vei învăța să proiectezi sisteme automate și roboți independenți. De la brațe robotice industriale, până la case inteligente și mașini autonome."
        lbl_hero_d = Label(text=hero_desc, font_size='15sp', color=COLOR_WHITE, halign='left', valign='top', line_height=1.4)
        lbl_hero_d.bind(width=lambda *x: lbl_hero_d.setter('text_size')(lbl_hero_d, (lbl_hero_d.width, None)))
        hero_card.add_widget(lbl_hero_d)
        content.add_widget(hero_card)

        # --- 3. GRID CARDS ---
        grid = GridLayout(cols=2, spacing=15, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        def create_clean_card(bg_col, title, items, height=220):
            card = RoundedCard(bg_color=bg_col, size_hint_y=None, height=height)
            card.orientation = 'vertical'
            
            # Titlu
            lbl_t = Label(text=title.upper(), color=COLOR_WHITE, bold=True, font_size='14sp', size_hint_y=None, height=30, halign='left')
            lbl_t.bind(size=lambda *x: lbl_t.setter('text_size')(lbl_t, (lbl_t.width, None)))
            card.add_widget(lbl_t)
            
            # Spatiu
            card.add_widget(Label(size_hint_y=None, height=10))

            # Lista
            clean_text = ""
            for item in items:
                clean_text += f"- {item}\n\n"
            
            lbl_body = Label(text=clean_text, color=COLOR_WHITE, font_size='13sp', halign='left', valign='top')
            lbl_body.bind(size=lambda *x: lbl_body.setter('text_size')(lbl_body, (lbl_body.width, None)))
            card.add_widget(lbl_body)
            
            return card

        # Stânga: MAGENTA
        opts = ["Joburi în robotică", "Industrie 4.0", "Colaborări fabrici", "Proiecte Smart"]
        grid.add_widget(create_clean_card(COLOR_MAGENTA, "Oportunități", opts))

        # Dreapta: PURPLE (Refolosim Purple pentru că Orange nu e în paletă)
        learn = ["Automatizări", "Control inteligent", "Programare AI", "Electronică"]
        grid.add_widget(create_clean_card(COLOR_PURPLE, "Ce vei studia", learn))
        
        content.add_widget(grid)

        # --- 4. MESAJ FINAL (DARK NAVY cu Border CYAN) ---
        # Folosim Dark Navy pentru fundal, dar adăugăm un border Cyan ca să se vadă.
        msg_card = RoundedCard(
            bg_color=COLOR_DARK_NAVY, 
            size_hint_y=None, 
            height=160,
            has_border=True,
            border_color=COLOR_CYAN
        )
        msg_card.orientation = 'vertical'
        msg_card.spacing = 5
        
        msg_card.add_widget(Label(text="DE CE SĂ ALEGI AIA?", color=COLOR_CYAN, bold=True, font_size='14sp', size_hint_y=None, height=25, halign='center'))
        
        txt_final = "Dacă ești pasionat de tehnologie și vrei să înțelegi cum se configurează viitorul, aceasta este specializarea potrivită pentru tine."
        lbl_msg = Label(text=txt_final, font_size='15sp', color=COLOR_WHITE, halign='center', valign='middle', line_height=1.3)
        lbl_msg.bind(size=lambda *x: lbl_msg.setter('text_size')(lbl_msg, (lbl_msg.width, None)))
        msg_card.add_widget(lbl_msg)
        
        content.add_widget(msg_card)

        # --- BUTON ÎNAPOI ---
        bottom_bar = BoxLayout(size_hint_y=None, height=70, padding=[20, 10, 20, 10])
        btn_back = Button(text="Înapoi la Meniu", background_normal='', background_color=COLOR_MAGENTA, color=COLOR_WHITE, bold=True)
        btn_back.bind(on_release=self.go_back)
        bottom_bar.add_widget(btn_back)
        main_layout.add_widget(bottom_bar)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def go_back(self, instance):
        if self.manager:
            self.manager.transition.direction = 'right'
            self.manager.current = 'menu'