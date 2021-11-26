#!/usr/bin/env python
# -*- coding: utf-8 -*-
import Level_1
from Player import *
from Enemy import *
from textures import *
from buttones import *
# from OpenGL.GL import *
# from OpenGL.GLU import *
import datetime
import ctypes
import json

# Объявляем переменные
user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#004400"
FPS = 60
RED = (255, 0, 0)
GREEN = (0, 155, 55)
GREY = (50, 50, 50)
dt = datetime.datetime.now() - datetime.datetime.now()
# PLATFORM_WIDTH = WIN_WIDTH / 48
# PLATFORM_HEIGHT = WIN_HEIGHT / 25.25
# PLATFORM_COLOR = "#FF6262"

with open("saves.json", 'r') as f:
    dict = json.load(f)

music_volume = dict["music_volume"]
Number_of_level = 0
gallery_pictures = []
amount_passed_levels = dict["amount_passed_levels"]
is_landay = dict["is_landay"]
is_einstein = dict["is_einstein"]
gallery_pictures.append(is_landay)
is_menu = False
is_options_menu = False
is_gallery_menu = False
menu_music = False
is_levels = False
is_game_over = False
is_pass_level_screen = False
running_1 = 0
running_2 = 0
is_pause_menu = False
switch_pause = False
is_restart = False
is_achievements_menu = False

up = False
timer = pygame.time.Clock()


def menu(bg, screen):
    """

    :param bg: background of game window
    :param screen: general screen of window
    :return:
    """
    global running_1, is_menu, is_levels, menu_music, is_gallery_menu, is_options_menu, dict, is_achievements_menu
    if not menu_music:
        pygame.mixer.music.set_volume(dict["music_volume"])
        pygame.mixer.music.load("Music/menu_music.mp3")
        pygame.mixer.music.play(-1)
    # bg = pygame.image.load("Textures/additional task.png")
    # screen.blit(bg, (0, 0))
    screen.fill(Color(GREEN))

    start_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT*2, WIN_WIDTH / 3.2,
                          PLATFORM_HEIGHT*2, 'Start')
    start_button.draw(screen)

    levels_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT*6, WIN_WIDTH / 3.2,
                           PLATFORM_HEIGHT*2, 'Levels')
    levels_button.draw(screen)

    options_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT*10, WIN_WIDTH / 3.2,
                            PLATFORM_HEIGHT*2, 'Options')
    options_button.draw(screen)

    gallery_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT*14, WIN_WIDTH / 3.2,
                            PLATFORM_HEIGHT*2, 'Gallery')
    gallery_button.draw(screen)

    achievements_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT*18,
                                 WIN_WIDTH / 3.2, PLATFORM_HEIGHT*2, 'Achievements')
    achievements_button.draw(screen)

    quit_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT*22, WIN_WIDTH / 3.2,
                         PLATFORM_HEIGHT*2, 'Quit')
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
                if achievements_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = False
                    menu_music = True
                    is_achievements_menu = True
                    run = False
    pygame.display.update()
    return running_1, is_menu, is_levels, menu_music, is_gallery_menu, is_options_menu


