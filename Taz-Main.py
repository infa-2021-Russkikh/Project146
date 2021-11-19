#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from Player import *
from Enemy import *
from blocks import *
from buttones import *
from OpenGL.GL import *
from OpenGL.GLU import *
import ctypes

# Объявляем переменные
user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
FPS = 60
RED = (255, 0, 0)
GREEN = (0, 155, 55)
# PLATFORM_WIDTH = 32
# PLATFORM_HEIGHT = 32
# PLATFORM_COLOR = "#FF6262"
is_game_over = False
running_1 = False

up = False
timer = pygame.time.Clock()


def menu(bg, screen):
    global running_1, is_menu
    screen.fill(Color(GREEN))
    start_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 6 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                              WIN_HEIGHT / 15, 'Start')
    start_button.draw(screen)
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
    pygame.display.update()
    return running_1, is_menu


def game_over(bg, screen):
    global is_menu, running_1, is_game_over
    screen.fill(Color(WHITE))
    restart_button = Button(RED, WIN_WIDTH/2 - WIN_WIDTH/6.2, WIN_HEIGHT/2 - WIN_HEIGHT/27, WIN_WIDTH/3.2,
                              WIN_HEIGHT/15, 'GAME OVER ^_^')
    restart_button.draw(screen)
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
    pygame.display.update()
    return is_menu, running_1, is_game_over


def level_1(bg, screen):
    global is_game_over, running_1
    typical_enemy = Enemy(WIN_WIDTH / 7, WIN_HEIGHT / 2.65)
    hero = Player(WIN_WIDTH / 35, WIN_HEIGHT / 19.6)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию — стоим
    up = False
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    enemies = []
    entities.add(hero)
    entities.add(typical_enemy)

    level = [
        "------------------------------------------------",
        "-                                              -",
        "-                                              -",
        "-                                              -",
        "-            --                                -",
        "-                            -   --            -",
        "--                                             -",
        "-                                              -",
        "-                   ---                        -",
        "-                                              -",
        "-                   --            --           -",
        "-    -----                                     -",
        "-                                              -",
        "-      --------                                -",
        "-                                ---           -",
        "-                -                             -",
        "-                   --                         -",
        "-       ----                                   -",
        "-                                    -----     -",
        "-                      --                      -",
        "-                                              -",
        "-                             ----             -",
        "-                                              -",
        "-                                              -",
        "------------------------------------------------"]

    enemies.append(typical_enemy)

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                # создаем блок, заливаем его цветом и рисеум его
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0
    pygame.display.update()
    run = True
    while run:
        timer.tick(FPS)
        for event in pygame.event.get():  # Обрабатываем события
            if event.type == QUIT:
                raise SystemExit("QUIT")
            if event.type == KEYDOWN and event.key == K_UP:
                up = True
            if event.type == KEYUP and event.key == K_UP:
                up = False
            if event.type == KEYDOWN and event.key == K_LEFT:
                left = True
            if event.type == KEYDOWN and event.key == K_RIGHT:
                right = True
            if event.type == KEYUP and event.key == K_RIGHT:
                right = False
            if event.type == KEYUP and event.key == K_LEFT:
                left = False

        hero.collide_enemy(enemies, hero)

        if hero.health > 0:
            screen.blit(bg, (0, 0))  # Каждую итерацию движения перса необходимо всё перерисовывать
            hero.update(left, right, up, platforms)  # передвижение
            typical_enemy.update()
            entities.draw(screen)  # отображение
        elif hero.health <= 0:
            is_game_over = True
            run = False
            running_1 = False
            game_over(bg, screen)
        pygame.display.update()  # обновление и вывод всех изменений на экран
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
        elif running_1:
            while running_1:
                level_1(bg, screen)
        elif is_game_over:
            while is_game_over:
                game_over(bg, screen)


if __name__ == "__main__":
    main()
