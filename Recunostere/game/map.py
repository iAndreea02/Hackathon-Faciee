import pygame

class GameMap:
    def __init__(self):
        self.width = 900
        self.height = 600
        self.background = (135, 206, 250)  # bleu frumos

        # Font
        self.font = pygame.font.SysFont("Arial", 26, bold=True)

        # Load logos (black background removed)
        def load_icon(path):
            img = pygame.image.load(path).convert_alpha()  # <- FIX
            img.set_colorkey((0, 0, 0))
            return img


        self.logos = {
            "Automatica": load_icon("assets/automatica1.png"),
            "Calculatoare": load_icon("assets/calculatoare1.png"),
            "Inginerie Electrică": load_icon("assets/inginerie electrica1.png"),
            "Inginerie Electronică": load_icon("assets/electronica1.png")
        }

        # resize smaller
        def resize(img, w):
            scale = w / img.get_width()
            h = int(img.get_height() * scale)
            return pygame.transform.smoothscale(img, (w, h))

        for k in self.logos:
            self.logos[k] = resize(self.logos[k], 110)

        # Highly spaced positions
        self.positions = {
            "Automatica": (self.width // 2, 120),
            "Calculatoare": (self.width // 2, self.height - 140),
            "Inginerie Electrică": (150, self.height // 2),
            "Inginerie Electronică": (self.width - 150, self.height // 2)
        }

    # Draw logo + nice text
    def draw_logo(self, screen, name, img, pos):
        x, y = pos

        # hover
        mouse = pygame.mouse.get_pos()
        rect = img.get_rect(center=pos)
        hover = rect.collidepoint(mouse)

        scale = 1.10 if hover else 1.0
        w = int(img.get_width() * scale)
        h = int(img.get_height() * scale)

        scaled = pygame.transform.smoothscale(img, (w, h))
        rect = scaled.get_rect(center=pos)
        screen.blit(scaled, rect)

        # text
        color = (10, 10, 60) if not hover else (0, 0, 0)
        label = self.font.render(name, True, color)
        label_rect = label.get_rect(center=(x, y + h // 2 + 35))
        screen.blit(label, label_rect)

    # Main draw
    def draw(self, screen):
        screen.fill(self.background)

        # Draw specializations
        for name, img in self.logos.items():
            self.draw_logo(screen, name, img, self.positions[name])
