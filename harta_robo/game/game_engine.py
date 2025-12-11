import pygame
from game.map import GameMap
from game.robot import Robot

class GameEngine:
    def __init__(self, map_path, robot_path=None):
        pygame.init()

        pygame.display.set_mode((1, 1))

        # DIMENSIUNEA FERESTREI VIZIBILE
        self.screen_w = 500
        self.screen_h = 300


        # DIMENSIUNEA HĂRȚII LOGICE
        self.map_w = 1280
        self.map_h = 720

        # ÎNCĂRCARE HARTĂ
        self.map_original = GameMap(
            map_path,
            target_width=self.map_w,
            target_height=self.map_h
        )

        # FEREASTRA JOCULUI
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Campus Game")

        # ROBOT START (dreapta jos)
        start_x = self.map_w - 290
        start_y = self.map_h - 100
        self.robot = Robot(pos=(start_x, start_y), scale=0.16)

        self.active = False
        self.current_building = None

        self.dialog_text = None
        self.dialog_timer = 0

    # ======================================================
    # CAMERA – CENTREAZĂ ROBOTUL PE ECRAN
    # ======================================================
    def get_camera_offset(self):
        offset_x = self.screen_w // 2 - self.robot.x
        offset_y = self.screen_h // 2 - self.robot.y

        # limite (nu ieșim din hartă)
        offset_x = min(0, offset_x)
        offset_y = min(0, offset_y)

        offset_x = max(offset_x, self.screen_w - self.map_w)
        offset_y = max(offset_y, self.screen_h - self.map_h)

        return offset_x, offset_y

    # ======================================================
    # UPDATE
    # ======================================================
    def update(self, gesture):

        if gesture == "PALM":
            self.active = True
        elif gesture == "FIST":
            self.active = False

        if not self.active:
            return

        moves = {
            "LIKE": "UP",
            "PEACE": "RIGHT",
            "ROCK": "LEFT",
            "BACK": "DOWN"
        }

        if gesture in moves:

            self.robot.update(
                moves[gesture],
                self.map_w,
                self.map_h,
                self.map_original
            )

            # Coliziune clădiri
            hit = self.map_original.get_building_hit(self.robot.get_rect())

            if hit and hit != self.current_building:
                self.current_building = hit
                self.dialog_text = hit
                self.dialog_timer = 120

            elif hit is None:
                self.current_building = None

    # ======================================================
    # DRAW
    # ======================================================
    def draw(self):
        offset_x, offset_y = self.get_camera_offset()

        # Desenăm harta în funcție de cameră
        self.screen.blit(self.map_original.image, (offset_x, offset_y))

        # Desenăm robotul cu offset de cameră
        self.robot.draw(self.screen, offset=(offset_x, offset_y))

        # --------------------------
        # Speech bubble
        # --------------------------
        if self.dialog_text and self.dialog_timer > 0:
            font = pygame.font.SysFont("Arial", 26, bold=True)
            text_surf = font.render(self.dialog_text, True, (255, 255, 255))
            padding = 10

            # poziția balonului urmează robotul în camera
            bx = self.robot.x + offset_x - 10
            by = self.robot.y + offset_y - 60

            bubble_rect = text_surf.get_rect()
            bubble_rect.x = bx
            bubble_rect.y = by
            bubble_rect.inflate_ip(padding * 2, padding * 2)

            pygame.draw.rect(self.screen, (0, 0, 0), bubble_rect, border_radius=12)
            pygame.draw.rect(self.screen, (255, 255, 255), bubble_rect, 2, border_radius=12)

            self.screen.blit(text_surf, (bubble_rect.x + padding, bubble_rect.y + padding))

            self.dialog_timer -= 1

        pygame.display.flip()
