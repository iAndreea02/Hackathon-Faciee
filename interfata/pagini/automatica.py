from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Line
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivy.clock import Clock
import os

# --- PALETA CYBER ---
COLOR_BG = get_color_from_hex("#050E23")       # Deep Navy
COLOR_CARD_BG = (0.04, 0.1, 0.23, 0.85)        # Navy Transparent (Glass effect)
COLOR_CYAN = get_color_from_hex("#00B5CC")     # Cyan Neon
COLOR_MAGENTA = get_color_from_hex("#E62B90")  # Magenta Neon
COLOR_WHITE = (1, 1, 1, 1)

class CyberCard(BoxLayout):
    """
    Card stil 'HUD' cu colțuri marcate (Brackets) în loc de chenar complet.
    Include animație de apariție (Fade + Slide Up).
    """
    def __init__(self, title, text_content, accent_color=COLOR_CYAN, delay=0, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.padding = [15, 12, 15, 12]
        self.spacing = 2
        
        # Inițial invizibil pentru animație
        self.opacity = 0 
        self.anim_delay = delay
        self.accent_col = accent_color

        # Desenare grafică Cyber
        with self.canvas.before:
            # 1. Fundal semi-transparent
            Color(*COLOR_CARD_BG)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            
            # 2. Colțuri (Brackets) - stil HUD
            Color(*accent_color)
            self.lines = []
            # Vom actualiza punctele în _update_rect, aici doar inițializăm instrucțiunile
            self.line_tl = Line(width=1.5) # Top Left
            self.line_tr = Line(width=1.5) # Top Right
            self.line_bl = Line(width=1.5) # Bottom Left
            self.line_br = Line(width=1.5) # Bottom Right

        self.bind(pos=self._update_rect, size=self._update_rect)

        # Construcția textului
        full_text = (
            f"[color={self.to_hex(accent_color)}][b]>> {title.upper()}[/b][/color]\n"
            f"[size=13sp]{text_content}[/size]"
        )

        lbl = Label(
            text=full_text,
            font_size='15sp', 
            color=COLOR_WHITE,
            markup=True,
            halign='left',
            valign='top',
            size_hint_y=None,
            line_height=1.2
        )
        lbl.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        lbl.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        self.add_widget(lbl)

    def _update_rect(self, *args):
        x, y, w, h = self.x, self.y, self.width, self.height
        self.rect.pos = (x, y)
        self.rect.size = (w, h)
        
        # Lungimea brațului colțului
        d = 15 
        
        # Desenăm colțurile "tech"
        self.line_tl.points = [x, y+h-d, x, y+h, x+d, y+h]       # Stânga-Sus
        self.line_tr.points = [x+w-d, y+h, x+w, y+h, x+w, y+h-d] # Dreapta-Sus
        self.line_bl.points = [x, y+d, x, y, x+d, y]             # Stânga-Jos
        self.line_br.points = [x+w-d, y, x+w, y, x+w, y+d]       # Dreapta-Jos
        
        # Înălțime dinamică
        if self.children:
            self.height = self.children[0].height + self.padding[1] + self.padding[3]

    def animate_in(self):
        # Reset poziție ușor mai jos pentru efectul de "slide up"
        original_y = self.y
        # self.y -= 30 # (Kivy layout engines se luptă cu animarea pos-ului direct, folosim opacitate pt siguranță)
        
        # Animație simplă de opacitate cu delay
        anim = Animation(opacity=1, duration=0.6, t='out_quart')
        Clock.schedule_once(lambda dt: anim.start(self), self.anim_delay)

    def to_hex(self, color):
        return "#{:02x}{:02x}{:02x}".format(int(color[0]*255), int(color[1]*255), int(color[2]*255))


class AutomaticaPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cards = [] # Listă pentru a stoca cardurile pt animație
        
        # 1. Fundal Activ
        with self.canvas.before:
            Color(*COLOR_BG)
            self.bg = Rectangle(pos=self.pos, size=self.size)
            
            # --- EFECT DINAMIC: Scanner Line ---
            Color(*COLOR_CYAN)
            Color(0, 0.71, 0.8, 0.15) # Cyan transparent
            self.scanner = Rectangle(size=(0, 2), pos=(0,0)) # Inițial invizibil

        self.bind(size=self._update_bg, pos=self._update_bg)

        main_layout = FloatLayout()
        self.add_widget(main_layout)

        # --- HEADER ---
        header = BoxLayout(size_hint=(1, 0.08), pos_hint={'top': 1})
        # Titlu cu font 'monospaced' simulat (daca fontul default permite) sau Bold Tech
        title_lbl = Label(
            text="[ SYSTEM: AUTOMATICA_MODULE ]", # Stil terminal
            font_size='16sp',
            bold=True,
            color=COLOR_CYAN,
            markup=True
        )
        header.add_widget(title_lbl)
        main_layout.add_widget(header)

        # --- CONTENT SCROLL ---
        scroll = ScrollView(
            size_hint=(0.96, 0.82),
            pos_hint={'center_x': 0.5, 'center_y': 0.51}
        )
        
        self.content_box = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=[0, 10, 0, 10]
        )
        self.content_box.bind(minimum_height=self.content_box.setter('height'))
        scroll.add_widget(self.content_box)
        main_layout.add_widget(scroll)

        # --- ADĂUGARE ELEMENTE ---
        
        # Imaginea
        img_path = os.path.join("imagini", "automatica.png")
        if os.path.exists(img_path):
            img = Image(
                source=img_path,
                size_hint_y=None,
                height=120,
                allow_stretch=True,
                keep_ratio=True,
                opacity=0 # Start invizibil
            )
            self.content_box.add_widget(img)
            self.img_widget = img
        
        # Creăm cardurile și le salvăm referința
        card_data = [
            ("Misiune", "Proiectarea sistemelor care gândesc singure. Roboți, senzori, inteligență.", COLOR_CYAN),
            ("Oportunități", "• Industrie 4.0 & Automotive\n• Dezvoltare Software Industrial\n• Robotică Avansată", COLOR_CYAN),
            ("Diplomă", "[b]Inginer Automatică[/b]\nSpecialist în controlul proceselor complexe.", COLOR_WHITE),
            ("Mesaj Liceeni", "Tehnologia e terenul tău de joacă? Hai să construim viitorul împreună!", COLOR_MAGENTA)
        ]

        # Generăm cardurile cu delay progresiv
        delay_step = 0.2
        current_delay = 0.3
        
        for title, text, col in card_data:
            c = CyberCard(title=title, text_content=text, accent_color=col, delay=current_delay)
            self.content_box.add_widget(c)
            self.cards.append(c)
            current_delay += delay_step

        # Buffer jos
        self.content_box.add_widget(Label(size_hint_y=None, height=20))

        # --- FOOTER ---
        # Buton stil "Bară de sistem"
        btn = Button(
            text="< TERMINATE SESSION >",
            size_hint=(1, 0.08),
            pos_hint={'bottom': 1},
            background_normal='',
            background_color=(0, 0, 0, 0), # Transparent, desenăm noi
            color=COLOR_MAGENTA,
            bold=True
        )
        # Grafică buton personalizată
        with btn.canvas.before:
            Color(*COLOR_MAGENTA)
            self.btn_line = Line(width=1.5)
            Color(0.9, 0.17, 0.56, 0.15) # Magenta transparent fundal
            self.btn_bg = Rectangle()
            
        btn.bind(pos=self._update_btn, size=self._update_btn)
        btn.bind(on_release=self.go_back)
        main_layout.add_widget(btn)

    def on_enter(self):
        """ Se apelează automat când ecranul devine activ """
        # 1. Pornim Scanner-ul
        self.start_scanner()
        
        # 2. Animăm Imaginea
        if hasattr(self, 'img_widget'):
            Animation(opacity=1, duration=1).start(self.img_widget)
            
        # 3. Declanșăm animațiile cardurilor
        for card in self.cards:
            card.animate_in()

    def start_scanner(self):
        """ Animație infinită a liniei de scanare """
        self.scanner.size = (self.width, 3)
        self.scanner.pos = (0, self.height) # Start sus
        
        # Animăm pos y de la height la 0
        anim = Animation(pos=(0, 0), duration=2.5, t='in_out_sine')
        anim += Animation(pos=(0, self.height), duration=0) # Reset instant sus
        anim.repeat = True
        anim.start(self.scanner)

    def _update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        # Scannerul se actualizează prin animație, dar setăm lățimea
        self.scanner.size = (self.width, 3)

    def _update_btn(self, instance, *args):
        # Desenăm un chenar doar sus și jos pentru buton
        self.btn_bg.pos = instance.pos
        self.btn_bg.size = instance.size
        self.btn_line.points = [
            instance.x, instance.top, instance.right, instance.top, # Linie Sus
            instance.right, instance.y, instance.x, instance.y      # Linie Jos
        ]

    def go_back(self, instance):
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'