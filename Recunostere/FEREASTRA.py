import pygame
import sys
import os

pygame.init()

# Dimensiuni fereastră
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Specializări - Puncte Cardinale")

# Fundal bleu deschis
BLUE = (135, 206, 250)

# Font DEFAULT – acesta există pe Raspberry Pi
font = pygame.font.Font(None, 36)

# Funcție pentru încărcare fără fundal negru
def load_no_bg(path):
    full_path = os.path.join(os.path.dirname(__file__), path)

    if not os.path.exists(full_path):
        print(f"[EROARE] Nu găsesc fișierul: {full_path}")
        sys.exit(1)

    img = pygame.image.load(full_path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img

# Logo-uri (CASE SENSITIVE pe Linux!)
logos = {
    "Automatica": load_no_bg("automatica1.png"),
    "Calculatoare": load_no_bg("calculatoare1.png"),
    "Inginerie Electrică": load_no_bg("inginerie_electrica1.png"),
    "Inginerie Electronică": load_no_bg("electronica1.png")
}

# Redimensionăm imaginile
def resize(img, w):
    scale = w / img.get_width()
    h = int(img.get_height() * scale)
    return pygame.transform.smoothscale(img, (w, h))

for key in logos:
    logos[key] = resize(logos[key], 120)

# Poziții
positions = {
    "Automatica": (WIDTH // 2, 120),
    "Calculatoare": (WIDTH // 2, HEIGHT - 140),
    "Inginerie Electrică": (150, HEIGHT // 2),
    "Inginerie Electronică": (WIDTH - 150, HEIGHT // 2)
}

# Funcție pentru desenare (STATICĂ, fără hover)
def draw_logo(name, img, center_pos):
    x, y = center_pos

    img_rect = img.get_rect(center=(x, y))
    screen.blit(img, img_rect)

    # Text simplu
    text = font.render(name, True, (10, 10, 60))
    text_rect = text.get_rect(center=(x, y + img.get_height() // 2 + 30))
    screen.blit(text, text_rect)

# Loop principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLUE)

    # Desenăm logo-urile statice
    for name, img in logos.items():
        draw_logo(name, img, positions[name])

    pygame.display.update()
    clock.tick(30)  # stabilitate pe Raspberry Pi

pygame.quit()
sys.exit()
