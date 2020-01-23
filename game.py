import pygame
import os
import math
import time

import random

pygame.init()

enemy = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
sp = pygame.sprite.Group()
healt_sprite = pygame.sprite.Group()


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
    def __init__(self, group, x, y, defa, g, smax, x1, y1, x2, y2):
        super().__init__(group)
        self.defa = defa
        self.smax = smax
        self.g = g
        l = math.hypot(y1 - y2, x1 - x2)
        self.angle = math.degrees(math.atan((y1 - y2) / (x1 - x2)))
        self.vx = self.defa * (x1 - x2) / l * (min(self.smax, l) / self.smax)
        self.vy = self.defa * (y1 - y2) / l * (min(self.smax, l) / self.smax)
        self.def_image = load_image("Arrow.png", (255, 255, 255))
        self.image = pygame.transform.rotate(self.def_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 1080 - y
        self.x = x
        self.y = y

    def update(self, fps):
        self.vy -= self.g / fps
        y2 = self.y + self.vy / fps - self.g / fps ** 2 / 2
        x2 = self.x + self.vx / fps
        self.angle = math.degrees(math.atan((y2 - self.y) / (x2 - self.x)))

        self.image = pygame.transform.rotate(self.def_image, self.angle - 90)

        im_x, im_y = self.image.get_size()

        self.x = x2
        self.rect.x = self.x + im_x // 2
        self.y = y2
        self.rect.y = 1080 - self.y - im_y // 2


class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        not_image = load_image("Boy.png", (255, 255, 255))
        self.image = pygame.transform.scale(not_image, (132, 140))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = height - 150

    def update(self):
        pass


class Heart(pygame.sprite.Sprite):
    def __init__(self, group, x, y):
        super().__init__(group)
        not_im = load_image('heart.png', (255, 255, 255))
        self.image = pygame.transform.scale(not_im, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, *args):
        pass


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = pygame.display.get_surface().get_size()
player = Player(player_sprite)

x = 200 + 17 * 4
y = 100
defa = 50
g = 10
smax = 100
arrow = Arrow(sp, x, y, defa, g, smax, 100, 100, 0, 0)

for i in range(3):
    Heart(healt_sprite, i * 30 + 250, width - 600)
    print(width - 600)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass
    screen.fill((0, 0, 0))
    player_sprite.draw(screen)
    player_sprite.update()

    sp.draw(screen)
    sp.update(120)

    healt_sprite.draw(screen)
    healt_sprite.update()

    pygame.display.flip()
    time.sleep(1 / 120)

pygame.quit()
