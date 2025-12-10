import pygame
from PIL import Image

class Robot:
    def __init__(self, gif_path, pos=(300, 300), scale=0.10):
        self.x, self.y = pos
        self.scale = scale
        self.gif_path = gif_path

        self.frames = []
        self.frame_index = 0
        self.frame_counter = 0
        self.frame_delay = 5
        self.speed = 4

        self.load_gif()

    # ---------------------------------------------------------
    # LOAD GIF + CROP SLIGHTLY + SCALE SMALLER
    # ---------------------------------------------------------
    def load_gif(self):
        gif = Image.open(self.gif_path)

        try:
            while True:
                frame = gif.convert("RGBA")

                # crop minimal ca să eliminăm marginile goale ale GIF-ului
                bbox = frame.getbbox()
                if bbox:
                    frame = frame.crop(bbox)

                # convertim în pygame
                mode = frame.mode
                size = frame.size
                data = frame.tobytes()
                pg_frame = pygame.image.fromstring(data, size, mode)

                # doar scale, nimic altceva
                new_size = (
                    int(size[0] * self.scale),
                    int(size[1] * self.scale)
                )
                pg_frame = pygame.transform.smoothscale(pg_frame, new_size)

                self.frames.append(pg_frame)

                gif.seek(gif.tell() + 1)

        except EOFError:
            pass

    # ---------------------------------------------------------
    # MOVEMENT
    # ---------------------------------------------------------
    def update(self, direction):
        if direction == "UP":
            self.y -= self.speed
        elif direction == "DOWN":
            self.y += self.speed
        elif direction == "LEFT":
            self.x -= self.speed
        elif direction == "RIGHT":
            self.x += self.speed
        elif direction == "BACK":
            self.y += self.speed * 2

        self.frame_counter += 1
        if self.frame_counter >= self.frame_delay:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)

    # ---------------------------------------------------------
    # DRAW
    # ---------------------------------------------------------
    def draw(self, screen):
        screen.blit(self.frames[self.frame_index], (self.x, self.y))
