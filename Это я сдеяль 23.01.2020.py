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
        self.arrowhead = (0, 0)
        self.defa = defa
        self.smax = smax
        self.g = g
        self.type = 1
        l = math.hypot(y1 - y2, x1 - x2)
        if x1 == x2:
            x2 += 1
        self.angle = math.degrees(math.atan((y1 - y2) / (x1 - x2)))
        self.vx = self.defa * (x1 - x2) / l * (min(self.smax, l) / self.smax)
        self.vy = self.defa * (y1 - y2) / l * (min(self.smax, l) / self.smax)
        self.def_image = load_image("Arrow.png", (255, 255, 255))
        self.def_image = pygame.transform.scale(self.def_image, (10, 98))
        self.image = pygame.transform.rotate(self.def_image, -self.angle)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = 1080 - y
        self.x = x
        self.y = y

    def update(self, fps):
        if self.type == 2:
            return 0
        self.vy -= self.g / fps
        y2 = self.y + self.vy / fps - self.g / fps ** 2 / 2
        x2 = self.x + self.vx / fps
        self.angle = math.degrees(math.atan((y2 - self.y) / (x2 - self.x)))
        if x2 - self.x < 0:
            self.image = pygame.transform.rotate(self.def_image, self.angle + 90)
        else:
            self.image = pygame.transform.rotate(self.def_image, self.angle - 90)
        im_x, im_y = self.image.get_size()
        if x2 - self.x > 0:
            self.arrowhead = (x2 + im_x // 2, 0)
        else:
            self.arrowhead = (x2 - im_x // 2, 0)
        if y2 - self.y < 0:
            self.arrowhead = (self.arrowhead[0], 1080 - y2 + im_y // 2)
        else:
            self.arrowhead = (self.arrowhead[0], 1080 - y2 - im_y // 2)
        self.x = x2
        self.rect.x = self.x - im_x // 2
        self.y = y2
        self.rect.y = 1080 - self.y - im_y // 2

class Smth():
    def __init__(self):
        self.type = 0
        self.arrowhead = (0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        not_image = load_image("Boy.png", (255, 255, 255))
        self.image = pygame.transform.scale(not_image, (132, 140))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = height - 150
        self.x1 = self.rect.x
        im_x, im_y = self.image.get_size()
        self.x2 = self.x1 + im_x
        self.y1 = self.rect.y
        self.y2 = self.y1 + im_y

    def update(self):
        pass


class Heart(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        not_im = load_image('heart.png')
        self.image = pygame.transform.scale(not_im, (120, 130))
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = height - 150


screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = pygame.display.get_surface().get_size()
player = Player(player_sprite)
heart = Heart(healt_sprite)

x = 200 + 17 * 4
y = 100
defa = 3000
g = 1000
smax = 600
x1, y1, x2, y2 = 0, 0, 0, 0
dx, dy = 0, 0
running = True
flag = False
arrow = Smth()
flying = False
print(player.x1, player.x2, player.y1, player.y2)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x1, y1 = event.pos
            flag = True
        if event.type == pygame.MOUSEMOTION and flag:
            dx, dy = event.pos
        if event.type == pygame.MOUSEBUTTONUP:
            x2, y2 = event.pos
            if math.hypot(y1 - y2, x1 - x2) >= 10 and not flying:
                flying = True
                arrow = Arrow(sp, x, y, defa, g, smax, x1, y2, x2, y1)
                flag = False
    '''if arrow.arrowhead:
        pass
    if arrow.arrowhead[1] <= 0:
        pass'''

    if arrow.type == 1:
        # print(*arrow.arrowhead)
        if player.x1 <= arrow.arrowhead[0] <= player.x2 and player.y1 <= arrow.arrowhead[1] <= player.y2:
            flying = False
            arrow.type = 2
        if arrow.arrowhead[1] > 1080:
            flying = False
            arrow.type = 2
    screen.fill((0, 0, 0))
    sp.update(120)
    pygame.draw.rect(screen, (255, 0, 0), (player.x1, min(player.y1, player.y2), (player.x2 - player.x1), (player.y2 - player.y1)))
    a, b = arrow.arrowhead
    a, b = int(a), int(b)
    pygame.draw.circle(screen, (0, 0, 255), (a, b), 5)
    sp.draw(screen)
    player_sprite.draw(screen)
    player_sprite.update()
    pygame.display.flip()
    time.sleep(1 / 120)

pygame.quit()