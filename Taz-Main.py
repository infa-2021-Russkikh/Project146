#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame import *
from Player import *
from blocks import *
import ctypes

# Объявляем переменные
user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55
DISPLAY = (WIN_WIDTH, WIN_HEIGHT) # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
# PLATFORM_WIDTH = 32
# PLATFORM_HEIGHT = 32
# PLATFORM_COLOR = "#FF6262"
up = False
timer = pygame.time.Clock()


def main():
    hero = Player(55, 55)  # создаем героя по (x,y) координатам
    left = right = False    # по умолчанию — стоим
    up = False
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    entities.add(hero)

    level = [
       "------------------------------------------------",
       "-                                              -",
       "-                                              -",
       "-                                              -",
       "-            --                                -",
       "-                                              -",
       "--                                             -",
       "-                                              -",
       "-                   ---                        -",
       "-                                              -",
       "-                                              -",
       "-      ---                                     -",
       "-                                              -",
       "-   -----------                                -",
       "-                                              -",
       "-                -                             -",
       "-                   --                         -",
       "-                                              -",
       "-                                              -",
       "-                                              -",
       "-                                              -",
       "-                                              -",
       "-                                              -",
       "-                                              -",
       "------------------------------------------------"]
    
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("SUPER FOPF BOY")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
                                         # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))     # Заливаем поверхность сплошным цветом

    while 1:  # Основной цикл программы
        timer.tick(60)
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
        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        x=y=0 # координаты
        for row in level: # вся строка
            for col in row: # каждый символ
                if col == "-":
                  # создаем блок, заливаем его цветом и рисеум его
                    pf = Platform(x,y)
                    entities.add(pf)
                    platforms.append(pf)
                    
                x += PLATFORM_WIDTH # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT    # то же самое и с высотой
            x = 0
        hero.update(left, right, up ) # передвижение
        entities.draw(screen) # отображение
        pygame.display.update()     # обновление и вывод всех изменений на экран
        

if __name__ == "__main__":
    main()
