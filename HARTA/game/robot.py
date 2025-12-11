import pygame

class Robot:
    def __init__(self, pos=(200, 150), scale=0.05):
        self.x, self.y = pos
        self.base_scale = scale
        self.scale = scale
        self.speed = 0.15
        self.offset_y = 8

        # ORIGINAL SPRITES
        self.img_front_original  = pygame.image.load("assets/robot_fata.png").convert_alpha()
        self.img_left_original   = pygame.image.load("assets/robot_stanga.png").convert_alpha()
        self.img_right_original  = pygame.image.load("assets/robot_dreapta.png").convert_alpha()

        # INITIAL SCALED SPRITES
        self.img_front  = self.scale_sprite(self.img_front_original, self.scale)
        self.img_left   = self.scale_sprite(self.img_left_original, self.scale)
        self.img_right  = self.scale_sprite(self.img_right_original, self.scale)

        self.image = self.img_front

    # SCALE SPRITE
    def scale_sprite(self, img, scale):
        w = int(img.get_width() * scale)
        h = int(img.get_height() * scale)
        return pygame.transform.smoothscale(img, (w, h))

    # RESCALE (pentru zoom, dacă vei folosi în viitor)
    def rescale(self, zoom):
        self.scale = self.base_scale * zoom

        self.img_front = self.scale_sprite(self.img_front_original, self.scale)
        self.img_left  = self.scale_sprite(self.img_left_original, self.scale)
        self.img_right = self.scale_sprite(self.img_right_original, self.scale)

        # păstrează direcția curentă
        if self.image in (self.img_front_original, self.img_front):
            self.image = self.img_front
        elif self.image in (self.img_left_original, self.img_left):
            self.image = self.img_left
        elif self.image in (self.img_right_original, self.img_right):
            self.image = self.img_right

    # RECT EXACT al robotului
    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y - self.offset_y,
            self.image.get_width(),
            self.image.get_height()
        )

    # UPDATE + COLIZIUNE
    def update(self, direction, map_width, map_height, game_map=None):

        new_x = self.x
        new_y = self.y

        if direction == "UP":
            new_y -= self.speed
            self.image = self.img_front

        elif direction == "DOWN":
            new_y += self.speed
            self.image = self.img_front

        elif direction == "LEFT":
            new_x -= self.speed
            self.image = self.img_left

        elif direction == "RIGHT":
            new_x += self.speed
            self.image = self.img_right

        # COLIZIUNE PIXEL PERFECT
        if game_map:
            foot_x = int(new_x + self.image.get_width() // 2)
            foot_y = int(new_y + self.image.get_height() - 5)

            if not game_map.is_walkable(foot_x, foot_y):
                return  # se lovește → nu avansează

        # LIMITĂ HARTĂ
        w, h = self.image.get_width(), self.image.get_height()

        self.x = max(0, min(new_x, map_width - w))
        self.y = max(0, min(new_y, map_height - h))

    # ---------------------------------------------------------
    # DRAW cu CAMERA OFFSET — CEL MAI IMPORTANT!
    # ---------------------------------------------------------
    def draw(self, screen, offset=(0, 0)):
        ox, oy = offset
        screen.blit(self.image, (self.x + ox, self.y + oy - self.offset_y))
