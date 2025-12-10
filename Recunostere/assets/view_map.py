import pygame
import sys
import os

MAP_PATH = "assets/harta.png"   # modifică numele dacă e nevoie
SCALE_TO_WIDTH = 1280                  # None = fără scalare

def main():
    pygame.init()

    # Verificăm existența fișierului
    if not os.path.exists(MAP_PATH):
        print(f"FIȘIERUL NU EXISTĂ: {MAP_PATH}")
        sys.exit(1)

    # Încărcăm imaginea fără convert_alpha (ca să nu ceară video mode)
    try:
        map_img = pygame.image.load(MAP_PATH)
    except Exception as e:
        print(f"Nu pot încărca imaginea: {e}")
        sys.exit(1)

    map_width, map_height = map_img.get_size()

    # Scalare opțională
    if SCALE_TO_WIDTH is not None and map_width != SCALE_TO_WIDTH:
        factor = SCALE_TO_WIDTH / map_width
        new_size = (int(map_width * factor), int(map_height * factor))
        map_img = pygame.transform.smoothscale(map_img, new_size)
        map_width, map_height = new_size

    # Setăm video mode ABIA ACUM (înainte de convert)
    screen = pygame.display.set_mode((map_width, map_height))
    pygame.display.set_caption("Harta Campusului")

    # Acum putem converti imaginea
    map_img = map_img.convert()

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        screen.blit(map_img, (0, 0))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()
