import pygame
import random
from random import randint
import time
import gameUp1

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
size = WIDTH, HEIGHT = pygame.display.get_surface().get_size()

running = True
all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()
FPS = 60

def ask_exit():
    def dont():
        font = pygame.font.Font(None, 50)
        ans = ['нет', 'да']

        txt = font.render('Вы действительно хотите выйти?', 1, (100, 255, 100))
        txt_x = WIDTH // 2 - txt.get_width() // 2
        txt_y = 10
        screen.blit(txt, (txt_x, txt_y))

        for i in range(2):
            Distance = 100
            text = font.render(ans[i], 1, (100, 255, 100))
            text_x = WIDTH // 2 - text.get_width() // 2
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

    num = 0
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
        dont()
        pygame.display.flip()


class MainMenu:
    def __init__(self):
        self.list_of_games = []
        self.list_of_games_full = []

        self.list_of_games.append('Игра')
        self.list_of_games.append('Настройки')
        self.list_of_games.append('Выйти из игры')

    def draw(self):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)

        for i in range(len(self.list_of_games)):
            S = 100
            text = font.render(self.list_of_games[i], 1, (100, 255, 100))
            self.text_x = WIDTH // 2 - text.get_width() // 2
            self.text_y = S * (i + 1)
            self.text_w = text.get_width()
            self.text_h = text.get_height()
            screen.blit(text, (self.text_x, self.text_y))
            self.list_of_games_full.append([self.list_of_games[i], 0, self.text_x, self.text_y,
                                            self.text_w, self.text_h])

    def correct_game(self, cof):
        pygame.draw.polygon(screen, (100, 255, 100),
                            ((self.list_of_games_full[cof][2] - 20, self.list_of_games_full[cof][3]),
                             (self.list_of_games_full[cof][2] - 10,
                              self.list_of_games_full[cof][3] + self.list_of_games_full[cof][5] // 2),
                             (self.list_of_games_full[cof][2] - 20,
                              self.list_of_games_full[cof][3] + self.list_of_games_full[cof][5])))
        for i in range(len(self.list_of_games_full)):
            if i == cof:
                self.list_of_games_full[i][1] = 1
            else:
                self.list_of_games_full[i][1] = 0


def Settings():
    global cof_prefix, FPS
    def DrawSettings():
        font = pygame.font.Font(None, 50)
        main_settings = ['Текстуры', 'Назад']
        prefix_graph = ['низкие', 'средние', 'высокие', 'ультра высокие']
        txt = font.render('Настройки', 1, (100, 255, 100))
        txt_x = WIDTH // 2 - txt.get_width() // 2
        txt_y = 10
        screen.blit(txt, (txt_x, txt_y))

        for i in range(len(main_settings)):
            Distance = 100
            if main_settings[i] == 'Текстуры':
                text = font.render(main_settings[i] + ': ' + prefix_graph[cof_prefix], 1, (100, 255, 100))
            else:
                text = font.render(main_settings[i], 1, (100, 255, 100))
            text_x = WIDTH // 2 - text.get_width() // 2
            text_y = Distance * (i + 1)
            text_w = text.get_width()
            text_h = text.get_height()
            screen.blit(text, (text_x, text_y))
            res = main_settings[i]
            main_settings[i] = (res, 0, text_x, text_y, text_w, text_h)
        pygame.draw.polygon(screen, (100, 255, 100),
                            ((main_settings[num][2] - 20, main_settings[num][3]),
                             (main_settings[num][2] - 10,
                              main_settings[num][3] + main_settings[num][5] // 2),
                             (main_settings[num][2] - 20,
                              main_settings[num][3] + main_settings[num][5])))

    num = 0
    is_run = True
    while is_run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    cof_prefix = (cof_prefix + 1) % 4
                elif event.key == pygame.K_LEFT:
                    cof_prefix = (cof_prefix - 1) % 4
                elif event.key == pygame.K_UP:
                    num = (num + 1) % 2
                elif event.key == pygame.K_DOWN:
                    num = (num - 1) % 2
                elif event.key == pygame.K_KP_ENTER and num == 1:
                    return False
        FPS = 120 - cof_prefix * 35
        screen.fill((0, 0, 0))
        DrawSettings()
        pygame.display.flip()


menu = MainMenu()
music = pygame.mixer.music
music.load('data\MenuSong.mp3')  # Загрузка музыки
music.play()  # начало воспроизведения музыки
cof_limit = len(menu.list_of_games)
cof = 1
cof_prefix = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                cof = (cof - 1) % cof_limit
            elif event.key == pygame.K_DOWN:
                cof = (cof + 1) % cof_limit
            elif event.key == pygame.K_KP_ENTER:
                if cof == 0:
                    music.stop()
                    gameUp1.game()
                elif cof == 1:
                    Settings()
                elif cof == 2:
                    if ask_exit():
                        quit()

    screen.fill((0, 0, 0))
    menu.draw()
    menu.correct_game(cof)
    pygame.display.flip()
    time.sleep(1 / FPS)

pygame.quit()
