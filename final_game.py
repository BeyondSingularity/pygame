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

    def update(self, fps, offset):
        if self.type == 2:
            self.x += offset
            self.rect.x = int(self.x)
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
        self.rect.x = int(self.x - im_x // 2)
        self.y = y2
        self.rect.y = int(1080 - self.y - im_y // 2)

class Smth():
    def __init__(self):
        self.type = 0
        self.arrowhead = (0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self, group, x, reverse):
        super().__init__(group)
        self.image = pygame.transform.scale(load_image("Boy.png", (255, 255, 255)), (132, 140))
        heart_x = x
        if reverse:
            self.image = pygame.transform.flip(self.image, True, False)
            heart_x += self.image.get_size()[0]
        self.health = Heart(player_sprite, heart_x)
        self.rect = self.image.get_rect()
        self.rect.x = x
        if reverse:
            self.rect.x += self.image.get_size()[0]
        self.rect.y = height - 150
        self.x1 = self.rect.x
        self.im_x, self.im_y = self.image.get_size()
        self.x2 = self.x1 + self.im_x
        self.y1 = self.rect.y
        self.y2 = self.y1 + self.im_y

    def update(self, offset=0):
        self.x1 += offset
        self.rect.x = int(self.x1)
        self.x2 = self.x1 + self.im_x


class Heart(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        self.hearts = []
        for i in range(7):
            self.hearts.append(load_image(str(i) + '.png', (255, 255, 255)))
        self.image = pygame.transform.scale(self.hearts[start_health], (132, 42))
        self.rect = self.image.get_rect()
        self.x = pos
        self.rect.x = pos
        self.rect.y = height - 190
        self.health = start_health

    def get(self):
        return self.health

    def update(self, offset):
        self.x += offset
        self.rect.x = int(self.x)

    def bite(self):
        self.health -= 1
        self.image = pygame.transform.scale(self.hearts[self.health], (132, 42))

def play_round():
    flag = False
    arrow = Smth()
    running = True
    shot_was = False
    screen.fill((0, 0, 0))
    offset = 960 - (player.x2 + player.x1) // 2
    player_sprite.update(offset)
    sp.update(120, offset)
    sp.draw(screen)
    player_sprite.draw(screen)
    pygame.display.flip()
    time.sleep(1 / 120)
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
                if math.hypot(y1 - y2, x1 - x2) >= 10 and not shot_was:
                    shot_was = True
                    arrow = Arrow(sp, x, y, defa, g, smax, x1, y2, x2, y1)
                    flag = False
        if shot_was:
            if player2.x1 <= arrow.arrowhead[0] <= player2.x2 and player2.y1 <= arrow.arrowhead[1] <= player2.y2:
                running = False
                player2.health.bite()
                arrow.type = 2
            if arrow.arrowhead[1] > 1080:
                running = False
                arrow.type = 2
            screen.fill((0, 0, 0))
            offset = 960 - arrow.x
            arrow.x = 960
            arrow.rect.x = 960 - arrow.image.get_size()[0] // 2
            sp.update(120, offset)
            sp.draw(screen)
            player_sprite.update(offset)
            player_sprite.draw(screen)
            pygame.display.flip()
            time.sleep(1 / 120)


start_health = 2
x = 960
y = 100
defa = 3750
g = 1000
smax = 600
dx, dy = 0, 0
running = True
flag = False
arrow = Smth()
flying = False
shot_was = False

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = width, height = pygame.display.get_surface().get_size()
pos1 = random.randint(0, 5000)
pos2 = random.randint(8000, 13000)
pos1 = 6000
pos2 = 7000
player = Player(player_sprite, pos1, False)
player2 = Player(player_sprite, pos2, True)

player_sprite.update(0)
player_sprite.draw(screen)

pygame.display.flip()
arrowx = 0
while player2.health.get() != 0 and player.health.get() != 0:
    play_round()
    player, player2 = player2, player
    time.sleep(1)
pygame.quit()