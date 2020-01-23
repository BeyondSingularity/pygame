import pygame
import random
from random import randint

pygame.init()

size = width, height = 800, 600

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

running = True
all_sprites = pygame.sprite.Group()
player_sprite = pygame.sprite.Group()


class EnemyG2:
    def __init__(self, radius):
        self.speed = random.randrange(1, 4)
        self.radius = radius
        self.x = width - radius
        self.y = random.randint(radius + 50, height - radius)

    def create(self):
        pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), self.radius, 0)
        self.x -= self.speed


class PlayerG2(pygame.sprite.Sprite):
    def __init__(self, speed, radius):
        super().__init__(all_sprites)
        self.speed = speed
        self.radius = radius
        self.x = self.radius
        self.y = (height - 50) // 2

    def update(self):
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), self.radius, 0)


def Game2():
    player = PlayerG2(50, 25)
    enemy = EnemyG2(12)
    run = True

    music_Game2 = pygame.mixer.music
    music_Game2.load('data\Game2.mp3')
    music_Game2.play()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_Exit = ask_exit()
                if is_Exit:
                    music_Game2.stop()
                    run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player.y - player.speed >= 50:
                    player.y -= player.speed
                elif event.key == pygame.K_DOWN and player.y + player.speed <= height:
                    player.y += player.speed

        screen.fill((0, 0, 0))

        pygame.draw.line(screen, (255, 0, 0), (0, 50), (width, 50))
        player.update()
        enemy.create()
        pygame.display.flip()


def ask_exit():
    def dont():
        font = pygame.font.Font(None, 50)
        ans = ['нет', 'да']

        txt = font.render('Вы действительно хотите выйти?', 1, (100, 255, 100))
        txt_x = width // 2 - txt.get_width() // 2
        txt_y = 0
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

        self.list_of_games.append('Ryder')
        self.list_of_games.append('Game_2')
        self.list_of_games.append('Выйти из игры')

    def draw(self):
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 50)

        for i in range(len(self.list_of_games)):
            S = 100
            text = font.render(self.list_of_games[i], 1, (100, 255, 100))
            self.text_x = width // 2 - text.get_width() // 2
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


menu = MainMenu()
music = pygame.mixer.music
music.load('data\MenuSong.mp3')  # Загрузка музыки
music.play()  # начало воспроизведения музыки
cof_limit = len(menu.list_of_games)
cof = 1
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
                    pass
                elif cof == 1:
                    music.stop()
                    Game2()
                    music.load('MenuSong.mp3')
                    music.play()
                elif cof == 2:
                    if ask_exit():
                        quit()

    screen.fill((0, 0, 0))
    menu.draw()
    menu.correct_game(cof)
    pygame.display.flip()

pygame.quit()
