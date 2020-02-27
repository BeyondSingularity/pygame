import pygame
import os
import math
import time

import random

pygame.init()


def draw_win_screeen(screen, win_player, width, height):
    ans = [win_player + ' победил', 'Начать заново', 'Выйти в главное меню']
    num = 1
    is_run = True
    font = pygame.font.Font(None, 50)
    for i in range(3):
        Distance = 100
        text = font.render(ans[i], 1, (100, 255, 100))
        text_x = width // 2 - text.get_width() // 2
        text_y = Distance * (i + 1)
        text_w = text.get_width()
        text_h = text.get_height()
        res = ans[i]
        ans[i] = (res, text, text_x, text_y, text_w, text_h)
    while is_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    num = (num - 1) % 2
                elif event.key == pygame.K_DOWN:
                    num = (num + 1) % 2
                elif event.key == pygame.K_KP_ENTER:
                    if num == 1:
                        return
                    elif num == 0:
                        game()
        screen.fill((0, 0, 0))
        for i in range(3):
            screen.blit(ans[i][1], (ans[i][2], ans[i][3]))

        pygame.draw.polygon(screen, (100, 255, 100),
                            ((ans[num + 1][2] - 20, ans[num + 1][3]),
                             (ans[num + 1][2] - 10,
                              ans[num + 1][3] + ans[num + 1][5] // 2),
                             (ans[num + 1][2] - 20,
                              ans[num + 1][3] + ans[num + 1][5])))
        pygame.display.flip()


def ask_exit(screen, width):
    num = 0

    def draw_ask_exit(num):
        font = pygame.font.Font(None, 50)
        ans = ['нет', 'да']

        txt = font.render('Вы действительно хотите выйти?', 1, (100, 255, 100))
        txt_x = width // 2 - txt.get_width() // 2
        txt_y = 10
        screen.blit(txt, (txt_x, txt_y))

        for i in range(2):
            Distance = 100
            text = font.render(ans[i], 1, (100, 255, 100))
            text_x = width // 2 - text.get_width() // 2
            text_y = Distance * (i + 1)
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            res = ans[i]
            ans[i] = (res, 0, text_x, text_y, text_w, text_h)
        pygame.draw.polygon(screen, (100, 255, 100),
                            ((ans[num][2] - 20, ans[num][3]),
                             (ans[num][2] - 10,
                              ans[num][3] + ans[num][5] // 2),
                             (ans[num][2] - 20,
                              ans[num][3] + ans[num][5])))

    is_run = True
    while is_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    num = (num - 1) % 2
                elif event.key == pygame.K_DOWN:
                    num = (num + 1) % 2
                elif event.key == pygame.K_KP_ENTER:
                    if num == 0:
                        return False
                    elif num == 1:
                        return True
        screen.fill((0, 0, 0))
        draw_ask_exit(num)
        pygame.display.flip()


def game():
    player_sprite = pygame.sprite.Group()
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
            self.health = Heart(group, heart_x)
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
            self.kof = 1 + int(not reverse)

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

    class Ground(pygame.sprite.Sprite):
        def __init__(self, group, x):
            super().__init__(group)
            self.x = x
            self.image = load_image("ground.jpg")
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = 1080 - 145

        def update(self, offset):
            self.x += offset
            while self.x < -499:
                self.x += 2495
            while self.x > 1996:
                self.x -= 2495
            self.rect.x = int(self.x)

    def make_trajectory(x, y, x1, y2, x2, y1):
        t = 0.5
        l = math.hypot(y2 - y1, x2 - x1)
        vx = defa * (x2 - x1) / l * (min(smax, l) / smax)
        vy = defa * (y1 - y2) / l * (min(smax, l) / smax)
        circles = []
        for i in range(10):
            vy -= g * t / 10
            y += vy * t / 10 - g * (t / 10) ** 2 / 2
            x -= vx * t / 10
            circles.append((x, y, 6 - i // 2))
        return circles

    start_health = 1
    x = 960
    y = 230
    defa = 3750
    g = 1000
    smax = 600
    running = True
    flag = False
    arrow = Smth()
    flying = False
    shot_was = False

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    size = width, height = pygame.display.get_surface().get_size()
    height -= 130
    pos1 = random.randint(0, 5000)
    pos2 = random.randint(8000, 13000)
    pos2 = pos1 + 400
    player = Player(player_sprite, pos1, False)
    player2 = Player(player_sprite, pos2, True)
    for i in range(5):
        Ground(player_sprite, (i - 1) * 499)

    player_sprite.update(0)
    player_sprite.draw(screen)

    pygame.display.flip()
    arrowx = 0
    while player2.health.get() != 0 and player.health.get() != 0:
        change_coefficient = True
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
                    screen.fill((0, 0, 0))
                    for a, b, r in make_trajectory(x, y, x1, y1, dx, dy):
                        pygame.draw.circle(screen, (255, 255, 255), (int(a), 1080 - int(b)), r)
                        sp.draw(screen)
                        player_sprite.draw(screen)
                        pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONUP:
                    x2, y2 = event.pos
                    if math.hypot(y1 - y2, x1 - x2) >= 10 and not shot_was:
                        shot_was = True
                        arrow = Arrow(sp, x, y, defa, g, smax, x1, y2, x2, y1)
                        flag = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if ask_exit(screen, width):
                            return
                        else:
                            change_coefficient = False
            if shot_was:
                screen.fill((0, 0, 0))
                if player2.x1 <= arrow.arrowhead[0] <= player2.x2 and player2.y1 <= arrow.arrowhead[1] <= player2.y2:
                    running = False
                    player2.health.bite()
                    arrow.type = 2
                if arrow.arrowhead[1] > 1080 - 145:
                    running = False
                    arrow.type = 2
                offset = 960 - arrow.x
                arrow.x = 960
                arrow.rect.x = 960 - arrow.image.get_size()[0] // 2
                sp.update(120, offset)
                sp.draw(screen)
                player_sprite.update(offset)
                player_sprite.draw(screen)
                pygame.display.flip()
                time.sleep(1 / 120)
        player, player2 = player2, player
        if change_coefficient:
            time.sleep(1)

    if player.health.get() == 0:
        draw_win_screeen(screen, 'Игрок ' + str(player.kof), width, height)
    elif player2.health.get() == 0:
        draw_win_screeen(screen, 'Игрок ' + str(player.kof), width, height)
