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
# PLATFORM_WIDTH = 32
# PLATFORM_HEIGHT = 32
# PLATFORM_COLOR = "#FF6262"

up = False
timer = pygame.time.Clock()


def game_over(bg, screen):
    screen.fill(Color(WHITE))
    game_over_button = Button(RED, WIN_WIDTH/2 - WIN_WIDTH/19.2, WIN_HEIGHT/2 - WIN_HEIGHT/27, WIN_WIDTH/19.2,
                              WIN_HEIGHT/27, 'GAME OVER ^_^')
    game_over_button.draw(screen)



def main():
    typical_enemy = Enemy(WIN_WIDTH/7, WIN_HEIGHT/2.65)
    hero = Player(WIN_WIDTH/35, WIN_HEIGHT/19.6)  # создаем героя по (x,y) координатам
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

    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)
    # screen = pygame.display.set_mode(DISPLAY, pygame.DOUBLEBUF | pygame.OpenGL)  # Создаем окошко
    pygame.display.set_caption("SUPER FOPF BOY")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности,   будем использовать как фон
    # glClearColor(BACKGROUND_COLOR/255, 1)

    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

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
    running = True
    while running:  # Основной цикл программы
        timer.tick(FPS)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                raise SystemExit("QUIT")
        if e.type == KEYDOWN and e.key == K_UP:
            up = True
        if e.type == KEYUP and e.key == K_UP:
            up = False
        if e.type == KEYDOWN and e.key == K_LEFT:
            left = True
        if e.type == KEYDOWN and e.key == K_RIGHT:
            right = True
        if e.type == KEYUP and e.key == K_RIGHT:
            right = False
        if e.type == KEYUP and e.key == K_LEFT:
            left = False

        # glClear(GL_COLOR_BUFFER_BIT)
        hero.collide_enemy(enemies, hero)

        if hero.health > 0:
            screen.blit(bg, (0, 0))  # Каждую итерацию движения перса необходимо всё перерисовывать
            hero.update(left, right, up, platforms)  # передвижение
            typical_enemy.update()
            entities.draw(screen)  # отображение
        elif hero.health <= 0:
            game_over(bg, screen)
            # running = False
        pygame.display.update()  # обновление и вывод всех изменений на экран


if __name__ == "__main__":
    main()
