#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Player import *
from Enemy import *
from blocks import *
from buttones import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
import ctypes
# import os
# Объявляем переменные
user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
FPS = 60
RED = (255, 0, 0)
GREEN = (0, 155, 55)
# PLATFORM_WIDTH = WIN_WIDTH / 48
# PLATFORM_HEIGHT = WIN_HEIGHT / 25.25
# PLATFORM_COLOR = "#FF6262"

Number_of_level = 1
is_game_over = False
running_1 = 0
is_pause_menu = False

up = False
timer = pygame.time.Clock()


def menu(bg, screen):
    """

    :param bg: background of game window
    :param screen: general screen of window
    :return:
    """
    global running_1, is_menu
    pygame.mixer.music.load("menu_music.mp3")
    pygame.mixer.music.play(-1)
    screen.fill(Color(GREEN))

    start_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 6 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                          WIN_HEIGHT / 15, 'Start')
    start_button.draw(screen)

    quit_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 1.5 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                         WIN_HEIGHT / 15, 'Quit')
    quit_button.draw(screen)

    pygame.display.update()
    run = True
    while run:
        timer.tick(FPS)
        for even in pygame.event.get():  # Обрабатываем события
            if even.type == QUIT:
                raise SystemExit("QUIT")
            if even.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                if start_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = False
                    running_1 = True
                    run = False
                if quit_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = False
                    running_1 = False
                    run = False
    pygame.display.update()
    return running_1, is_menu


def pause_menu(bg, screen):
    """

    :param bg:
    :param screen:
    :return:
    """
    global running_1, is_menu
    pygame.mixer.music.pause()

    continue_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 6 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                             WIN_HEIGHT / 15, 'Continue')
    continue_button.draw(screen)

    menu_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 6 - WIN_HEIGHT / 7, WIN_WIDTH / 3.2,
                         WIN_HEIGHT / 15, 'Menu')
    menu_button.draw(screen)

    pygame.display.update()

    run = True
    while run:
        timer.tick(FPS)
        for even in pygame.event.get():  # Обрабатываем события
            if even.type == QUIT:
                raise SystemExit("QUIT")
            if even.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                if continue_button.is_pressed(mouse_pos, mouse_pressed):
                    running_1 = 1
                    run = False
                if menu_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = True
                    running_1 = 0
                    run = False
        pygame.display.update()
    return running_1, is_menu


def game_over(bg, screen):
    """

    :param bg:
    :param screen:
    :return:
    """
    global is_menu, running_1, is_game_over
    pygame.mixer.music.stop()
    screen.fill(Color(WHITE))

    restart_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 2 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                            WIN_HEIGHT / 15, 'Restart')
    restart_button.draw(screen)

    menu_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 6 - WIN_HEIGHT / 7, WIN_WIDTH / 3.2,
                         WIN_HEIGHT / 15, 'Menu')
    menu_button.draw(screen)

    game_over_text = Button(RED, WIN_WIDTH / 2, WIN_HEIGHT / 2 - WIN_HEIGHT / 7, 0.1, 0.1, 'GAME OVER ^_^')
    game_over_text.draw(screen)
    pygame.display.update()
    run = True
    while run:
        timer.tick(FPS)
        for even in pygame.event.get():  # Обрабатываем события
            if even.type == QUIT:
                raise SystemExit("QUIT")
            if even.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                if restart_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = False
                    running_1 = True
                    is_game_over = False
                    run = False
                if menu_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = True
                    is_game_over = False
                    run = False
    pygame.display.update()
    return is_menu, running_1, is_game_over


def level_1(bg, screen):
    global is_game_over, running_1, is_menu

    pygame.mixer.music.load("chocolate-chip-by-uncle-morris.mp3")
    pygame.mixer.music.play(-1)

    typical_enemy = Enemy(WIN_WIDTH / 7, WIN_HEIGHT / 2.65)
    hero = Player(PLATFORM_WIDTH, WIN_HEIGHT - PLATFORM_HEIGHT)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию — стоим
    Up = False
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    level_exits = []
    enemies = []
    entities.add(hero)
    entities.add(typical_enemy)
    enemies.append(typical_enemy)

    level = [
        "------------------------------------------------",
        "-                                               ",
        "-                   ---           --           *",
        "-                        -   --                 ",
        "-            --                        --      -",
        "-                    --      -   --            -",
        "--                                       --    -",
        "-            -              --                 -",
        "-                     -               --       -",
        "-                                              -",
        "-              -    --            --           -",
        "-    -----                                     -",
        "-                          --        -         -",
        "-      --------                                -",
        "-                                ---           -",
        "-                -                             -",
        "-                   --          ------         -",
        "-       ----                                   -",
        "-                                    -----     -",
        "-                      --                      -",
        "-                                              -",
        "-                             ----             -",
        "-                                              -",
        "-                                              -",
        "------------------------------------------------"]

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                # создаем блок, заливаем его цветом и рисеум его
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                level_exit = Level_exit(x, y)
                entities.add(level_exit)
                level_exits.append(level_exit)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0

    run = True
    while run:
        timer.tick(FPS)
        if running_1 == 1:
            for event in pygame.event.get():  # Обрабатываем события
                if event.type == QUIT:
                    raise SystemExit("QUIT")
                if event.type == KEYDOWN and event.key == K_UP:
                    Up = True
                if event.type == KEYDOWN and event.key == K_w:
                    Up = True
                if event.type == KEYUP and event.key == K_UP:
                    Up = False
                if event.type == KEYUP and event.key == K_w:
                    Up = False
                if event.type == KEYDOWN and event.key == K_LEFT:
                    left = True
                if event.type == KEYDOWN and event.key == K_a:
                    left = True
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    right = True
                if event.type == KEYDOWN and event.key == K_d:
                    right = True
                if event.type == KEYUP and event.key == K_RIGHT:
                    right = False
                if event.type == KEYUP and event.key == K_d:
                    right = False
                if event.type == KEYUP and event.key == K_LEFT:
                    left = False
                if event.type == KEYUP and event.key == K_a:
                    left = False
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    running_1 = 2

            hero.collide_enemy(enemies, hero)
            if hero.health > 0:
                screen.blit(bg, (0, 0))  # Каждую итерацию движения перса необходимо всё перерисовывать
                hero.update(left, right, Up, platforms)  # передвижение
                typical_enemy.update()
                entities.draw(screen)  # отображение
                for e in level_exits:
                    if sprite.collide_rect(hero, e):
                        running_1 = 0
                        run = False
                        is_menu = True
            elif hero.health <= 0:
                is_game_over = True
                run = False
                running_1 = 0
                game_over(bg, screen)
            pygame.display.update()  # обновление и вывод всех изменений на экран
        elif running_1 == 2:
            while running_1 == 2:
                pause_menu(bg, screen)
        elif running_1 == 0:
            run = False

    return is_game_over, running_1


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)
    # screen = pygame.display.set_mode(DISPLAY, pygame.DOUBLEBUF | pygame.OpenGL)  # Создаем окошко
    pygame.display.set_caption("SUPER FOPF BOY")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности,   будем использовать как фон
    # running = False
    # glClearColor(BACKGROUND_COLOR/255, 1)
    menu(bg, screen)
    runnin = True
    while runnin:
        if is_menu:
            while is_menu:
                menu(bg, screen)
        elif running_1 != 0:
            while running_1:
                level_1(bg, screen)
        elif is_game_over:
            while is_game_over:
                game_over(bg, screen)
        else:
            runnin = False


if __name__ == "__main__":
    main()
