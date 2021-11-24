#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Player import *
from Enemy import *
from textures import *
from buttones import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
import ctypes
import json
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

with open("saves.json", 'r') as f:
    dict = json.load(f)

Number_of_level = 1
gallery_pictures = []
is_landay = dict["is_landay"]
gallery_pictures.append(is_landay)
is_menu = False
is_options_menu = False
is_gallery_menu = False
menu_music = False
is_levels = False
is_game_over = False
running_1 = 0
is_pause_menu = False


# def get_data():
#     with open("saves.json", "wb") as fp:
#         pickle.dump(gallery_pictures, fp)
#
#
# def saves_data():
#     with open("saves.json", "rb") as fp:
#         gallery_pictures = pickle.load(fp)

up = False
timer = pygame.time.Clock()


def menu(bg, screen):
    """

    :param bg: background of game window
    :param screen: general screen of window
    :return:
    """
    global running_1, is_menu, is_levels, menu_music, is_gallery_menu, is_options_menu
    if not menu_music:
        pygame.mixer.music.load("Music/menu_music.mp3")
        pygame.mixer.music.play(-1)
    bg = pygame.image.load("Textures/additional task.png")
    screen.blit(bg, (0, 0))
    # screen.fill(Color(GREEN))

    start_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 6 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                          WIN_HEIGHT / 15, 'Start')
    start_button.draw(screen)

    levels_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 3 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                           WIN_HEIGHT / 15, 'Levels')
    levels_button.draw(screen)

    options_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 2 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                            WIN_HEIGHT / 15, 'Options')
    options_button.draw(screen)

    gallery_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 1.5 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                           WIN_HEIGHT / 15, 'Gallery')
    gallery_button.draw(screen)

    quit_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 1.2 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
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
                    menu_music = False
                    running_1 = True
                    run = False
                if quit_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = False
                    running_1 = False
                    run = False
                if levels_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = False
                    menu_music = True
                    is_levels = True
                    run = False
                if gallery_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = False
                    menu_music = True
                    is_gallery_menu = True
                    run = False
                if options_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = False
                    menu_music = True
                    is_options_menu = True
                    run = False
    pygame.display.update()
    return running_1, is_menu, is_levels, menu_music, is_gallery_menu, is_options_menu


def level_menu(bg, screen):
    """

    :param screen:
    :return:
    """
    global is_menu, running_1, is_levels

    bg = pygame.image.load("Textures/additional task.png")
    screen.blit(bg, (0, 0))
    # screen.fill(Color(GREEN))

    level_1_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 3 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                            WIN_HEIGHT / 15, 'Level 1')
    level_1_button.draw(screen)

    back_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 1.2 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                         WIN_HEIGHT / 15, 'Back')
    back_button.draw(screen)

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
                if level_1_button.is_pressed(mouse_pos, mouse_pressed):
                    running_1 = True
                    is_levels = False
                    run = False
                if back_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = True
                    is_levels = False
                    run = False


def gallery_menu(bg, screen):
    global is_menu, menu_music, is_gallery_menu

    screen.fill(Color(GREEN))

    if not is_landay:
        picture_1_image = pygame.image.load("Textures/invisible_person.png")
        picture_1_image_rect = picture_1_image.get_rect(center=(200, 150))
        screen.blit(picture_1_image, picture_1_image_rect)
    else:
        picture_1_image = pygame.image.load("Textures/gallery_landay_picture.png")
        picture_1_image_rect = picture_1_image.get_rect(center=(200, 150))
        screen.blit(picture_1_image, picture_1_image_rect)

    back_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 1.2 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                         WIN_HEIGHT / 15, 'Back')
    back_button.draw(screen)

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
                if back_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = True
                    is_gallery_menu = False
                    run = False
        return is_gallery_menu, is_menu, menu_music


def options_menu(bg, screen):
    global is_menu, menu_music, is_options_menu, is_landay, dict

    screen.fill(Color(GREEN))

    back_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 1.2 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                         WIN_HEIGHT / 15, 'Back')
    back_button.draw(screen)

    reset_progress_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 6 - WIN_HEIGHT / 27,
                                   WIN_WIDTH / 3.2, WIN_HEIGHT / 15, 'Reset progress')
    reset_progress_button.draw(screen)

    run = True
    while run:
        timer.tick(FPS)
        for even in pygame.event.get():  # Обрабатываем события
            if even.type == QUIT:
                raise SystemExit("QUIT")
            if even.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                if back_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = True
                    is_options_menu = False
                    run = False
                if reset_progress_button.is_pressed(mouse_pos, mouse_pressed):
                    is_landay = 0
                    dict["is_landay"] = 0
                    with open("saves.json", 'w') as f:
                        json.dump(dict, f)
                    with open("saves.json", 'r') as f:
                        dict = json.load(f)

        pygame.display.update()
        return is_options_menu, is_menu, menu_music, is_landay


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
    pygame.mixer.music.unpause()
    return running_1, is_menu


