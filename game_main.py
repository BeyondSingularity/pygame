import math
import pygame
import os

pygame.init()

sp = pygame.sprite.Group()

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Arrow(pygame.sprite.Sprite):
    def __init__(self, group, x, y, defa, g, smax):
        super.__init__(group)
        self.defa = defa
        self.smax = smax
        self.g = g
        self.image = load_image("Arrow.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def start(self, x1, y1, x2, y2, screen):
        l = math.hypot(y1 - y2, x1 - x2)
        angle = math.degrees(math.atan((y1 - y2) / (x1 - x2)))
        self.vx = self.defa * (x1 - x2) / l * (min(self.smax, l) / self.smax)
        self.vy = self.defa * (y1 - y2) / l * (min(self.smax, l) / self.smax)

        self.image = pygame.transform.rotate(screen, -angle)

    def update(self, fps, screen):
        self.vy -= self.g / fps
        y2 = self.rect.y + self.vy / fps - self.g / fps / fps / 2
        x2 = self.rect.x + self.vx / fps
        new_angle = math.degrees(math.atan((y2 - self.y) / (x2 - self.x)))

        self.image = pygame.transform.rotate(screen, -new_angle)

        self.rect.x = x2
        self.rect.y = y2


running = True
fps = 120

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = pygame.display.get_surface().get_size()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    screen.fill((255, 255, 255))
    sp.draw(screen)
    sp.update()
    pygame.display.flip()

pygame.quit()