def level_menu(bg, screen):
    """

    :param screen:
    :return:
    """
    global is_menu, running_1, running_2, is_levels, amount_passed_levels

    bg = pygame.image.load("Textures/additional task.png")
    # screen.blit(bg, (0, 0))
    screen.fill(Color(GREEN))

    level_1_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 3 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                            WIN_HEIGHT / 15, 'Level 1')
    level_1_button.draw(screen)

    if amount_passed_levels < 1:
        level_2_button = Button(GREY, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 2 - WIN_HEIGHT / 27,
                                WIN_WIDTH / 3.2,
                                WIN_HEIGHT / 15, 'Level 2')

        cannot_button = Button(GREY, WIN_WIDTH / 2, WIN_HEIGHT / 2 - WIN_HEIGHT / 29, 0.1, 0.1,
                               'Firstly, pass all previous levels')
    else:
        level_2_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 2 - WIN_HEIGHT / 27,
                                WIN_WIDTH / 3.2,
                                WIN_HEIGHT / 15, 'Level 2')
    level_2_button.draw(screen)

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
                if level_2_button.is_pressed(mouse_pos, mouse_pressed):
                    if amount_passed_levels < 1:
                        cannot_button.draw(screen, RED)
                        pygame.display.update()
                    else:
                        running_2 = True
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

    if not is_einstein:
        picture_2_image = pygame.image.load("Textures/invisible_person.png")
        picture_2_image_rect = picture_2_image.get_rect(center=(500, 150))
        screen.blit(picture_2_image, picture_2_image_rect)
    else:
        picture_2_image = pygame.image.load("Textures/gallery_einstein_picture.png")
        picture_2_image_rect = picture_2_image.get_rect(center=(500, 150))
        screen.blit(picture_2_image, picture_2_image_rect)

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
    global is_menu, menu_music, is_options_menu, is_landay, dict, amount_passed_levels

    screen.fill(Color(GREEN))

    back_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 1.2 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                         WIN_HEIGHT / 15, 'Back')
    back_button.draw(screen)

    music_off_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 1.5 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                              WIN_HEIGHT / 15, 'Music off')
    music_off_button.draw(screen)

    music_on_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 2 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                             WIN_HEIGHT / 15, 'Music on')
    music_on_button.draw(screen)

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
                if music_off_button.is_pressed(mouse_pos, mouse_pressed):
                    pygame.mixer.music.set_volume(0)
                    dict["music_volume"] = 0
                    with open("saves.json", 'w') as f:
                        json.dump(dict, f)
                    with open("saves.json", 'r') as f:
                        dict = json.load(f)
                if music_on_button.is_pressed(mouse_pos, mouse_pressed):
                    pygame.mixer.music.set_volume(1)
                    dict["music_volume"] = 1
                    with open("saves.json", 'w') as f:
                        json.dump(dict, f)
                    with open("saves.json", 'r') as f:
                        dict = json.load(f)
                if reset_progress_button.is_pressed(mouse_pos, mouse_pressed):
                    amount_passed_levels = 0
                    is_landay = 0
                    dict["amount_passed_levels"] = 0
                    dict["is_landay"] = 0
                    with open("saves.json", 'w') as f:
                        json.dump(dict, f)
                    with open("saves.json", 'r') as f:
                        dict = json.load(f)

        pygame.display.update()
        return is_options_menu, is_menu, menu_music, is_landay, amount_passed_levels


def achievements_menu(bg, screen):
    global is_menu, menu_music, is_achievements_menu, dict

    screen.fill(Color(GREEN))

    level_1_name = Button(GREEN, PLATFORM_WIDTH * 5, PLATFORM_HEIGHT * 3, PLATFORM_WIDTH,
                          PLATFORM_HEIGHT, 'level 1')
    level_2_name = Button(GREEN, PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 3, PLATFORM_WIDTH,
                          PLATFORM_HEIGHT, 'level 2')

    try:
        level_1_record = Button(GREEN, PLATFORM_WIDTH * 5, PLATFORM_HEIGHT * 5, PLATFORM_WIDTH,
                                PLATFORM_HEIGHT, f'{dict["your_time_seconds_1"]}')
        level_2_record = Button(GREEN, PLATFORM_WIDTH * 5, PLATFORM_HEIGHT * 5, PLATFORM_WIDTH,
                                PLATFORM_HEIGHT, f'{dict["your_time_seconds_2"]}')
    except:
        level_1_record = Button(GREEN, PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 5, PLATFORM_WIDTH,
                                PLATFORM_HEIGHT, "Empty -_-")
        level_2_record = Button(GREEN, PLATFORM_WIDTH * 5, PLATFORM_HEIGHT * 5, PLATFORM_WIDTH,
                                PLATFORM_HEIGHT, "Empty -_-")

    level_1_record.draw(screen, Color=WHITE)
    level_2_record.draw(screen, Color=WHITE)
    level_1_name.draw(screen)
    level_2_name.draw(screen)

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
                    is_achievements_menu = False
                    run = False
        return is_achievements_menu, is_menu, menu_music


