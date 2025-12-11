from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import get_color_from_hex
import os

# --- PALETA CYBER / NEON ---
COLOR_BG = get_color_from_hex("#050E23")       # Navy (Fundal Ecran)
COLOR_CARD = get_color_from_hex("#0B1A3A")     # Navy ușor mai deschis (Fundal Card)
COLOR_CYAN = get_color_from_hex("#00B5CC")     # Cyan (Linii, Titluri)
COLOR_MAGENTA = get_color_from_hex("#E62B90")  # Magenta (Highlight)
COLOR_WHITE = (1, 1, 1, 1)

class TechCard(BoxLayout):
    """
    Card rectangular, stil 'bloc de date', foarte compact.
    """
    def __init__(self, title, text_content, accent_color=COLOR_CYAN, is_highlight=False, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        # Padding redus: [Stanga, Sus, Dreapta, Jos]
        self.padding = [10, 8, 10, 8] 
        self.spacing = 0
        
        # Desenare fundal și contur rectangular
        with self.canvas.before:
            # Alegem culorile
            if is_highlight:
                Color(0.2, 0.05, 0.15, 1) # Un fundal foarte închis roșiatic
                border_col = COLOR_MAGENTA
                line_w = 1.1
            else:
                Color(*COLOR_CARD)
                border_col = COLOR_CYAN
                line_w = 1.0

            # 1. Fundal DREPTUNGHIULAR (Fără colțuri rotunjite)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            
            # 2. Contur simplu
            Color(*border_col)
            self.line = Line(rectangle=(self.x, self.y, self.width, self.height), width=line_w)

        self.bind(pos=self._update_rect, size=self._update_rect)

        # Construcția textului (Titlu + Conținut într-un singur Label pentru economie de spațiu)
        # [size=13sp] micșorează textul corpului pentru a fi compact
        full_text = (
            f"[color={self.to_hex(accent_color)}][b]{title.upper()}[/b][/color]\n"
            f"[size=13sp]{text_content}[/size]"
        )

        lbl = Label(
            text=full_text,
            font_size='14sp', 
            color=COLOR_WHITE,
            markup=True,
            halign='left',
            valign='top',
            size_hint_y=None,
            line_height=1.15  # Liniile foarte apropiate
        )
        
        # Ajustare dimensiuni
        lbl.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        lbl.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        
        self.add_widget(lbl)

    def _update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size
        self.line.rectangle = (self.x, self.y, self.width, self.height)
        # Înălțime dinamică bazată strict pe text + padding mic
        if self.children:
            self.height = self.children[0].height + self.padding[1] + self.padding[3]

    def to_hex(self, color):
        return "#{:02x}{:02x}{:02x}".format(int(color[0]*255), int(color[1]*255), int(color[2]*255))


class AutomaticaPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Fundal
        with self.canvas.before:
            Color(*COLOR_BG)
            self.bg = Rectangle(pos=self.pos, size=self.size)
            
            # Grid decorativ subtil pe fundal (Opțional - stil tech)
            Color(1, 1, 1, 0.03) # Foarte transparent
            self.grid_line = Line(points=[0, 0, 0, 0]) # Placeholder

        self.bind(size=self._update_bg, pos=self._update_bg)

        main_layout = FloatLayout()
        self.add_widget(main_layout)

        # --- HEADER (Titlu) ---
        header = BoxLayout(size_hint=(1, 0.08), pos_hint={'top': 1})
        title_lbl = Label(
            text="AUTOMATICĂ ȘI INFORMATICĂ",
            font_size='19sp',
            bold=True,
            color=COLOR_CYAN,
            halign='center',
            valign='middle'
        )
        title_lbl.bind(size=title_lbl.setter('text_size'))
        header.add_widget(title_lbl)
        main_layout.add_widget(header)

        # --- SCROLL VIEW (Conținut) ---
        # Ocupă spațiul dintre header și footer
        scroll = ScrollView(
            size_hint=(0.94, 0.82), # 94% lățime (margini laterale mici)
            pos_hint={'center_x': 0.5, 'center_y': 0.51}
        )
        
        content_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=8 # Spațiu foarte mic între carduri (Compact)
        )
        content_box.bind(minimum_height=content_box.setter('height'))
        scroll.add_widget(content_box)
        main_layout.add_widget(scroll)

        # 1. Imagine (Compactă)
        img_path = os.path.join("imagini", "automatica.png")
        if os.path.exists(img_path):
            img = Image(
                source=img_path,
                size_hint_y=None,
                height=110, # Foarte scundă
                allow_stretch=True,
                keep_ratio=True
            )
            content_box.add_widget(img)

        # 2. Carduri Rectangulare

        content_box.add_widget(TechCard(
            title="Despre",
            text_content="Proiectezi sisteme automate și roboți care lucrează autonom."
        ))

        content_box.add_widget(TechCard(
            title="Oportunități",
            text_content="• Industrie 4.0 & Robotică\n• Cercetare și dezvoltare\n• Proiectare sisteme inteligente"
        ))

        content_box.add_widget(TechCard(
            title="Diplomă",
            text_content="[b]Inginer Automatică și Info. Aplicată[/b]\nÎnveți automatizarea sistemelor complexe și control industrial."
        ))

        # Highlight Card
        content_box.add_widget(TechCard(
            title="De ce să alegi asta?",
            text_content="Pasiune pentru roboți și tehnologie 'smart'? Aici lucrezi la proiecte reale care inovează viitorul.",
            accent_color=COLOR_MAGENTA,
            is_highlight=True
        ))
        
        # Buffer mic jos
        content_box.add_widget(Label(size_hint_y=None, height=5))

        # --- FOOTER (Buton) ---
        btn_back = Button(
            text="< ÎNAPOI MENIU",
            size_hint=(1, 0.08),
            pos_hint={'bottom': 1},
            background_normal='',
            background_color=COLOR_MAGENTA, # Buton plin pentru contrast
            color=COLOR_WHITE,
            font_size='14sp',
            bold=True
        )
        # Eliminăm fundalul default rotunjit al butonului dacă e cazul, 
        # dar background_normal='' rezolvă asta, făcându-l dreptunghiular.
        
        btn_back.bind(on_release=self.go_back)
        main_layout.add_widget(btn_back)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        # Linie decorativă orizontală sub titlu
        self.grid_line.points = [0, self.height*0.92, self.width, self.height*0.92]

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'