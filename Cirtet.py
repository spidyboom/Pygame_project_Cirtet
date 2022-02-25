import pygame
from copy import deepcopy
from random import choice, randrange


def check(num):
    if figure[num].x < 0 or figure[num].x > W - 1:
        return False
    elif figure[num].y > H - 1 or field[figure[num].y][figure[num].x]:
        return False
    return True

def simple_game():
    global lines
    global field
    global anim_cnt, anim_spd, anim_lmt
    global color
    global next_color
    global next_figure
    global figure

    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.blit(game_sc, (20, 20))
    game_sc.blit(game_bg, (0, 0))
    end_color = 'blue'
    sc.blit(next_figures, (490, 320))

    for i in range(lines):
        pygame.time.wait(200)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_lmt = 100
            elif event.key == pygame.K_UP:
                rotate = True

    figure_old = deepcopy(figure)
    for num in range(4):
        figure[num].x += dx
        if not check(num):

            figure = deepcopy(figure_old)
            break

    anim_cnt += anim_spd
    if anim_cnt > anim_lmt:
        anim_cnt = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check(i):
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_lmt = 2000
                break

    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check(i):
                figure = deepcopy(figure_old)
                break

    line, lines = H - 1, 0
    for row in range(H - 1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            lines += 1

    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

    for i in range(4):
        figure_rect.x = figure[i].x * TILE
        figure_rect.y = figure[i].y * TILE
        pygame.draw.rect(game_sc, color, figure_rect)

    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)
                # здесь

    for i in range(4):
        figure_rect.x = next_figure[i].x * TILE + 380
        figure_rect.y = next_figure[i].y * TILE + 385
        pygame.draw.rect(sc, next_color, figure_rect)

    sc.blit(title_cirtet, (520, 20))

    for i in range(W):
        if field[0][i]:
            field = [[0 for i in range(W)] for i in range(H)]
            anim_cnt, anim_spd, anim_lmt = 0, 60, 2000
            for i_rect in grid:
                pygame.draw.rect(game_sc, end_color, i_rect)
                sc.blit(game_sc, (20, 20))
                pygame.display.flip()
                clock.tick(200)
                pygame.mixer.music.pause()
                pygame.mixer.music.play(-1)


    pygame.display.flip()
    clock.tick(FPS)


W, H = 10, 15
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 740, 700
FPS = 60
figures_pos = [[(0, 0), (0, -1), (0, 1), (-1, 0)],
               [(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

pygame.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()
pygame.mixer.music.load("sounds/lume-young-man(mp3novinki.net).mp3")

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

anim_cnt, anim_spd, anim_lmt = 0, 60, 2000

bg = pygame.image.load('data/Game_Fone.jpg').convert()
game_bg = pygame.image.load('data/Tile_Fone.jpg').convert()


name_Cirtet = pygame.font.Font('font/font.ttf', 45)
font = pygame.font.Font('font/font.ttf', 20)

title_cirtet = name_Cirtet.render('Cirtet', True, pygame.Color('cornflowerblue'))
next_figures = font.render('Следуящая фигура:', True, pygame.Color('purple'))

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure, lines = deepcopy(choice(figures)), deepcopy(choice(figures)), 0
color, next_color = get_color(), get_color()

pygame.mixer.music.play(-1)
while True:
    simple_game()