def pause_menu(bg, screen):
    """

    :param bg:
    :param screen:
    :return:
    """
    global running_1, is_menu, Number_of_level, running_2, menu_music, switch_pause, dt, date_time_obj4
    pygame.mixer.music.pause()

    pause_bg = pygame.image.load("Textures/pause_bg.png")
    screen.blit(pause_bg, (PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 1))

    continue_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 6 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                             WIN_HEIGHT / 15, 'Continue')
    continue_button.draw(screen)

    menu_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 2, WIN_WIDTH / 3.2,
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
                    if Number_of_level == 1:
                        running_1 = 1
                        dt += datetime.datetime.now() - date_time_obj4
                    elif Number_of_level == 2:
                        running_2 = 1
                        dt += datetime.datetime.now() - date_time_obj4
                    run = False
                if menu_button.is_pressed(mouse_pos, mouse_pressed):
                    dt = datetime.datetime.now() - datetime.datetime.now()
                    is_menu = True
                    running_1 = 0
                    running_2 = 0
                    menu_music = False
                    run = False
        pygame.display.update()
    pygame.mixer.music.unpause()
    return running_1, is_menu, switch_pause, dt, date_time_obj4


def game_over(bg, screen):
    """

    :param bg:
    :param screen:
    :return:
    """
    global is_menu, running_1, is_game_over, running_2, Number_of_level, dict, menu_music, dt

    dt = datetime.datetime.now() - datetime.datetime.now()

    pygame.mixer.music.set_volume(dict["music_volume"])
    pygame.mixer.music.load('Music/game_over.mp3')
    pygame.mixer.music.play()
    screen.fill(Color(WHITE))

    restart_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 2 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                            WIN_HEIGHT / 15, 'Restart')
    restart_button.draw(screen)

    menu_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 1.2 - WIN_HEIGHT / 7, WIN_WIDTH / 3.2,
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
                    if Number_of_level == 1:
                        running_1 = 1
                    elif Number_of_level == 2:
                        running_2 = 1
                    is_game_over = False
                    run = False
                if menu_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = True
                    menu_music = False
                    is_game_over = False
                    run = False
    pygame.display.update()
    return is_menu, running_1, is_game_over, menu_music, running_2


def restart():
    global running_1, running_2, is_restart, is_menu, Number_of_level
    is_menu = False
    if Number_of_level == 1:
        running_1 = 1
    elif Number_of_level == 2:
        running_2 = 1
    is_restart = False


def pass_level_screen(bg, screen, your_time):
    global running_1, is_menu, Number_of_level, running_2, menu_music, switch_pause, dt, \
        date_time_obj4, is_pass_level_screen, is_restart

    pause_bg = pygame.image.load("Textures/pause_bg.png")
    screen.blit(pause_bg, (PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 1))

    next_level_button = Button(RED, PLATFORM_WIDTH * 20, WIN_HEIGHT / 6 - WIN_HEIGHT / 27,
                               PLATFORM_WIDTH * 8,
                               WIN_HEIGHT / 15, 'Next_level')
    next_level_button.draw(screen, size=48)

    what_time_button = Button(RED, PLATFORM_WIDTH * 24, PLATFORM_HEIGHT * 13, 0.000001,
                              0.000001, f'{your_time}')
    what_time_button.draw(screen, size=48, Color=WHITE)

    restart_button = Button(RED, PLATFORM_WIDTH * 21, PLATFORM_HEIGHT * 8, PLATFORM_WIDTH * 6,
                            PLATFORM_HEIGHT * 2, 'Restart')
    restart_button.draw(screen, size=48)

    menu_button = Button(RED, WIN_WIDTH / 2 - PLATFORM_WIDTH * 2, WIN_HEIGHT / 2 + PLATFORM_HEIGHT * 2,
                         PLATFORM_WIDTH * 4,
                         WIN_HEIGHT / 15, 'Menu')
    menu_button.draw(screen, size=48)

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
                if next_level_button.is_pressed(mouse_pos, mouse_pressed):
                    dt = datetime.datetime.now() - datetime.datetime.now()
                    if Number_of_level == 1:
                        running_1 = 0
                        is_pass_level_screen = False
                        running_2 = 1
                    # elif Number_of_level == 2:
                    #     running_2 = 0
                    #     is_pass_level_screen = False
                    run = False
                if menu_button.is_pressed(mouse_pos, mouse_pressed):
                    dt = datetime.datetime.now() - datetime.datetime.now()
                    is_menu = True
                    running_1 = 0
                    is_pass_level_screen = False
                    menu_music = False
                    run = False
                if restart_button.is_pressed(mouse_pos, mouse_pressed):
                    dt = datetime.datetime.now() - datetime.datetime.now()
                    if Number_of_level == 1:
                        is_restart = True
                        running_1 = 0
                        is_pass_level_screen = False
                    if Number_of_level == 2:
                        is_restart = True
                        is_pass_level_screen = False
                        running_2 = 0
                    run = False
        pygame.display.update()
    pygame.mixer.music.unpause()
    return running_1, is_menu, switch_pause, dt, is_pass_level_screen, running_2


