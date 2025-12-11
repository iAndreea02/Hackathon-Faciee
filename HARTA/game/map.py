import pygame

class GameMap:
    def __init__(self, path, target_width=1280, target_height=720):
        # imaginea scalată pentru display
        original = pygame.image.load(path).convert()
        self.image = pygame.transform.smoothscale(original, (target_width, target_height))

        # mask pentru walkable()
        self.mask = self.image.copy()

        self.width = target_width
        self.height = target_height

        # =============================
        #     CLĂDIRILE DE INTERES
        # =============================
        # POZIȚII ESTIMATE DIN SCREENSHOT – SE POT AJUSTA UȘOR

        # -----------------------------
        # 1. CORP D – dreptunghiul lung din partea dreaptă sus
        # -----------------------------
        self.rect_D = pygame.Rect(840, 260, 380, 110)

        # -----------------------------
        # 2. CORP J – dreptunghi mare albastru (sub D)
        # -----------------------------
        self.rect_J = pygame.Rect(880, 430, 260, 180)

        # -----------------------------
        # 3. CORP G – clădirea albastră cu multe ferestre (stânga lui J)
        # -----------------------------
        self.rect_G = pygame.Rect(760, 580, 330, 130)

        # -----------------------------
        # 4. CORP Y – clădirea mare în dreapta jos
        # -----------------------------
        self.rect_Y = pygame.Rect(980, 580, 280, 130)

    # ----------------------------------------------------------
    # WALKABLE = încă folosit pentru coliziuni pixel perfect
    # ----------------------------------------------------------
    def is_walkable(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False

        color = self.mask.get_at((x, y))

        # detectăm albastru închis (clădiri)
        if color.r < 80 and color.g < 80 and color.b > 120:
            return False  

        return True

    # ----------------------------------------------------------
    # DETECTEAZĂ CLĂDIREA ATINSĂ
    # ----------------------------------------------------------
    def get_building_hit(self, robot_rect):

        if robot_rect.colliderect(self.rect_D):
            return "CORPUL D"

        if robot_rect.colliderect(self.rect_J):
            return "CORP J – CANTINA"

        if robot_rect.colliderect(self.rect_G):
            return "CORPUL Y"

        if robot_rect.colliderect(self.rect_Y):
            return "CORPUL G"

        return None
