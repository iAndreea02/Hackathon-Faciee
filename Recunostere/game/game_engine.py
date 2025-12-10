import pygame
from game.map import GameMap
from game.robot import Robot

class GameEngine:
    def __init__(self, map_path, robot_path):
        pygame.init()

        # 🟦 NECESAR: inițializăm o fereastră temporară
        # altfel imaginile din GameMap nu pot fi convertite
        pygame.display.set_mode((1, 1))

        # Acum putem încărca harta în siguranță
        self.map = GameMap()

        # 🟦 Creăm fereastra REALĂ fix pe dimensiunea hărții
        self.screen = pygame.display.set_mode(
            (self.map.width, self.map.height)
        )
        pygame.display.set_caption("Campus Game")

        # Poziția de start a robotului
        start_x = 40
        start_y = self.map.height - 120
        self.robot = Robot(robot_path, pos=(start_x, start_y))

        self.active = False


    def update(self, gesture):
        # Activare / dezactivare control
        if gesture == "PALM":
            self.active = True
        elif gesture == "FIST":
            self.active = False

        if not self.active:
            return

        # 3 degete (BACK) → robotul merge în jos
        if gesture == "BACK":
            self.robot.update("DOWN")
            return

        # Mișcări standard
        moves = {
            "LIKE": "UP",        # sus
            "PEACE": "RIGHT",    # dreapta
            "ROCK": "LEFT"       # stânga
        }

        if gesture in moves:
            self.robot.update(moves[gesture])


    def draw(self):
        self.map.draw(self.screen)
        self.robot.draw(self.screen)
        pygame.display.flip()