def game_over(bg, screen):
    """

    :param bg:
    :param screen:
    :return:
    """
    global is_menu, running_1, is_game_over
    pygame.mixer.music.load('Music/game_over.mp3')
    pygame.mixer.music.play()
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
    """

    :param bg:
    :param screen:
    :return:
    """
    global is_game_over, running_1, is_menu, is_landay, menu_music

    pygame.mixer.music.load("Music/chocolate-chip-by-uncle-morris.mp3")
    pygame.mixer.music.play(-1)

    typical_enemy_1 = Enemy(WIN_WIDTH / 7, WIN_HEIGHT / 2.65)
    typical_enemy_2 = Enemy(WIN_WIDTH / 1.2, WIN_HEIGHT / 5.6)
    typical_enemy_3 = Enemy(WIN_WIDTH / 1.38, WIN_HEIGHT / 3.8, 2)
    typical_enemy_4 = Enemy(WIN_WIDTH / 1.535, WIN_HEIGHT / 1.29)

    hero = Player(PLATFORM_WIDTH, WIN_HEIGHT - PLATFORM_HEIGHT)  # создаем героя по (x,y) координатам
    left = right = False  # по умолчанию — стоим
    Up = False

    landay = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    level_exits = []
    enemies = []
    gallery_features = []

    entities.add(hero)
    entities.add(typical_enemy_1, typical_enemy_2, typical_enemy_3, typical_enemy_4)
    enemies.append(typical_enemy_1)
    enemies.append(typical_enemy_2)
    enemies.append(typical_enemy_3)
    enemies.append(typical_enemy_4)

    level = [
        "------------------------------------------------",
        "-                                               ",
        "-                                              *",
        "-                  --                           ",
        "-             --                               -",
        "-                       -        -             -",
        "-                                      ----    -",
        "-              -            --                 -",
        "-                       -        -----         -",
        "-                                              -",
        "-              -                               -",
        "-    -----                            -        -",
        "-                                              -",
        "-      --------                                -",
        "-                                         -    -",
        "-                -                             -",
        "-                   --                    c    -",
        "-                                         -    -",
        "-                                              -",
        "-                      --            -         -",
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
            if not is_landay:
                if col == "c":
                    gallery_landay = "gallery_landay"
                    gallery_feature = Gallery_feature(x, y, gallery_landay)
                    entities.add(gallery_feature)
                    gallery_features.append(gallery_feature)

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
                typical_enemy_1.update()
                typical_enemy_2.update()
                typical_enemy_3.update(26)
                typical_enemy_4.update(35)
                entities.draw(screen)  # отображение

                for e in level_exits:
                    if sprite.collide_rect(hero, e):

                        if landay:
                            is_landay = 1
                            dict["is_landay"] = 1
                            with open("saves.json", 'w') as f:
                                json.dump(dict, f)

                        menu_music = True
                        running_1 = 0
                        run = False
                        is_menu = True
                for g in gallery_features:
                    if sprite.collide_rect(hero, g):
                        entities.remove(gallery_feature)
                        landay = True
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

    return is_game_over, running_1, is_landay, is_menu, menu_music


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)
    # screen = pygame.display.set_mode(DISPLAY, pygame.DOUBLEBUF | pygame.OpenGL)  # Создаем окошко
    pygame.display.set_caption("SUPER FOPF BOY")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности, будем использовать как фон
    # glClearColor(BACKGROUND_COLOR/255, 1)

    # get_data()

    menu(bg, screen)
    runnin = True
    while runnin:
        if is_menu:
            while is_menu:
                menu(bg, screen)
        elif is_levels:
            while is_levels:
                level_menu(bg, screen)
        elif is_gallery_menu:
            while is_gallery_menu:
                gallery_menu(bg, screen)
        elif is_options_menu:
            while is_options_menu:
                options_menu(bg, screen)
        elif running_1 != 0:
            while running_1:
                level_1(bg, screen)
        elif is_game_over:
            while is_game_over:
                game_over(bg, screen)
        else:
            # saves_data()
            runnin = False


if __name__ == "__main__":
    main()