def level_1(bg, screen):
    """

    :param bg:
    :param screen:
    :return:
    """
    global is_game_over, running_1, is_menu, is_landay, menu_music, Number_of_level, amount_passed_levels, dict, \
        switch_pause, date_time_obj4, is_pass_level_screen
    Number_of_level = 1

    date_time_obj1 = datetime.datetime.now()

    pygame.mixer.music.set_volume(dict["music_volume"])
    pygame.mixer.music.load("Music/chocolate-chip-by-uncle-morris.mp3")
    pygame.mixer.music.play(-1)

    typical_enemy_1 = Enemy(WIN_WIDTH / 7, PLATFORM_HEIGHT * 10)
    typical_enemy_2 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 7.5, PLATFORM_HEIGHT * 5)
    typical_enemy_3 = Enemy(WIN_WIDTH / 1.38, PLATFORM_HEIGHT * 7, 2)
    typical_enemy_4 = Enemy(WIN_WIDTH / 1.535, PLATFORM_HEIGHT * 20)

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
        "-              -        c   --                 -",
        "-                       -        -----         -",
        "-                                              -",
        "-              -                               -",
        "-    -----                            -        -",
        "-                                              -",
        "-          ----                                -",
        "-                                         -    -",
        "-                -                             -",
        "-                   --                         -",
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
                level_exit = Platform(x, y, "exit_door")
                entities.add(level_exit)
                level_exits.append(level_exit)
            if not is_landay:
                if col == "c":
                    gallery_landay = "gallery_landay"
                    gallery_feature = Platform(x, y, gallery_landay)
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
                    switch_pause = True

            hero.collide_enemy(enemies, hero)
            if hero.health > 0:
                screen.blit(bg, (0, 0))  # Каждую итерацию движения перса необходимо всё перерисовывать
                hero.update(left, right, Up, platforms)  # передвижение
                typical_enemy_1.update()
                typical_enemy_2.update()
                typical_enemy_3.update(26)
                typical_enemy_4.update(35)
                entities.draw(screen)  # отображение

                date_time_obj3 = datetime.datetime.now()
                # .strftime("%M:%S")
                time_delta_2 = date_time_obj3 - date_time_obj1 - dt

                time_button = Button(RED, PLATFORM_WIDTH * 43, PLATFORM_HEIGHT / 2,
                                     0.000001,
                                     0.000001, f'{time_delta_2}')
                time_button.draw(screen, Color=WHITE, size=36)

                for e in level_exits:
                    if sprite.collide_rect(hero, e):
                        amount_passed_levels = 1
                        your_time = time_delta_2

                        timestr = f'{your_time}'
                        ftr = [3600, 60, 1, 10 ** (-6)]
                        your_time_seconds = sum([a * b for a, b in zip(ftr, map(float, timestr.split(':')))])
                        try:
                            if your_time_seconds < dict["your_time_seconds_1"]:
                                dict["your_time_seconds_1"] = your_time_seconds
                        except:
                            dict["your_time_seconds_1"] = your_time_seconds

                        dict["amount_passed_levels"] = 1
                        if landay:
                            is_landay = 1
                            dict["is_landay"] = 1
                        with open("saves.json", 'w') as f:
                            json.dump(dict, f)

                        menu_music = False
                        is_pass_level_screen = True
                        while is_pass_level_screen:
                            pass_level_screen(bg, screen, your_time)
                        run = False
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
            if switch_pause:
                date_time_obj4 = datetime.datetime.now()
                switch_pause = False
            while running_1 == 2:
                pause_menu(bg, screen)
        elif running_1 == 0:
            run = False

    return is_game_over, running_1, is_landay, is_menu, menu_music, Number_of_level, amount_passed_levels, \
           switch_pause, is_pass_level_screen


def level_2(bg, screen):
    """

    :param bg:
    :param screen:
    :return:
    """
    global is_game_over, running_2, is_menu, is_einstein, menu_music, Number_of_level, dict, switch_pause, \
        date_time_obj4, dt, is_pass_level_screen
    Number_of_level = 2

    pygame.mixer.music.set_volume(dict["music_volume"])
    pygame.mixer.music.load("Music/Office_Passenger_Dirty_Love.mp3")
    pygame.mixer.music.play(-1)

    typical_enemy_1 = Enemy(PLATFORM_WIDTH * 5, PLATFORM_HEIGHT * 23, 3)
    typical_enemy_2 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 8, PLATFORM_HEIGHT * 3, 2)
    typical_enemy_3 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 13, PLATFORM_HEIGHT * 3)
    typical_enemy_4 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 18, PLATFORM_HEIGHT * 3, 2)
    typical_enemy_5 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 22, PLATFORM_HEIGHT * 3)
    typical_enemy_6 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 27, PLATFORM_HEIGHT * 3, 4)
    typical_enemy_7 = Enemy(PLATFORM_WIDTH * 30.5, PLATFORM_HEIGHT * 22)
    archer_enemy_1 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 12, PLATFORM_HEIGHT * 5, enemy_image="enemy_2")
    archer_enemy_2 = Enemy(PLATFORM_WIDTH * 9, PLATFORM_HEIGHT * 7, enemy_image="enemy_2")
    archer_enemy_3 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 17, PLATFORM_HEIGHT * 7, enemy_image="enemy_2_straight")
    archer_enemy_4 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 17, PLATFORM_HEIGHT * 11, enemy_image="enemy_2")
    archer_enemy_5 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 9, enemy_image="enemy_2_90")

    hero = Player(PLATFORM_WIDTH, WIN_HEIGHT - PLATFORM_HEIGHT * 7)  # создаем героя по (x,y) координатам
    # hero = Player(WIN_WIDTH - PLATFORM_WIDTH*18, WIN_HEIGHT - PLATFORM_HEIGHT * 9)  # создаем героя по
    # (x,y) координатам
    left = right = False  # по умолчанию — стоим
    Up = False

    einstein = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    passes_in_level = []
    level_exits = []
    enemies = []
    bullets_1 = []
    bullets_2 = []
    bullets_3 = []
    bullets_4 = []
    bullets_5 = []
    lavas = []
    gallery_features = []

    date_time_obj1 = datetime.datetime.now()

    entities.add(hero)
    entities.add(typical_enemy_1, typical_enemy_2, typical_enemy_3, typical_enemy_4, typical_enemy_5, typical_enemy_6,
                 typical_enemy_7, archer_enemy_1, archer_enemy_2, archer_enemy_3, archer_enemy_4, archer_enemy_5)
    enemies.append(typical_enemy_1)
    enemies.append(typical_enemy_2)
    enemies.append(typical_enemy_3)
    enemies.append(typical_enemy_4)
    enemies.append(typical_enemy_5)
    enemies.append(typical_enemy_6)
    enemies.append(typical_enemy_7)
    enemies.append(archer_enemy_1)
    enemies.append(archer_enemy_2)
    enemies.append(archer_enemy_3)
    enemies.append(archer_enemy_4)
    enemies.append(archer_enemy_5)

    switch = True
    part_1 = True
    part_2 = False

    run = True
    while run:
        timer.tick(FPS)
        if switch:
            if part_1:
                level = Level_1.lvl_1
                x = y = 0  # координаты
                for row in level:  # вся строка
                    for col in row:  # каждый символ
                        if col == "-":
                            # создаем блок, заливаем его цветом и рисуем его
                            pf = Platform(x, y)
                            entities.add(pf)
                            platforms.append(pf)
                        if col == "=":
                            # создаем блок, заливаем его цветом и рисуем его
                            pfo = Platform(x, y + PLATFORM_HEIGHT / 10, "platform")
                            entities.add(pfo)
                            platforms.append(pfo)
                        if col == "/":
                            level_exit = Platform(x, y, "exit_door_180")
                            entities.add(level_exit)
                            level_exits.append(level_exit)
                        if col == "p":
                            pass_in_level = Platform(x, y, "pass_2")
                            entities.add(pass_in_level)
                            passes_in_level.append(pass_in_level)
                        if col == "*":
                            level_exit = Platform(x, y, "exit_door_2")
                            entities.add(level_exit)
                            level_exits.append(level_exit)
                        if col == "_":
                            lava = Platform(x, y, "lava_erase")
                            entities.add(lava)
                            lavas.append(lava)
                        if not is_einstein:
                            if col == "c":
                                gallery_einstein = "gallery_einstein"
                                gallery_feature = Platform(x, y, gallery_einstein)
                                entities.add(gallery_feature)
                                gallery_features.append(gallery_feature)

                        x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
                    y += PLATFORM_HEIGHT  # то же самое и с высотой
                    x = 0
                switch = False
            if part_2:
                hero.startX = PLATFORM_WIDTH * 2
                hero.startY = PLATFORM_HEIGHT * 2
                level = Level_1.lvl_2
                x = y = 0  # координаты
                for row in level:  # вся строка
                    for col in row:  # каждый символ
                        if col == "-":
                            # создаем блок, заливаем его цветом и рисуем его
                            pf = Platform(x, y)
                            entities.add(pf)
                            platforms.append(pf)
                        if col == "/":
                            level_exit = Platform(x, y, "exit_door_180")
                            entities.add(level_exit)
                            level_exits.append(level_exit)
                        if col == "p":
                            pass_in_level = Platform(x, y, "pass_2")
                            entities.add(pass_in_level)
                        if col == "*":
                            level_exit = Platform(x, y, "exit_door_2")
                            entities.add(level_exit)
                            level_exits.append(level_exit)
                        if col == "_":
                            lava = Platform(x, y, "lava_erase")
                            entities.add(lava)
                            lavas.append(lava)
                        if not is_einstein:
                            if col == "c":
                                gallery_einstein = "gallery_einstein"
                                gallery_feature = Platform(x, y, gallery_einstein)
                                entities.add(gallery_feature)
                                gallery_features.append(gallery_feature)

                        x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
                    y += PLATFORM_HEIGHT  # то же самое и с высотой
                    x = 0
                switch = False
        if running_2 == 1:
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
                    switch_pause = True
                    running_2 = 2

            hero.collide_enemy(enemies, hero)
            if hero.health > 0:

                screen.blit(bg, (0, 0))  # Каждую итерацию движения перса необходимо всё перерисовывать
                hero.update(left, right, Up, platforms)  # передвижение
                typical_enemy_1.update(move_counter=25)
                typical_enemy_2.update(move_counter=15)
                typical_enemy_3.update(move_counter=16)
                typical_enemy_4.update(move_counter=16)
                typical_enemy_5.update(move_counter=18)
                typical_enemy_6.update(move_counter=12)
                typical_enemy_7.update(move_counter=20)

                date_time_obj2 = datetime.datetime.now()
                time_delta = date_time_obj2 - date_time_obj1
                seconds = time_delta.total_seconds()

                if ((seconds + 1) // 1) % 3 == 0 and len(bullets_1) == 0:
                    bullet_1 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 12, PLATFORM_HEIGHT * 5, 10, "bomb_erase")
                    bullets_1.append(bullet_1)
                    enemies.append(bullet_1)
                    entities.add(bullet_1)

                    centerX_hero, centerY_hero = hero.rect.center
                    centerX_bullet_1, centerY_bullet_1 = bullet_1.rect.center
                    dx_1 = centerX_hero - centerX_bullet_1
                    dy_1 = centerY_hero - centerY_bullet_1
                    c_1 = (dx_1 ** 2 + dy_1 ** 2) ** 0.5

                if len(bullets_1) > 0:
                    if c_1 > 500 and len(bullets_1) != 0:
                        enemies.remove(bullet_1)
                        entities.remove(bullet_1)
                        bullets_1.remove(bullet_1)
                    if bullet_1.rect.x < WIN_WIDTH or bullet_1.rect.x > 0 or bullet_1.rect.y < WIN_HEIGHT \
                            or bullet_1.rect.y > 0:
                        bullet_1.update(enemy_image="bomb", a=dx_1, b=dy_1, C=c_1)
                    if bullet_1.rect.x >= WIN_WIDTH or bullet_1.rect.x <= 0 or bullet_1.rect.y >= WIN_HEIGHT \
                            or bullet_1.rect.y <= 0:
                        enemies.remove(bullet_1)
                        entities.remove(bullet_1)
                        bullets_1.remove(bullet_1)

                if ((seconds + 1) // 1) % 3 == 0 and len(bullets_2) == 0:
                    bullet_2 = Enemy(PLATFORM_WIDTH * 9, PLATFORM_HEIGHT * 7, 10, "bomb_erase")
                    bullets_2.append(bullet_2)
                    enemies.append(bullet_2)
                    entities.add(bullet_2)

                    centerX_hero, centerY_hero = hero.rect.center
                    centerX_bullet_2, centerY_bullet_2 = bullet_2.rect.center

                    dx_2 = centerX_hero - centerX_bullet_2
                    dy_2 = centerY_hero - centerY_bullet_2
                    c_2 = (dx_2 ** 2 + dy_2 ** 2) ** 0.5

                if len(bullets_2) > 0:
                    if c_2 > 500 and len(bullets_2) != 0:
                        enemies.remove(bullet_2)
                        entities.remove(bullet_2)
                        bullets_2.remove(bullet_2)
                    if bullet_2.rect.x < WIN_WIDTH or bullet_2.rect.x > 0 or bullet_2.rect.y < WIN_HEIGHT \
                            or bullet_2.rect.y > 0:
                        bullet_2.update(enemy_image="bomb", a=dx_2, b=dy_2, C=c_2)
                    if bullet_2.rect.x >= WIN_WIDTH or bullet_2.rect.x <= 0 or bullet_2.rect.y >= WIN_HEIGHT \
                            or bullet_2.rect.y <= 0:
                        enemies.remove(bullet_2)
                        entities.remove(bullet_2)
                        bullets_2.remove(bullet_2)

                if ((seconds + 1) // 1) % 3 == 0 and len(bullets_3) == 0:
                    bullet_3 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 17, PLATFORM_HEIGHT * 7, 5, "bomb_mini")
                    bullets_3.append(bullet_3)
                    enemies.append(bullet_3)
                    entities.add(bullet_3)

                    centerX_hero, centerY_hero = hero.rect.center
                    centerX_bullet_3, centerY_bullet_3 = bullet_3.rect.center
                    dx_3 = centerX_hero - centerX_bullet_3
                    dy_3 = centerY_hero - centerY_bullet_3
                    c_3 = (dx_3 ** 2 + dy_3 ** 2) ** 0.5

                if len(bullets_3) > 0:
                    if c_3 > PLATFORM_HEIGHT * 4 and len(bullets_3) != 0:
                        enemies.remove(bullet_3)
                        entities.remove(bullet_3)
                        bullets_3.remove(bullet_3)
                    if bullet_3.rect.x < WIN_WIDTH or bullet_3.rect.x > 0 or bullet_3.rect.y < WIN_HEIGHT \
                            or bullet_3.rect.y > 0:
                        bullet_3.update(enemy_image="bomb_mini", a=dx_3, b=dy_3, C=c_3)
                    if bullet_3.rect.x >= WIN_WIDTH or bullet_3.rect.x <= 0 or bullet_3.rect.y >= WIN_HEIGHT \
                            or bullet_3.rect.y <= 0:
                        enemies.remove(bullet_3)
                        entities.remove(bullet_3)
                        bullets_3.remove(bullet_3)

                if ((seconds + 1) // 1) % 3 == 0 and len(bullets_4) == 0:
                    bullet_4 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 17, PLATFORM_HEIGHT * 11, 5, "bomb_mini")
                    bullets_4.append(bullet_4)
                    enemies.append(bullet_4)
                    entities.add(bullet_4)

                    centerX_hero, centerY_hero = hero.rect.center
                    centerX_bullet_4, centerY_bullet_4 = bullet_4.rect.center
                    dx_4 = centerX_hero - centerX_bullet_4
                    dy_4 = centerY_hero - centerY_bullet_4
                    c_4 = (dx_4 ** 2 + dy_4 ** 2) ** 0.5

                if len(bullets_4) > 0:
                    if c_4 > PLATFORM_HEIGHT * 4 and len(bullets_4) != 0:
                        enemies.remove(bullet_4)
                        entities.remove(bullet_4)
                        bullets_4.remove(bullet_4)
                    if bullet_4.rect.x < WIN_WIDTH or bullet_4.rect.x > 0 or bullet_4.rect.y < WIN_HEIGHT \
                            or bullet_4.rect.y > 0:
                        bullet_4.update(enemy_image="bomb_mini", a=dx_4, b=dy_4, C=c_4)
                    if bullet_4.rect.x >= WIN_WIDTH or bullet_4.rect.x <= 0 or bullet_4.rect.y >= WIN_HEIGHT \
                            or bullet_4.rect.y <= 0:
                        enemies.remove(bullet_4)
                        entities.remove(bullet_4)
                        bullets_4.remove(bullet_4)

                if ((seconds + 1) // 1) % 3 == 0 and len(bullets_5) == 0:
                    bullet_5 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 9, 5, "bomb_mini")
                    bullets_5.append(bullet_5)
                    enemies.append(bullet_5)
                    entities.add(bullet_5)

                    centerX_hero, centerY_hero = hero.rect.center
                    centerX_bullet_5, centerY_bullet_5 = bullet_5.rect.center
                    dx_5 = centerX_hero - centerX_bullet_5
                    dy_5 = centerY_hero - centerY_bullet_5
                    c_5 = (dx_5 ** 2 + dy_5 ** 2) ** 0.5

                if len(bullets_5) > 0:
                    if c_5 > PLATFORM_HEIGHT * 4 and len(bullets_5) != 0:
                        enemies.remove(bullet_5)
                        entities.remove(bullet_5)
                        bullets_5.remove(bullet_5)
                    if bullet_5.rect.x < WIN_WIDTH or bullet_5.rect.x > 0 or bullet_5.rect.y < WIN_HEIGHT \
                            or bullet_5.rect.y > 0:
                        bullet_5.update(enemy_image="bomb_mini", a=dx_5, b=dy_5, C=c_5)
                    if bullet_5.rect.x >= WIN_WIDTH or bullet_5.rect.x <= 0 or bullet_5.rect.y >= WIN_HEIGHT \
                            or bullet_5.rect.y <= 0:
                        enemies.remove(bullet_5)
                        entities.remove(bullet_5)
                        bullets_5.remove(bullet_5)

                entities.draw(screen)  # отображение

                date_time_obj3 = datetime.datetime.now()
                # .strftime("%M:%S")
                time_delta_2 = date_time_obj3 - date_time_obj1 - dt

                time_button = Button(RED, PLATFORM_WIDTH * 43, PLATFORM_HEIGHT / 2,
                                     0.000001,
                                     0.000001, f'{time_delta_2}')
                time_button.draw(screen, Color=WHITE, size=36)

                for e in level_exits:
                    if sprite.collide_rect(hero, e):

                        your_time = time_delta_2
                        timestr = f'{your_time}'
                        ftr = [3600, 60, 1, 10 ** (-6)]
                        your_time_seconds = sum([a * b for a, b in zip(ftr, map(float, timestr.split(':')))])
                        try:
                            if your_time_seconds < dict["your_time_seconds_2"]:
                                dict["your_time_seconds_2"] = your_time_seconds
                        except:
                            dict["your_time_seconds_2"] = your_time_seconds

                        if einstein:
                            is_einstein = 1
                            dict["is_einstein"] = 1
                            with open("saves.json", 'w') as f:
                                json.dump(dict, f)

                        menu_music = False
                        is_pass_level_screen = True
                        while is_pass_level_screen:
                            pass_level_screen(bg, screen, your_time)
                        run = False
                for g in gallery_features:
                    if sprite.collide_rect(hero, g):
                        entities.remove(gallery_feature)
                        einstein = True
                # for pa in passes_in_level:
                #     if sprite.collide_rect(hero, pa):
                #         part_1 = False
                #         part_2 = True
                #         switch = True
                for l in lavas:
                    if sprite.collide_rect(hero, l):
                        hero.health = 0
            elif hero.health <= 0:
                is_game_over = True
                run = False
                running_2 = 0
                game_over(bg, screen)
            pygame.display.update()  # обновление и вывод всех изменений на экран
        elif running_2 == 2:
            if switch_pause:
                date_time_obj4 = datetime.datetime.now()
                switch_pause = False
            while running_2 == 2:
                pause_menu(bg, screen)
        elif running_2 == 0:
            run = False

    return is_game_over, running_2, is_einstein, is_menu, menu_music, switch_pause, dt


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    screen = pygame.display.set_mode(DISPLAY)
    # screen = pygame.display.set_mode(DISPLAY, pygame.DOUBLEBUF | pygame.OpenGL)  # Создаем окошко
    pygame.display.set_caption("SUPER FOPF BOY")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности, будем использовать как фон
    # glClearColor(BACKGROUND_COLOR/255, 1)

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
        elif running_2 != 0:
            while running_2:
                level_2(bg, screen)
        elif is_game_over:
            while is_game_over:
                game_over(bg, screen)
        elif is_restart:
            restart()
        elif is_achievements_menu:
            while is_achievements_menu:
                achievements_menu(bg, screen)
        else:
            runnin = False


if __name__ == "__main__":
    main()
