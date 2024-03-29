#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import pygame.mixer
import Level_2
from Enemy import *
from textures import *
from buttones import *
import datetime
import ctypes
import json
import ctypes
import os
import pyganim

COLOR = "#888888"
user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55
PLATFORM_WIDTH = WIN_WIDTH / 48
PLATFORM_HEIGHT = WIN_HEIGHT / 25.25
WIDTH = PLATFORM_WIDTH
HEIGHT = PLATFORM_HEIGHT
GRAVITY = PLATFORM_HEIGHT * 0.013
JUMP_POWER = PLATFORM_HEIGHT / 3.4
MOVE_SPEED = PLATFORM_WIDTH / 9.2
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
ANIMATION_DELAY = 0.1  # скорость смены кадров
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами
up = False
god_mode = 0
#Массивы с спрайтами
ANIMATION_RIGHT = [('%s/FOPF/r1.png' % ICON_DIR),
                   ('%s/FOPF/r2.png' % ICON_DIR),
                   ('%s/FOPF/r3.png' % ICON_DIR),
                   ('%s/FOPF/r4.png' % ICON_DIR),
                   ('%s/FOPF/r5.png' % ICON_DIR)]
ANIMATION_LEFT = [('%s/FOPF/l1.png' % ICON_DIR),
                  ('%s/FOPF/l2.png' % ICON_DIR),
                  ('%s/FOPF/l3.png' % ICON_DIR),
                  ('%s/FOPF/l4.png' % ICON_DIR),
                  ('%s/FOPF/l5.png' % ICON_DIR)]
ANIMATION_JUMP_LEFT = [('%s/FOPF/jl.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP_RIGHT = [('%s/FOPF/jr.png' % ICON_DIR, 0.1)]
ANIMATION_JUMP = [('%s/FOPF/j.png' % ICON_DIR, 0.1)]
ANIMATION_STAY = [('%s/FOPF/0.png' % ICON_DIR, 0.1)]
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


k = 100
with open("saves.json", 'r') as f:
    dict = json.load(f)
music_volume = dict["music_volume"]
Number_of_level = 0
gallery_pictures = []
amount_passed_levels = dict["amount_passed_levels"]
is_landay = dict["is_landay"]
is_einstein = dict["is_einstein"]
is_karasev = dict["is_karasev"]
is_red_key = dict["is_red_key"]


#снова что-то нужное для прогресса
try:
    if dict["your_time_seconds_1"] <= 12.5:
        is_1 = 1
    else:
        is_1 = 0
except KeyError:
    is_1 = 0
try:
    if dict["your_time_seconds_2"] <= 60:
        is_2 = 1
    else:
        is_2 = 0
except KeyError:
    is_2 = 0
try:
    if dict["your_time_seconds_3"] <= 180:
        is_3 = 1
    else:
        is_3 = 0
except KeyError:
    is_3 = 0
progress = (dict["is_einstein"] + dict["is_landay"] + dict["is_karasev"] + dict["is_red_key"] + dict["is_yellow_key"]
            + dict["amount_passed_levels"] + is_1 + is_2 + is_3) * 100 // 11
#маркеры для менюшек
gallery_pictures.append(is_landay)
is_menu = False
is_options_menu = False
is_gallery_menu = False
menu_music = False
is_levels = False
is_game_over = False
is_pass_level_screen = False
is_hiryanov_menu = False
running_1 = 0
running_2 = 0
running_3_1 = 0
running_3_2 = 0
is_pause_menu = False
switch_pause = False
is_restart = False
is_achievements_menu = False

up = False
timer = pygame.time.Clock()
class Player(sprite.Sprite):
    def __init__(self, x, y, HEALTH = k , invisible_time=0):
        sprite.Sprite.__init__(self)
        self.x_vel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.y_vel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.health = HEALTH #здоровье
        self.invisible_time = invisible_time
        self.image.set_colorkey(Color(COLOR))  # делаем фон прозрачным
        # Анимация движения вправо
        boltAnim = []
        for anim in ANIMATION_RIGHT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimRight = pyganim.PygAnimation(boltAnim)
        self.boltAnimRight.play()
        #  Анимация движения влево
        boltAnim = []
        for anim in ANIMATION_LEFT:
            boltAnim.append((anim, ANIMATION_DELAY))
        self.boltAnimLeft = pyganim.PygAnimation(boltAnim)
        self.boltAnimLeft.play()

        self.boltAnimStay = pyganim.PygAnimation(ANIMATION_STAY)
        self.boltAnimStay.play()
        self.boltAnimStay.blit(self.image, (0, 0))  # По-умолчанию, стоим

        self.boltAnimJumpLeft = pyganim.PygAnimation(ANIMATION_JUMP_LEFT)
        self.boltAnimJumpLeft.play()

        self.boltAnimJumpRight = pyganim.PygAnimation(ANIMATION_JUMP_RIGHT)
        self.boltAnimJumpRight.play()

        self.boltAnimJump = pyganim.PygAnimation(ANIMATION_JUMP)
        self.boltAnimJump.play()

    def update(self, left, right, Up, platforms):
        if Up:
            if self.onGround or god_mode == 1:  # прыгаем, только когда можем оттолкнуться от земли или включен особый режим
                self.y_vel = -JUMP_POWER
                # jump_sound.play()
            self.image.fill(Color(COLOR))
            self.boltAnimJump.blit(self.image, (0, 0))
        if left:
            self.x_vel = -MOVE_SPEED  # Лево
            self.image.fill(Color(COLOR))
            if Up:  # для прыжка влево есть отдельная анимация
                self.boltAnimJumpLeft.blit(self.image, (0, 0))
            else:
                self.boltAnimLeft.blit(self.image, (0, 0))
        if right:
            self.x_vel = MOVE_SPEED  # Право
            self.x_vel = MOVE_SPEED  # Право = x + n
            self.image.fill(Color(COLOR))
            if Up:  #анимация для прыжка в право
                self.boltAnimJumpRight.blit(self.image, (0, 0))
            else:
                self.boltAnimRight.blit(self.image, (0, 0))

        if not (left or right):  # стоим, когда нет указаний идти
            self.x_vel = 0
            if not Up:
                self.image.fill(Color(COLOR))
                self.boltAnimStay.blit(self.image, (0, 0))
        if not self.onGround:
            self.y_vel += GRAVITY
        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.y_vel
        self.collide(0, self.y_vel, platforms)

        self.rect.x += self.x_vel  # переносим свои положение на xvel
        self.collide(self.x_vel, 0, platforms)

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:  # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:  # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True  # и становится на что-то твердое
                    self.y_vel = 0  # и энергия падения пропадает

                if yvel < 0:  # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.y_vel = 0  # и энергия прыжка пропадает
    
    def collide_enemy(self, enemies, hero):#коллизия с врагом
        for en in enemies:
            if sprite.collide_rect(self, en):
                hero.health -= 100 # может привести к смерти

def menu(bg, screen):
    """

    :param bg: background of game window
    :param screen: general screen of window
    :return:
    """
    global god_mode, running_1, is_menu, is_levels, menu_music, is_gallery_menu, is_options_menu, dict, is_achievements_menu, k, running_2, running_3_1, is_landay,is_einstein, is_karasev  
    running_2, running_3_1, is_landay,is_einstein, is_karasev  
    music_volume = dict["music_volume"]
    Number_of_level = 0
    gallery_pictures = []
    #штуки для прогресса
    amount_passed_levels = dict["amount_passed_levels"]
    is_landay = dict["is_landay"]
    is_einstein = dict["is_einstein"]
    is_karasev = dict["is_karasev"]
    is_red_key = dict["is_red_key"]
    god_mode = dict["god_mode"]
    k = 100 + god_mode * 10000000
    if not menu_music:
        pygame.mixer.music.set_volume(dict["music_volume"])
        pygame.mixer.music.load("Music/menu_music.mp3")
        pygame.mixer.music.play(-1)
    
    screen.fill(Color(GREEN))
    #сохранение
    with open("saves.json", 'r') as f:
        dict = json.load(f)
    #рисовалка кнопок
    start_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 3, WIN_WIDTH / 3.2,
                          PLATFORM_HEIGHT * 2, 'Start/Continue')
    start_button.draw(screen)

    levels_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 7, WIN_WIDTH / 3.2,
                           PLATFORM_HEIGHT * 2, 'Levels')
    levels_button.draw(screen)

    options_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 11, WIN_WIDTH / 3.2,
                            PLATFORM_HEIGHT * 2, 'Options')
    options_button.draw(screen)

    gallery_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 15, WIN_WIDTH / 3.2,
                            PLATFORM_HEIGHT * 2, 'Gallery')
    gallery_button.draw(screen)

    achievements_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 19,
                                 WIN_WIDTH / 3.2, PLATFORM_HEIGHT * 2, 'Achievements')
    achievements_button.draw(screen)

    quit_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 22.5, WIN_WIDTH / 3.2,
                         PLATFORM_HEIGHT * 2, 'Quit')
    quit_button.draw(screen)

    progress_button = Button(RED, WIN_WIDTH / 2, PLATFORM_HEIGHT * 1, 0.00000001, 0.00000001,
                             f'Progress: {progress} %')
    progress_button.draw(screen)

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
                    if amount_passed_levels == 0:
                        running_1 = True
                    if amount_passed_levels == 1:
                        running_2 = True
                    if amount_passed_levels >= 2:
                        running_3_1 = True
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
    global is_menu, running_1, running_2, running_3_1, is_levels, amount_passed_levels

    bg = pygame.image.load("Textures/additional task.png")
    # screen.blit(bg, (0, 0))
    screen.fill(Color(GREEN))

    level_1_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 4, WIN_WIDTH / 3.2,
                            WIN_HEIGHT / 15, 'Level 1')
    level_1_button.draw(screen)
    #Рисовалка кнопок
    if amount_passed_levels < 1:
        level_2_button = Button(GREY, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 8,
                                WIN_WIDTH / 3.2,
                                WIN_HEIGHT / 15, 'Level 2')

        cannot_button = Button(GREY, WIN_WIDTH / 2, WIN_HEIGHT / 2 - WIN_HEIGHT / 29, 0.1, 0.1,
                               'Firstly, pass all previous levels')
    else:
        level_2_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 8,
                                WIN_WIDTH / 3.2,
                                WIN_HEIGHT / 15, 'Level 2')
    level_2_button.draw(screen)

    if amount_passed_levels < 2:
        level_3_button = Button(GREY, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 12,
                                WIN_WIDTH / 3.2,
                                WIN_HEIGHT / 15, 'Level 3')

        cannot_button = Button(GREY, WIN_WIDTH / 2, WIN_HEIGHT / 2 - WIN_HEIGHT / 29, 0.1, 0.1,
                               'Firstly, pass all previous levels')
    else:
        level_3_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, PLATFORM_HEIGHT * 12,
                                WIN_WIDTH / 3.2,
                                WIN_HEIGHT / 15, 'Level 3')
    level_3_button.draw(screen)

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
                if level_3_button.is_pressed(mouse_pos, mouse_pressed):
                    if amount_passed_levels < 2:
                        cannot_button.draw(screen, RED)
                        pygame.display.update()
                    else:
                        running_3_1 = True
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

    if not is_karasev:
        picture_2_image = pygame.image.load("Textures/invisible_person.png")
        picture_2_image_rect = picture_2_image.get_rect(center=(800, 150))
        screen.blit(picture_2_image, picture_2_image_rect)
    else:
        picture_2_image = pygame.image.load("Textures/karasev_gallery_feature.png")
        picture_2_image_rect = picture_2_image.get_rect(center=(800, 150))
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
    global is_menu, menu_music, is_options_menu, is_landay, dict, amount_passed_levels, is_karasev, is_einstein, \
        is_red_key, is_yellow_key, god_mode

    screen.fill(Color(GREEN))

    back_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 1.2 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                         WIN_HEIGHT / 15, 'Back')
    back_button.draw(screen)

    god_mode_button = Button(RED, WIN_WIDTH / 2 - WIN_WIDTH / 6.2, WIN_HEIGHT / 3 - WIN_HEIGHT / 27, WIN_WIDTH / 3.2,
                         WIN_HEIGHT / 15, 'God mode')
    god_mode_button.draw(screen)

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
                if god_mode_button.is_pressed(mouse_pos, mouse_pressed):
                    dict["is_yellow_key"] = 1
                    dict["is_red_key"] = 1
                    dict["amount_passed_levels"] = 3
                    dict["is_landay"] = 1
                    dict["is_einstein"] = 1
                    dict["is_karasev"] = 1
                    dict["your_time_seconds_1"] = 12.5
                    dict["your_time_seconds_2"] = 60
                    dict["your_time_seconds_3"] = 300
                    dict["progress"] = 100
                    dict["god_mode"] = 1
                    god_mode = dict["god_mode"]
                    print(god_mode)
                    with open("saves.json", 'w') as foo:
                        json.dump(dict, foo)
                    with open("saves.json", 'r') as foo:
                        dict = json.load(foo)
                if music_off_button.is_pressed(mouse_pos, mouse_pressed):
                    pygame.mixer.music.set_volume(0)
                    dict["music_volume"] = 0
                    with open("saves.json", 'w') as foo:
                        json.dump(dict, foo)
                    with open("saves.json", 'r') as foo:
                        dict = json.load(foo)
                if music_on_button.is_pressed(mouse_pos, mouse_pressed):
                    pygame.mixer.music.set_volume(1)
                    dict["music_volume"] = 1
                    with open("saves.json", 'w') as foo:
                        json.dump(dict, foo)
                    with open("saves.json", 'r') as foo:
                        dict = json.load(foo)
                if reset_progress_button.is_pressed(mouse_pos, mouse_pressed):
                    amount_passed_levels = 0
                    is_1 = 0
                    is_2 = 0
                    is_3 = 0
                    is_landay = 0
                    is_einstein = 0
                    is_karasev = 0
                    is_red_key = 0
                    is_yellow_key = 0
                    dict["god_mode"] = 0
                    god_mode = dict["god_mode"]
                    print(god_mode)
                    dict["is_yellow_key"] = 0
                    dict["is_red_key"] = 0
                    dict["amount_passed_levels"] = 0
                    dict["is_landay"] = 0
                    dict["is_einstein"] = 0
                    dict["is_karasev"] = 0
                    dict["progress"] = 0
                    dict["progress"] = 0
                    #5del dict["your_time_seconds_1"]
                    #del dict["your_time_seconds_2"]
                    #del dict["your_time_seconds_3"]
                    with open("saves.json", 'w') as foo:
                        json.dump(dict, foo)
                    with open("saves.json", 'r') as foo:
                        dict = json.load(foo)

        pygame.display.update()
        return is_options_menu, is_menu, menu_music, is_landay, amount_passed_levels


def achievements_menu(bg, screen):
    global is_menu, menu_music, is_achievements_menu, dict, is_red_key, your_time_sec_1

    screen.fill(Color(GREEN))

    level_1_name = Button(GREEN, PLATFORM_WIDTH * 5, PLATFORM_HEIGHT * 3, PLATFORM_WIDTH,
                          PLATFORM_HEIGHT, 'level 1')
    level_2_name = Button(GREEN, PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 3, PLATFORM_WIDTH,
                          PLATFORM_HEIGHT, 'level 2')
    level_3_name = Button(GREEN, PLATFORM_WIDTH * 25, PLATFORM_HEIGHT * 3, PLATFORM_WIDTH,
                          PLATFORM_HEIGHT, 'level 3')

    try:
        level_1_record = Button(GREEN, PLATFORM_WIDTH * 5, PLATFORM_HEIGHT * 5, PLATFORM_WIDTH,
                                PLATFORM_HEIGHT, f'{dict["your_time_seconds_1"]}')
    except KeyError:
        level_1_record = Button(GREEN, PLATFORM_WIDTH * 5, PLATFORM_HEIGHT * 5, PLATFORM_WIDTH,
                                PLATFORM_HEIGHT, "Empty -_-")
    try:
        level_2_record = Button(GREEN, PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 5, PLATFORM_WIDTH,
                                PLATFORM_HEIGHT, f'{dict["your_time_seconds_2"]}')
    except KeyError:
        level_2_record = Button(GREEN, PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 5, PLATFORM_WIDTH,
                                PLATFORM_HEIGHT, "Empty -_-")

    try:
        level_3_record = Button(GREEN, PLATFORM_WIDTH * 25, PLATFORM_HEIGHT * 5, PLATFORM_WIDTH,
                                PLATFORM_HEIGHT, f'{dict["your_time_seconds_3"]}')
    except KeyError:
        level_3_record = Button(GREEN, PLATFORM_WIDTH * 25, PLATFORM_HEIGHT * 5, PLATFORM_WIDTH,
                                PLATFORM_HEIGHT, "Empty -_-")

    level_1_name.draw(screen, Color=WHITE)
    level_2_name.draw(screen, Color=WHITE)
    level_3_name.draw(screen, Color=WHITE)
    try:
        if dict["your_time_seconds_1"] <= 12.5:
            level_1_record.draw(screen, Color=WHITE)
        else:
            level_1_record.draw(screen, Color=RED)
    except KeyError:
        level_1_record.draw(screen, Color=WHITE)
    try:
        if dict["your_time_seconds_2"] <= 60:
            level_2_record.draw(screen, Color=WHITE)
        else:
            level_2_record.draw(screen, Color=RED)
    except KeyError:
        level_2_record.draw(screen, Color=WHITE)

    try:
        if dict["your_time_seconds_2"] <= 180:
            level_3_record.draw(screen, Color=WHITE)
        else:
            level_3_record.draw(screen, Color=RED)
    except KeyError:
        level_3_record.draw(screen, Color=WHITE)

    if dict["is_red_key"] == 0:
        picture_1_image = pygame.image.load("Textures/hud_keyRed_disabled.png")
        picture_1_image_rect = picture_1_image.get_rect(center=(PLATFORM_WIDTH * 6, PLATFORM_HEIGHT * 8))
        screen.blit(picture_1_image, picture_1_image_rect)
    else:
        picture_1_image = pygame.image.load("Textures/hud_keyRed.png")
        picture_1_image_rect = picture_1_image.get_rect(center=(PLATFORM_WIDTH * 6, PLATFORM_HEIGHT * 8))
        screen.blit(picture_1_image, picture_1_image_rect)

    if dict["is_yellow_key"] == 0:
        picture_1_image = pygame.image.load("Textures/hud_keyYellow_disabled.png")
        picture_1_image_rect = picture_1_image.get_rect(center=(PLATFORM_WIDTH * 6, PLATFORM_HEIGHT * 20))
        screen.blit(picture_1_image, picture_1_image_rect)
    else:
        picture_1_image = pygame.image.load("Textures/hud_keyYellow.png")
        picture_1_image_rect = picture_1_image.get_rect(center=(PLATFORM_WIDTH * 6, PLATFORM_HEIGHT * 20))
        screen.blit(picture_1_image, picture_1_image_rect)

    describe_yellow_key_left = Button(RED, PLATFORM_WIDTH * 4, PLATFORM_HEIGHT * 20, 0.00001,
                                      0.00001, 'The')
    describe_yellow_key_left.draw(screen, size=36, Color=WHITE)

    describe_yellow_key = Button(RED, PLATFORM_WIDTH * 13, PLATFORM_HEIGHT * 20, 0.00001,
                                 0.00001, 'open your second breath')
    describe_yellow_key.draw(screen, size=36, Color=WHITE)

    back_button = Button(RED, PLATFORM_WIDTH * 3, PLATFORM_HEIGHT * 22, PLATFORM_WIDTH * 4,
                         PLATFORM_HEIGHT * 2, 'Back')
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
    global running_1, is_menu, Number_of_level, running_2, menu_music, switch_pause, dt, date_time_obj4, \
        is_pass_level_screen, is_restart, running_3_1, running_3_2
    pygame.mixer.music.pause()

    pause_bg = pygame.image.load("Textures/pause_bg.png")
    screen.blit(pause_bg, (PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 1))

    continue_button = Button(RED, PLATFORM_WIDTH * 20, WIN_HEIGHT / 6 - WIN_HEIGHT / 27, PLATFORM_WIDTH * 8,
                             PLATFORM_HEIGHT * 2, 'Continue')
    continue_button.draw(screen)

    menu_button = Button(RED, PLATFORM_WIDTH * 20, WIN_HEIGHT / 2, PLATFORM_WIDTH * 8,
                         PLATFORM_HEIGHT * 2, 'Menu')
    menu_button.draw(screen)

    restart_button = Button(RED, PLATFORM_WIDTH * 20, PLATFORM_HEIGHT * 8, PLATFORM_WIDTH * 8,
                            PLATFORM_HEIGHT * 2, 'Restart')
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
                if continue_button.is_pressed(mouse_pos, mouse_pressed):
                    if Number_of_level == 1:
                        running_1 = 1
                        dt += datetime.datetime.now() - date_time_obj4
                    elif Number_of_level == 2:
                        running_2 = 1
                        dt += datetime.datetime.now() - date_time_obj4
                    elif Number_of_level == 31:
                        running_3_1 = 1
                        dt += datetime.datetime.now() - date_time_obj4
                    elif Number_of_level == 32:
                        running_3_2 = 1
                        dt += datetime.datetime.now() - date_time_obj4
                    run = False
                if menu_button.is_pressed(mouse_pos, mouse_pressed):
                    dt = datetime.datetime.now() - datetime.datetime.now()
                    is_menu = True
                    running_1 = 0
                    running_2 = 0
                    running_3_1 = 0
                    running_3_2 = 0
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
                    if Number_of_level == 31 or Number_of_level == 32:
                        is_restart = True
                        is_pass_level_screen = False
                        running_3_1 = 0
                        running_3_2 = 0
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
    global is_menu, running_1, is_game_over, running_2, Number_of_level, dict, menu_music, dt, running_3_1, is_restart

    dt = datetime.datetime.now() - datetime.datetime.now()

    pygame.mixer.music.set_volume(dict["music_volume"])
    pygame.mixer.music.load('Music/game_over.mp3')
    pygame.mixer.music.play()
    screen.fill(Color(WHITE))

    if dict["is_yellow_key"] == 0:
        dict["health"] = 100
    elif dict["is_yellow_key"] == 1:
        dict["health"] = 200

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
            if even.type == KEYDOWN and even.key == K_r:
                is_menu = False
                if Number_of_level == 1:
                    running_1 = 1
                elif Number_of_level == 2:
                    running_2 = 1
                elif Number_of_level == 31 or Number_of_level == 32:
                    running_3_1 = 1
                is_game_over = False
                run = False
            if even.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                mouse_pressed = pygame.mouse.get_pressed()
                if restart_button.is_pressed(mouse_pos, mouse_pressed):
                    dt = datetime.datetime.now() - datetime.datetime.now()
                    is_restart = True
                    is_menu = False
                    # if Number_of_level == 1:
                    #     running_1 = 1
                    # elif Number_of_level == 2:
                    #     running_2 = 1
                    # elif Number_of_level == 31 or Number_of_level == 32:
                    #     running_3_2 = 0
                    #     running_3_1 = 1
                    is_game_over = False
                    run = False
                if menu_button.is_pressed(mouse_pos, mouse_pressed):
                    is_menu = True
                    menu_music = False
                    is_game_over = False
                    run = False
    pygame.display.update()
    return is_menu, running_1, is_game_over, menu_music, running_2, running_3_1, running_3_2


def restart():
    global running_1, running_2, is_restart, is_menu, Number_of_level, running_3_1
    is_menu = False
    if Number_of_level == 1:
        running_1 = 1
    elif Number_of_level == 2:
        running_2 = 1
    elif Number_of_level == 31 or Number_of_level == 32:
        running_3_1 = 1
    is_restart = False


def pass_level_screen(bg, screen, your_time, your_time_seconds):
    global running_1, is_menu, Number_of_level, running_2, menu_music, switch_pause, dt, \
        date_time_obj4, is_pass_level_screen, is_restart, running_3_1, running_3_2, is_hiryanov_menu

    pause_bg = pygame.image.load("Textures/maybe_pause_bg.png")
    screen.blit(pause_bg, (PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 1))

    next_level_button = Button(RED, PLATFORM_WIDTH * 20, WIN_HEIGHT / 6 - WIN_HEIGHT / 27,
                               PLATFORM_WIDTH * 8,
                               WIN_HEIGHT / 15, 'Next_level')
    next_level_button.draw(screen, size=48)
    if Number_of_level == 1:
        on_record_time_button = Button(RED, PLATFORM_WIDTH * 30.5, PLATFORM_HEIGHT * 13, 0.000001,
                                       0.000001, 'of 0:00:12:5')
        on_record_time_button.draw(screen, size=48, Color=WHITE)

        if your_time_seconds > 12.5:
            what_time_button = Button(RED, PLATFORM_WIDTH * 20.5, PLATFORM_HEIGHT * 13, 0.000001,
                                      0.000001, f'{your_time}')
            what_time_button.draw(screen, size=48, Color=RED)
        if your_time_seconds <= 12.5:
            what_time_button = Button(RED, PLATFORM_WIDTH * 20.5, PLATFORM_HEIGHT * 13, 0.000001,
                                      0.000001, f'{your_time}')
            what_time_button.draw(screen, size=48, Color=GREEN)
    if Number_of_level == 2:
        on_record_time_button = Button(RED, PLATFORM_WIDTH * 30.5, PLATFORM_HEIGHT * 13, 0.000001,
                                       0.000001, 'of 0:00:01:00')
        on_record_time_button.draw(screen, size=48, Color=WHITE)

        if your_time_seconds > 60:
            what_time_button = Button(RED, PLATFORM_WIDTH * 20.5, PLATFORM_HEIGHT * 13, 0.000001,
                                      0.000001, f'{your_time}')
            what_time_button.draw(screen, size=48, Color=RED)
        if your_time_seconds <= 60:
            what_time_button = Button(RED, PLATFORM_WIDTH * 20.5, PLATFORM_HEIGHT * 13, 0.000001,
                                      0.000001, f'{your_time}')
            what_time_button.draw(screen, size=48, Color=GREEN)

    if Number_of_level == 32:
        on_record_time_button = Button(RED, PLATFORM_WIDTH * 30.5, PLATFORM_HEIGHT * 13, 0.000001,
                                       0.000001, 'of 0:00:05:00')
        on_record_time_button.draw(screen, size=48, Color=WHITE)

        if your_time_seconds > 180:
            what_time_button = Button(RED, PLATFORM_WIDTH * 20.5, PLATFORM_HEIGHT * 13, 0.000001,
                                      0.000001, f'{your_time}')
            what_time_button.draw(screen, size=48, Color=RED)
        if your_time_seconds <= 180:
            what_time_button = Button(RED, PLATFORM_WIDTH * 20.5, PLATFORM_HEIGHT * 13, 0.000001,
                                      0.000001, f'{your_time}')
            what_time_button.draw(screen, size=48, Color=GREEN)

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
                    elif Number_of_level == 2:
                        running_2 = 0
                        is_pass_level_screen = False
                        running_3_1 = 1
                    elif Number_of_level == 32:
                        running_3_2 = 0
                        is_hiryanov_menu = True
                        is_pass_level_screen = False
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


"""def hiryanov_menu(bg, screen):
    global is_hiryanov_menu, is_menu, menu_music, dt, progress

    pause_bg = pygame.image.load("Textures/hiryanov.png")
    screen.blit(pause_bg, (PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 1))

    if progress == 100:
        next_level_button = Button(RED, PLATFORM_WIDTH * 20, WIN_HEIGHT / 6 - WIN_HEIGHT / 27,
                                   PLATFORM_WIDTH * 8,
                                   WIN_HEIGHT / 15, "You not complete all my problems. Back to beginning and do all!")
        next_level_button.draw(screen, size=48)
    if progress < 100:
        next_level_button = Button(RED, PLATFORM_WIDTH * 20, WIN_HEIGHT / 6 - WIN_HEIGHT / 27,
                                   PLATFORM_WIDTH * 8,
                                   WIN_HEIGHT / 15, "You complete all my problems. Unfortunately, I love recursion!!")
        next_level_button.draw(screen, size=48)

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
                if menu_button.is_pressed(mouse_pos, mouse_pressed):
                    dt = datetime.datetime.now() - datetime.datetime.now()
                    is_menu = True
                    is_hiryanov_menu = False
                    menu_music = False
                    run = False

"""
def level_1(bg, screen):
    """

    :param bg:
    :param screen:
    :return:
    """
    global is_game_over, running_1, is_menu, is_landay, menu_music, Number_of_level, amount_passed_levels, dict, \
        switch_pause, date_time_obj4, is_pass_level_screen, is_red_key, progress
    Number_of_level = 1

    date_time_obj1 = datetime.datetime.now()
    invisible_time = 0

    collect_gallery_feature_sound = pygame.mixer.Sound("Sounds/Collect_gallery_feature.wav")
    is_gallery_sound = True

    pygame.mixer.music.set_volume(dict["music_volume"])
    pygame.mixer.music.load("Music/chocolate-chip-by-uncle-morris.mp3")
    pygame.mixer.music.play(-1)

    typical_enemy_1 = Enemy(WIN_WIDTH / 7, PLATFORM_HEIGHT * 10)
    typical_enemy_2 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 7.5, PLATFORM_HEIGHT * 5)
    typical_enemy_3 = Enemy(WIN_WIDTH / 1.38, PLATFORM_HEIGHT * 7, 2)
    typical_enemy_4 = Enemy(WIN_WIDTH / 1.535, PLATFORM_HEIGHT * 20)

    if dict["is_yellow_key"] == 0:
        hero = Player(PLATFORM_WIDTH, WIN_HEIGHT - PLATFORM_HEIGHT)  # создаем героя по (x,y) координатам
    elif dict["is_yellow_key"] == 1:
        if dict["health"] == 200:
            hero = Player(PLATFORM_WIDTH, WIN_HEIGHT - PLATFORM_HEIGHT, HEALTH=200)
        if dict["health"] == 100:
            hero = Player(PLATFORM_WIDTH, WIN_HEIGHT - PLATFORM_HEIGHT)
    left = right = False  # по умолчанию — стоим
    Up = False

    landay = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    level_exits = []
    enemies = []
    gallery_features = []

    if dict["is_yellow_key"] == 1:
        heart = True
    if dict["is_yellow_key"] == 0:
        heart = False

    entities.add(hero)
    entities.add(typical_enemy_1, typical_enemy_2, typical_enemy_3, typical_enemy_4)
    enemies.append(typical_enemy_1)
    enemies.append(typical_enemy_2)
    enemies.append(typical_enemy_3)
    enemies.append(typical_enemy_4)

    level = [
        "------------------------------------------------",
        "-                                               ",
        "-                      -      c                *",
        "-                             -                 ",
        "-             --   -       -                   -",
        "-                      -                       -",
        "-                                      ----    -",
        "-              -                               -",
        "-                                -----         -",
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
                # создаем блок, заливаем его цветом и рисуем его
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
            if heart and hero.health == 0 and god_mode == 0:
                invisible_time = FPS // 1.5
                hero.health = 100
                heart = False
            elif invisible_time > 0:
                invisible_time -= 1
                hero.health = 100

            if hero.health or god_mode == 1  > 0:
                screen.blit(bg, (0, 0))  # Каждую итерацию движения перса необходимо всё перерисовывать
                hero.update(left, right, Up, platforms)  # передвижение
                typical_enemy_1.update()
                typical_enemy_2.update()
                typical_enemy_3.update(26)
                typical_enemy_4.update(35)
                entities.draw(screen)  # отображение

                if hero.health == 100:
                    xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(xp, (PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                    if dict["is_yellow_key"] == 1:
                        empty_double_xp = pygame.image.load("Textures/hud_heartEmpty.png")
                        screen.blit(empty_double_xp, (5 * PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                elif hero.health == 200:
                    xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(xp, (PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                    double_xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(double_xp, (5 * PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))

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
                        except KeyError:
                            dict["your_time_seconds_1"] = your_time_seconds
                        if dict["your_time_seconds_1"] <= 12.5:
                            dict["is_red_key"] = 1

                        dict["amount_passed_levels"] = 1
                        dict["health"] = hero.health
                        if landay:
                            is_landay = 1
                            dict["is_landay"] = 1
                        progress = (dict["is_einstein"] + dict["is_landay"] + dict["is_karasev"] + dict["is_red_key"] +
                                    dict["is_yellow_key"]
                                    + dict["amount_passed_levels"] + is_1 + is_2 + is_3) * 100 // 11
                        with open("saves.json", 'w') as foo:
                            json.dump(dict, foo)
                        with open("saves.json", 'r') as foo:
                            dict = json.load(foo)

                        menu_music = False
                        is_pass_level_screen = True
                        while is_pass_level_screen:
                            pass_level_screen(bg, screen, your_time, your_time_seconds)
                        run = False
                for g in gallery_features:
                    if sprite.collide_rect(hero, g):
                        if is_gallery_sound:
                            collect_gallery_feature_sound.play()
                            is_gallery_sound = False
                        entities.remove(gallery_feature)
                        landay = True
            elif hero.health<= 0 and god_mode == 0 :
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
           switch_pause, is_pass_level_screen, is_red_key


def level_2(bg, screen):
    """

    :param bg:
    :param screen:
    :return:
    """
    global is_game_over, running_2, is_menu, is_einstein, menu_music, Number_of_level, dict, switch_pause, \
        date_time_obj4, dt, is_pass_level_screen, is_red_key, progress
    Number_of_level = 2

    collect_gallery_feature_sound = pygame.mixer.Sound("Sounds/Collect_gallery_feature.wav")
    is_gallery_sound = True

    pygame.mixer.music.set_volume(dict["music_volume"])
    pygame.mixer.music.load("Music/Office_Passenger_Dirty_Love.mp3")
    pygame.mixer.music.play(-1)

    invisible_time = 0

    typical_enemy_1 = Enemy(PLATFORM_WIDTH * 5, PLATFORM_HEIGHT * 23, 3)
    typical_enemy_2 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 8, PLATFORM_HEIGHT * 3, 2)
    typical_enemy_3 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 13, PLATFORM_HEIGHT * 3)
    typical_enemy_4 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 18, PLATFORM_HEIGHT * 3, 2)
    typical_enemy_5 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 22, PLATFORM_HEIGHT * 3)
    typical_enemy_6 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 26.5, PLATFORM_HEIGHT * 3, 4)
    typical_enemy_7 = Enemy(PLATFORM_WIDTH * 30.5, PLATFORM_HEIGHT * 22)
    archer_enemy_1 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 12, PLATFORM_HEIGHT * 5, enemy_image="enemy_2")
    archer_enemy_2 = Enemy(PLATFORM_WIDTH * 9, PLATFORM_HEIGHT * 7, enemy_image="enemy_2")
    archer_enemy_3 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 17, PLATFORM_HEIGHT * 7, enemy_image="enemy_2_straight")
    archer_enemy_4 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 17, PLATFORM_HEIGHT * 11, enemy_image="enemy_2")
    archer_enemy_5 = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 15, PLATFORM_HEIGHT * 9, enemy_image="enemy_2_90")

    if dict["is_yellow_key"] == 0:
        hero = Player(PLATFORM_WIDTH, WIN_HEIGHT - PLATFORM_HEIGHT * 7)  # создаем героя по (x,y) координатам
    elif dict["is_yellow_key"] == 1:
        if dict["health"] == 200:
            hero = Player(PLATFORM_WIDTH, WIN_HEIGHT - PLATFORM_HEIGHT * 7, HEALTH=200)
        if dict["health"] == 100:
            hero = Player(PLATFORM_WIDTH, WIN_HEIGHT - PLATFORM_HEIGHT * 7)
    # (x,y) координатам
    left = right = False  # по умолчанию — стоим
    Up = False

    einstein = False
    red_key = False
    yellow_key = False

    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    disappear_platforms = []
    passes_in_level = []
    level_exits = []
    enemies = []
    bullets_1 = []
    bullets_2 = []
    bullets_3 = []
    bullets_4 = []
    bullets_5 = []
    lavas = []
    redkeys = []
    yellowkeys = []
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
    if dict["is_yellow_key"] == 1:
        heart = True
    if dict["is_yellow_key"] == 0:
        heart = False

    run = True
    while run:
        timer.tick(FPS)
        if switch:
            if part_1:
                level = Level_2.lvl_1
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
                            pfo = Platform(x, y + PLATFORM_HEIGHT / 4, "platform")
                            entities.add(pfo)
                            platforms.append(pfo)
                        if col == "/":
                            level_exit = Platform(x, y, "exit_door_180")
                            entities.add(level_exit)
                            platforms.append(level_exit)
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
                        if col == "+":
                            sdv = Platform(x + PLATFORM_WIDTH / 8, y + PLATFORM_HEIGHT / 8, "platform")
                            entities.add(sdv)
                            platforms.append(sdv)
                        if dict["is_red_key"] == 1:
                            if col == "k":
                                key = Platform(x, y, "keyRed")
                                entities.add(key)
                                redkeys.append(key)
                        if col == "K":
                            yellowkey = Platform(x, y, "keyYellow")
                            entities.add(yellowkey)
                            yellowkeys.append(yellowkey)
                        if not is_einstein:
                            if col == "c":
                                gallery_einstein = "gallery_einstein"
                                gallery_feature = Platform(x, y, gallery_einstein)
                                entities.add(gallery_feature)
                                gallery_features.append(gallery_feature)
                        if not red_key:
                            if col == "d":
                                platf = Platform(x, y, "platform")
                                entities.add(platf)
                                disappear_platforms.append(platf)

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
            if heart and hero.health == 0 and god_mode == 0:
                invisible_time = FPS // 1.5
                hero.health = 100
                heart = False
            elif invisible_time > 0:
                invisible_time -= 1
                hero.health = 100

            if hero.health  > 0 or god_mode ==1:
                screen.blit(bg, (0, 0))  # Каждую итерацию движения перса необходимо всё перерисовывать
                hero.update(left, right, Up, platforms)  # передвижение
                typical_enemy_1.update(move_counter=25)
                typical_enemy_2.update(move_counter=15)
                typical_enemy_3.update(move_counter=16)
                typical_enemy_4.update(move_counter=16)
                typical_enemy_5.update(move_counter=18)
                typical_enemy_6.update(move_counter=10)
                typical_enemy_7.update(move_counter=20)

                date_time_obj2 = datetime.datetime.now()
                time_delta = date_time_obj2 - date_time_obj1
                seconds = time_delta.total_seconds()

                for k in redkeys:
                    if sprite.collide_rect(hero, k):
                        entities.remove(key)
                        red_key = True
                        entities.remove(platf)
                        disappear_platforms.clear()
                for K in yellowkeys:
                    if sprite.collide_rect(hero, K):
                        entities.remove(yellowkey)
                        yellowkeys.remove(yellowkey)
                        yellow_key = True

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

                if hero.health == 100:
                    xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(xp, (PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                    if dict["is_yellow_key"] == 1:
                        empty_double_xp = pygame.image.load("Textures/hud_heartEmpty.png")
                        screen.blit(empty_double_xp, (5 * PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                elif hero.health == 200:
                    xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(xp, (PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                    double_xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(double_xp, (5 * PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))

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
                        except KeyError:
                            dict["your_time_seconds_2"] = your_time_seconds

                        if yellow_key:
                            dict["is_yellow_key"] = 1

                        dict["amount_passed_levels"] = 2
                        dict["health"] = hero.health

                        if einstein:
                            is_einstein = 1
                            dict["is_einstein"] = 1
                        progress = (dict["is_einstein"] + dict["is_landay"] + dict["is_karasev"] + dict["is_red_key"] +
                                    dict["is_yellow_key"]
                                    + dict["amount_passed_levels"] + is_1 + is_2 + is_3) * 100 // 11
                        with open("saves.json", 'w') as foo:
                            json.dump(dict, foo)
                        with open("saves.json", 'r') as foo:
                            dict = json.load(foo)

                        menu_music = False
                        is_pass_level_screen = True
                        while is_pass_level_screen:
                            pass_level_screen(bg, screen, your_time, your_time_seconds)
                        run = False
                for g in gallery_features:
                    if sprite.collide_rect(hero, g):
                        if is_gallery_sound:
                            collect_gallery_feature_sound.play()
                            is_gallery_sound = False
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
                        invisible_time = 0
            elif hero.health<= 0 and god_mode == 0 :
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

    return is_game_over, running_2, is_einstein, is_menu, menu_music, switch_pause, dt, is_red_key


def level_3_1(bg, screen):
    """

    :param bg:
    :param screen:
    :return:
    """
    global is_game_over, running_3_1, is_menu, is_landay, menu_music, Number_of_level, amount_passed_levels, dict, \
        switch_pause, date_time_obj4, is_pass_level_screen, running_3_2
    Number_of_level = 31

    date_time_obj1 = datetime.datetime.now()
    invisible_time = 0

    pygame.mixer.music.set_volume(dict["music_volume"])
    pygame.mixer.music.load("Music/boss_music_1.mp3")
    pygame.mixer.music.play(-1)
    hero = Player(PLATFORM_WIDTH * 3, WIN_HEIGHT - PLATFORM_HEIGHT * 4)
    if dict["is_yellow_key"] == 0:
        hero = Player(PLATFORM_WIDTH * 3, WIN_HEIGHT - PLATFORM_HEIGHT * 4)  # создаем героя по (x,y) координатам
    elif dict["is_yellow_key"] == 1:
        if dict["health"] == 200:
            hero = Player(PLATFORM_WIDTH * 3, WIN_HEIGHT - PLATFORM_HEIGHT * 4, HEALTH=200)
        if dict["health"] == 100:
            hero = Player(PLATFORM_WIDTH * 3, WIN_HEIGHT - PLATFORM_HEIGHT * 4)
    left = right = False  # по умолчанию — стоим
    Up = False
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    level_exits = []
    enemies = []
    lavas = []
    gallery_features = []
    bullets = []
    # bullets_1 = []
    bullets_2 = []
    bullets_3 = []
    bullets_4 = []
    bullets_5 = []
    bullets_6 = []
    archer_enemies = []

    if dict["is_yellow_key"] == 1:
        heart = True
    if dict["is_yellow_key"] == 0:
        heart = False
    hurt = False

    # archer_enemy_1 = Enemy(PLATFORM_WIDTH * 6, PLATFORM_HEIGHT * 2.5, enemy_image="enemy_2_straight")
    # archer_enemy_2 = Enemy(PLATFORM_WIDTH * 12, PLATFORM_HEIGHT * 4, enemy_image="enemy_2_straight")
    # archer_enemy_3 = Enemy(PLATFORM_WIDTH * 19, PLATFORM_HEIGHT * 5, enemy_image="enemy_2_straight")
    archer_enemy_4 = Enemy(PLATFORM_WIDTH * 6, PLATFORM_HEIGHT * 2.5, enemy_image="enemy_2_straight")
    archer_enemy_5 = Enemy(PLATFORM_WIDTH * 12, PLATFORM_HEIGHT * 2.5, enemy_image="enemy_2_straight")
    archer_enemy_6 = Enemy(PLATFORM_WIDTH * 18, PLATFORM_HEIGHT * 2.5, enemy_image="enemy_2_straight")

    boss = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 16, WIN_HEIGHT / 2, enemy_image="boss_1")
    entities.add(hero)
    entities.add(boss)
    enemies.append(boss)

    boss.health = 100

    level = [
        "                                                ",
        "                                                ",
        "                                                ",
        "      =                                         ",
        "                                                ",
        "            -                                   ",
        "                   -                            ",
        "   <                                            ",
        "           =                                    ",
        "                      <                         ",
        "       =                                        ",
        "                                                ",
        "              -   -   =                         ",
        "                                                ",
        "    -                                           ",
        "            <                                   ",
        "                     -                          ",
        "       =                                        ",
        "                                                ",
        "                  <                             ",
        "            -                                   ",
        "   -                                            ",
        "                                                ",
        "                                                ",
        "________________________________________________"]

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                # создаем блок, заливаем его цветом и рисуем его
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "=":
                pfo = Platform(x, y + PLATFORM_HEIGHT / 2)
                entities.add(pfo)
                platforms.append(pfo)
            if col == "<":
                pfol = Platform(x - PLATFORM_WIDTH / 2, y)
                entities.add(pfol)
                platforms.append(pfol)
            if col == "*":
                level_exit = Platform(x, y, "exit_door")
                entities.add(level_exit)
                level_exits.append(level_exit)
            if col == "_":
                lava = Platform(x, y, "lava_erase")
                entities.add(lava)
                lavas.append(lava)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0

    run = True
    while run:
        timer.tick(FPS)

        if running_3_1 == 1:

            hero.collide_enemy(enemies, hero)
            if heart and hero.health == 0:
                invisible_time = FPS // 1.5
                hero.health = 100
                heart = False
            elif invisible_time > 0:
                invisible_time -= 1
                hero.health = 100

            if hero.health > 0 or god_mode == 1:

                date_time_obj2 = datetime.datetime.now()
                time_delta = date_time_obj2 - date_time_obj1
                seconds = time_delta.total_seconds()

                screen.blit(bg, (0, 0))  # Каждую итерацию движения перса необходимо всё перерисовывать
                hero.update(left, right, Up, platforms)  # передвижение

                centerX_hero, centerY_hero = hero.rect.center
                centerX_boss, centerY_boss = boss.rect.center
                bottomleftX, bottomleftY = boss.rect.bottomleft
                bottomrightX, bottomrightY = boss.rect.bottomright

                dy_1 = centerY_hero - centerY_boss
                boss.update(move_counter=280, b=dy_1, d=boss.health / 100, enemy_image="boss_1",
                            bottomleftX=bottomleftX,
                            bottomleftY=bottomleftY, bottomrightX=bottomrightX)

                if ((seconds + 1) // 1) % 5 == 0 and len(bullets) == 0 and centerX_boss > PLATFORM_WIDTH * 30:
                    r = random.random()
                    if r > 0.8:
                        bullet = Enemy(centerX_boss, centerY_boss, 20, "bomb_big_green", color="green")
                    if r <= 0.8:
                        bullet = Enemy(centerX_boss, centerY_boss, 20, "bomb_big_purple")
                    bullets.append(bullet)
                    enemies.append(bullet)
                    entities.add(bullet)

                    centerX_hero, centerY_hero = hero.rect.center
                    centerX_bullet, centerY_bullet = bullet.rect.center
                    dx = centerX_hero - centerX_bullet
                    dy = centerY_hero - centerY_bullet
                    c = (dx ** 2 + dy ** 2) ** 0.5

                if len(bullets) > 0:
                    if bullet.rect.x < WIN_WIDTH or bullet.rect.x > 0 or bullet.rect.y < WIN_HEIGHT \
                            or bullet.rect.y > 0:
                        bullet.update(enemy_image="bomb_big_green", a=dx, b=dy, C=c)
                    if bullet.rect.x >= WIN_WIDTH or bullet.rect.x <= 0 or bullet.rect.y >= WIN_HEIGHT \
                            or bullet.rect.y <= 0:
                        enemies.remove(bullet)
                        entities.remove(bullet)
                        bullets.remove(bullet)

                if 75 >= boss.health > 50:
                    entities.add(archer_enemy_5, archer_enemy_6, archer_enemy_4)
                    enemies.append(archer_enemy_4)
                    enemies.append(archer_enemy_5)
                    enemies.append(archer_enemy_6)
                    archer_enemies.append(archer_enemy_5)
                    archer_enemies.append(archer_enemy_6)
                    archer_enemies.append(archer_enemy_4)
                    for arc in archer_enemies:
                        arc.update(enemy_image="enemy_2_straight")
                        for p in platforms:
                            if sprite.collide_rect(arc, p):
                                arc.onGround = True

                    if ((seconds + 1) // 1) % 3 == 0 and len(bullets_4) == 0:
                        centerX_archer_4, centerY_archer_4 = archer_enemy_4.rect.center
                        bullet_4 = Enemy(centerX_archer_4, centerY_archer_4, 5, "bomb_mini")
                        bullets_4.append(bullet_4)
                        enemies.append(bullet_4)
                        entities.add(bullet_4)

                        centerX_hero, centerY_hero = hero.rect.center
                        centerX_bullet_4, centerY_bullet_4 = bullet_4.rect.center
                        dx_4 = centerX_hero - centerX_archer_4
                        dy_4 = centerY_hero - centerY_archer_4
                        c_4 = (dx_4 ** 2 + dy_4 ** 2) ** 0.5

                    if len(bullets_4) > 0:
                        if c_4 > 400 and len(bullets_4) != 0:
                            enemies.remove(bullet_4)
                            entities.remove(bullet_4)
                            bullets_4.remove(bullet_4)
                        if bullet_4.rect.x < WIN_WIDTH or bullet_4.rect.x > 0 or bullet_4.rect.y < WIN_HEIGHT \
                                or bullet_4.rect.y > 0:
                            if len(bullets_4) != 0:
                                bullet_4.update(enemy_image="bomb", a=dx_4, b=dy_4, C=c_4)
                        if bullet_4.rect.x >= WIN_WIDTH or bullet_4.rect.x <= 0 or bullet_4.rect.y >= WIN_HEIGHT \
                                or bullet_4.rect.y <= 0:
                            if len(bullets_4) != 0:
                                enemies.remove(bullet_4)
                                entities.remove(bullet_4)
                                bullets_4.remove(bullet_4)

                    if ((seconds + 1) // 1) % 3 == 0 and len(bullets_5) == 0:
                        centerX_archer_5, centerY_archer_5 = archer_enemy_5.rect.center
                        bullet_5 = Enemy(centerX_archer_5, centerY_archer_5, 5, "bomb_mini")
                        bullets_5.append(bullet_5)
                        enemies.append(bullet_5)
                        entities.add(bullet_5)

                        centerX_hero, centerY_hero = hero.rect.center
                        centerX_bullet_5, centerY_bullet_5 = bullet_5.rect.center
                        dx_5 = centerX_hero - centerX_bullet_5
                        dy_5 = centerY_hero - centerY_bullet_5
                        c_5 = (dx_5 ** 2 + dy_5 ** 2) ** 0.5

                    if len(bullets_5) > 0:
                        if c_5 > 500 and len(bullets_5) != 0:
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

                    if ((seconds + 1) // 1) % 3 == 0 and len(bullets_6) == 0:
                        centerX_archer_6, centerY_archer_6 = archer_enemy_6.rect.center
                        bullet_6 = Enemy(centerX_archer_6, centerY_archer_6, 5, "bomb_mini")
                        bullets_6.append(bullet_6)
                        enemies.append(bullet_6)
                        entities.add(bullet_6)

                        centerX_hero, centerY_hero = hero.rect.center
                        centerX_bullet_6, centerY_bullet_6 = bullet_6.rect.center
                        dx_6 = centerX_hero - centerX_bullet_6
                        dy_6 = centerY_hero - centerY_bullet_6
                        c_6 = (dx_6 ** 2 + dy_6 ** 2) ** 0.5

                    if len(bullets_6) > 0:
                        if c_6 > 500 and len(bullets_6) != 0:
                            enemies.remove(bullet_6)
                            entities.remove(bullet_6)
                            bullets_6.remove(bullet_6)
                        if bullet_6.rect.x < WIN_WIDTH or bullet_6.rect.x > 0 or bullet_6.rect.y < WIN_HEIGHT \
                                or bullet_6.rect.y > 0:
                            bullet_6.update(enemy_image="bomb_mini", a=dx_6, b=dy_6, C=c_6)
                        if bullet_6.rect.x >= WIN_WIDTH or bullet_6.rect.x <= 0 or bullet_6.rect.y >= WIN_HEIGHT \
                                or bullet_6.rect.y <= 0:
                            enemies.remove(bullet_6)
                            entities.remove(bullet_6)
                            bullets_6.remove(bullet_6)

                if boss.health <= 50:
                    hh = hero.health
                    running_3_1 = 0
                    running_3_2 = 1
                    level_3_2(bg, screen, hh, time_delta)

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
                        running_3_1 = 2
                        switch_pause = True
                    if event.type == MOUSEBUTTONDOWN:
                        try:
                            if centerX_boss - centerX_hero < 145:
                                boss.health -= 2.5
                            if bullet.color == "green":
                                centerX_hero, centerY_hero = hero.rect.center
                                centerX_bullet, centerY_bullet = bullet.rect.center
                                if 120 > centerX_bullet - centerX_hero > 0:
                                    enemies.remove(bullet)
                                    entities.remove(bullet)
                                    bullets.remove(bullet)

                                    bullet = Enemy(centerX_bullet, centerY_bullet, 20, "bomb_big_green")
                                    bullets.append(bullet)
                                    enemies.append(bullet)
                                    entities.add(bullet)
                                    hurt = True

                                    centerX_hero, centerY_hero = hero.rect.center
                                    centerX_bullet, centerY_bullet = bullet.rect.center
                                    dx = centerX_boss - centerX_bullet
                                    dy = centerY_boss - centerY_bullet
                                    c = (dx ** 2 + dy ** 2) ** 0.5

                                if len(bullets) > 0:
                                    if bullet.rect.x < WIN_WIDTH or bullet.rect.x > 0 or bullet.rect.y < WIN_HEIGHT \
                                            or bullet.rect.y > 0:
                                        bullet.update(enemy_image="bomb_big_green", a=-dx, b=-dy, C=c)
                                    if bullet.rect.x >= WIN_WIDTH or bullet.rect.x <= 0 or bullet.rect.y >= WIN_HEIGHT \
                                            or bullet.rect.y <= 0:
                                        enemies.remove(bullet)
                                        entities.remove(bullet)
                                        bullets.remove(bullet)
                        except:
                            pass
                try:
                    for b in bullets:
                        if sprite.collide_rect(boss, b) and hurt:
                            boss.health -= 5
                            hurt = False
                            enemies.remove(bullet)
                            entities.remove(bullet)
                            bullets.remove(bullet)
                except:
                    pass

                entities.draw(screen)  # отображение
                if seconds < 8:
                    p_button = Button(RED, WIN_WIDTH / 2 - PLATFORM_WIDTH, PLATFORM_HEIGHT * 4, WIN_WIDTH / 1.8,
                                      WIN_HEIGHT / 15, 'Click left mouse button to')
                    p_button.draw(screen)

                    h_button = Button(RED, WIN_WIDTH / 2 - PLATFORM_WIDTH, PLATFORM_HEIGHT * 6, WIN_WIDTH / 1.8,
                                      WIN_HEIGHT / 15, 'attack the boss, when you')
                    h_button.draw(screen)

                    d_button = Button(RED, WIN_WIDTH / 2 - PLATFORM_WIDTH, PLATFORM_HEIGHT * 8, WIN_WIDTH / 1.8,
                                      WIN_HEIGHT / 15, 'nearly him'
                                                       ' or reflect green bomb')
                    d_button.draw(screen, size=48)

                if hero.health == 100:
                    xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(xp, (PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                    if dict["is_yellow_key"] == 1:
                        empty_double_xp = pygame.image.load("Textures/hud_heartEmpty.png")
                        screen.blit(empty_double_xp, (5 * PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                elif hero.health == 200:
                    xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(xp, (PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                    double_xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(double_xp, (5 * PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))

                date_time_obj3 = datetime.datetime.now()
                time_delta_2 = date_time_obj3 - date_time_obj1 - dt

                time_button = Button(RED, PLATFORM_WIDTH * 43, PLATFORM_HEIGHT / 2,
                                     0.000001,
                                     0.000001, f'{time_delta_2}')
                time_button.draw(screen, Color=WHITE, size=36)

                for l in lavas:
                    if sprite.collide_rect(hero, l):
                        running_3_1 = 0
                        is_game_over = True

            elif hero.health <= 0 and god_mode == 0 :
                Number_of_level = 31
                is_game_over = True
                run = False
                running_3_1 = 0
                game_over(bg, screen)
            pygame.display.update()  # обновление и вывод всех изменений на экран
        elif running_3_1 == 2:
            if switch_pause:
                date_time_obj4 = datetime.datetime.now()
                switch_pause = False
            while running_3_1 == 2:
                pause_menu(bg, screen)
        elif running_3_1 == 0:
            run = False

    return is_game_over, running_3_1, is_landay, is_menu, menu_music, Number_of_level, amount_passed_levels, \
           switch_pause, is_pass_level_screen, is_red_key


def level_3_2(bg, screen, hh, you_time):
    """

        :param bg:
        :param screen:
        :return:
        """
    global is_game_over, running_3_1, running_3_2, is_menu, is_landay, menu_music, Number_of_level, \
        amount_passed_levels, dict, switch_pause, date_time_obj4, is_pass_level_screen, is_hiryanov_menu, progress
    Number_of_level = 32

    invisible_time = 0
    date_time_obj1 = datetime.datetime.now()

    pygame.mixer.music.set_volume(dict["music_volume"])
    # pygame.mixer.music.load("Music/boss_music_1.mp3")
    # pygame.mixer.music.play(-1)

    hero = Player(PLATFORM_WIDTH * 10, PLATFORM_HEIGHT, HEALTH=hh)

    left = right = False  # по умолчанию — стоим
    Up = False
    entities = pygame.sprite.Group()  # Все объекты
    platforms = []  # то, во что мы будем врезаться или опираться
    level_exits = []
    enemies = []
    lavas = []
    gallery_features = []
    bullets = []
    # bullets_1 = []
    bullets_2 = []
    bullets_3 = []
    bullets_4 = []
    bullets_5 = []
    bullets_6 = []
    horizontal_bullets = []
    archer_enemies = []

    if dict["is_yellow_key"] == 1:
        heart = True
    if dict["is_yellow_key"] == 0:
        heart = False
    hurt = False

    # archer_enemy_2 = Enemy(PLATFORM_WIDTH * 12, PLATFORM_HEIGHT * 4, enemy_image="enemy_2_straight")
    # archer_enemy_3 = Enemy(PLATFORM_WIDTH * 19, PLATFORM_HEIGHT * 5, enemy_image="enemy_2_straight")
    archer_enemy_4 = Enemy(PLATFORM_WIDTH * 6, PLATFORM_HEIGHT * 1.5, enemy_image="enemy_2_straight")
    archer_enemy_5 = Enemy(PLATFORM_WIDTH * 22, PLATFORM_HEIGHT * 1.5, enemy_image="enemy_2_straight")
    archer_enemy_6 = Enemy(PLATFORM_WIDTH * 38, PLATFORM_HEIGHT * 1.5, enemy_image="enemy_2_straight")
    typical_enemy_1 = Enemy(PLATFORM_WIDTH * 22, PLATFORM_HEIGHT * 2.5)
    typical_enemy_2 = Enemy(PLATFORM_WIDTH * 33, PLATFORM_HEIGHT * 3)
    typical_enemy_3 = Enemy(PLATFORM_WIDTH * 36, PLATFORM_HEIGHT * 8)
    typical_enemy_4 = Enemy(PLATFORM_WIDTH * 36, PLATFORM_HEIGHT * 13.5)
    typical_enemy_5 = Enemy(PLATFORM_WIDTH * 14.5, PLATFORM_HEIGHT * 9)
    typical_enemy_6 = Enemy(PLATFORM_WIDTH * 12.5, PLATFORM_HEIGHT * 16.5)
    boss_right = Enemy(WIN_WIDTH - PLATFORM_WIDTH * 6, WIN_HEIGHT / 2, enemy_image="boss_1_right")
    boss_left = Enemy(PLATFORM_WIDTH * 3.5, WIN_HEIGHT / 2, enemy_image="boss_1_left")
    entities.add(hero)
    entities.add(boss_right, boss_left, typical_enemy_1, typical_enemy_2, typical_enemy_3, typical_enemy_4,
                 typical_enemy_5, typical_enemy_6)
    enemies.append(boss_right)
    enemies.append(typical_enemy_1)
    enemies.append(typical_enemy_2)
    enemies.append(typical_enemy_3)
    enemies.append(typical_enemy_4)
    enemies.append(typical_enemy_5)
    enemies.append(typical_enemy_6)
    enemies.append(boss_left)

    switch = True

    level = [
        "                                                ",
        "                                                ",
        "                                                ",
        "                   ======<                      ",
        "                               ------           ",
        "              -                                 ",
        "                                                ",
        "          -                 =                   ",
        "                                                ",
        "                                  -----         ",
        "             ----    ===                        ",
        "            -                                   ",
        "                             ---                ",
        "                                                ",
        "           -       -              =====         ",
        "                                                ",
        "                                                ",
        "          ======      =     ==  ==              ",
        "                                                ",
        "                                                ",
        "                                                ",
        "                    ---   =   --                ",
        "                                                ",
        "                                                ",
        "________________________________________________"]
    boss_left.health = 100
    boss_right.health = 100

    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                # создаем блок, заливаем его цветом и рисуем его
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "=":
                pfo = Platform(x, y + PLATFORM_HEIGHT / 2)
                entities.add(pfo)
                platforms.append(pfo)
            if col == "<":
                pfol = Platform(x - PLATFORM_WIDTH / 2, y + PLATFORM_HEIGHT / 2)
                entities.add(pfol)
                platforms.append(pfol)
            if col == "*":
                level_exit = Platform(x, y, "exit_door")
                entities.add(level_exit)
                level_exits.append(level_exit)
            if col == "_":
                lava = Platform(x, y, "lava_erase")
                entities.add(lava)
                lavas.append(lava)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0

    run = True
    while run:
        timer.tick(FPS)
        if running_3_2 == 1:
            hero.collide_enemy(enemies, hero)
            if heart and hero.health == 0:
                invisible_time = FPS // 1.5
                hero.health = 100
                heart = False
            elif invisible_time > 0:
                invisible_time -= 1
                hero.health = 100

            if hero.health > 0 or god_mode == 1:

                screen.blit(bg, (0, 0))  # Каждую итерацию движения перса необходимо всё перерисовывать
                hero.update(left, right, Up, platforms)  # передвижение
                typical_enemy_1.update(70)
                typical_enemy_2.update()
                typical_enemy_3.update()
                typical_enemy_4.update()
                typical_enemy_5.update()
                typical_enemy_6.update(70)

                date_time_obj2 = datetime.datetime.now()
                time_delta_3 = date_time_obj2 - date_time_obj1 + you_time
                seconds = time_delta_3.total_seconds()

                centerX_hero, centerY_hero = hero.rect.center
                centerX_boss_right, centerY_boss_right = boss_right.rect.center
                centerX_boss_left, centerY_boss_left = boss_left.rect.center
                right_bottomleftX, right_bottomleftY = boss_right.rect.bottomleft
                right_bottomrightX, right_bottomrightY = boss_right.rect.bottomright
                left_bottomleftX, left_bottomleftY = boss_left.rect.bottomleft
                left_bottomrightX, left_bottomrightY = boss_left.rect.bottomright
                left_topleftX, left_topleftY = boss_left.rect.topleft

                dy_1 = centerY_hero - centerY_boss_right
                dy_2 = centerY_hero - centerY_boss_left

                if boss_left.health > 0:
                    if 8 < (seconds + 5) % 10 <= 8.5:
                        boss_left.image.fill(WHITE)
                    elif 8.5 < (seconds + 5) % 10 <= 9:
                        boss_left.image = image.load('Textures/boss_1_left.png')
                    if 9 < (seconds + 5) % 10 <= 9.5:
                        boss_left.image.fill(WHITE)
                    elif 9.5 < (seconds + 5) % 10 <= 9.99999:
                        boss_left.image = image.load('Textures/boss_1_left.png')
                    boss_left.update(b=dy_1, d=boss_left.health / 100, enemy_image="boss_1_left",
                                     bottomleftX=left_bottomleftX,
                                     bottomleftY=left_bottomleftY, bottomrightX=left_bottomrightX, s=seconds % 10,
                                     topleftX=left_topleftX, topleftY=left_topleftY, move_counter=90)
                    if ((seconds + 5) // 1) % 10 == 0 and len(horizontal_bullets) == 0:
                        horizontal_bullet = Enemy(centerX_boss_left, centerY_boss_left, enemy_image="horizontal_attack")
                        horizontal_bullets.append(horizontal_bullet)
                        enemies.append(horizontal_bullet)
                        entities.add(horizontal_bullet)
                        cooldown = FPS * 1.5
                    if len(horizontal_bullets) > 0:
                        cooldown -= 1
                        if cooldown == 0:
                            enemies.remove(horizontal_bullet)
                            entities.remove(horizontal_bullet)
                            horizontal_bullets.remove(horizontal_bullet)
                elif boss_left.health == 0 and switch:
                    enemies.remove(boss_left)
                    switch = False

                if boss_right.health > 0:
                    boss_right.update(move_counter=95, b=dy_2, d=boss_left.health / 100, enemy_image="boss_1_right",
                                      bottomleftX=right_bottomleftX,
                                      bottomleftY=right_bottomleftY, bottomrightX=right_bottomrightX)
                    if ((seconds + 1) // 1) % 6 == 0 and len(bullets) == 0 and centerX_boss_right > PLATFORM_WIDTH * 30:
                        r = random.random()
                        if r > 0.8:
                            bullet = Enemy(centerX_boss_right, centerY_boss_right, 12, "bomb_big_green", color="green")
                        if r <= 0.8:
                            bullet = Enemy(centerX_boss_right, centerY_boss_right, 12, "bomb_big_purple")
                        bullets.append(bullet)
                        enemies.append(bullet)
                        entities.add(bullet)

                        centerX_hero, centerY_hero = hero.rect.center
                        centerX_bullet, centerY_bullet = bullet.rect.center
                        dx = centerX_hero - centerX_bullet
                        dy = centerY_hero - centerY_bullet
                        c = (dx ** 2 + dy ** 2) ** 0.5

                    if len(bullets) > 0:
                        if bullet.rect.x < WIN_WIDTH or bullet.rect.x > 0 or bullet.rect.y < WIN_HEIGHT \
                                or bullet.rect.y > 0:
                            bullet.update(enemy_image="bomb_big_green", a=dx, b=dy, C=c)
                        if bullet.rect.x >= WIN_WIDTH or bullet.rect.x <= 0 or bullet.rect.y >= WIN_HEIGHT \
                                or bullet.rect.y <= 0:
                            enemies.remove(bullet)
                            entities.remove(bullet)
                            bullets.remove(bullet)
                elif boss_right.health == 0 and switch:
                    enemies.remove(boss_right)
                    switch = False

                if boss_left.health == 0 or boss_right.health == 0:
                    entities.add(archer_enemy_5, archer_enemy_6, archer_enemy_4)
                    enemies.append(archer_enemy_4)
                    enemies.append(archer_enemy_5)
                    enemies.append(archer_enemy_6)
                    archer_enemies.append(archer_enemy_5)
                    archer_enemies.append(archer_enemy_6)
                    archer_enemies.append(archer_enemy_4)
                    for arc in archer_enemies:
                        arc.update(enemy_image="enemy_2_straight")
                        for p in platforms:
                            if sprite.collide_rect(arc, p):
                                arc.onGround = True
                    if ((seconds + 1) // 1) % 3 == 0 and len(bullets_4) == 0:
                        centerX_archer_4, centerY_archer_4 = archer_enemy_4.rect.center
                        bullet_4 = Enemy(centerX_archer_4, centerY_archer_4, 5, "bomb_mini")
                        bullets_4.append(bullet_4)
                        enemies.append(bullet_4)
                        entities.add(bullet_4)

                        centerX_hero, centerY_hero = hero.rect.center
                        centerX_bullet_4, centerY_bullet_4 = bullet_4.rect.center
                        dx_4 = centerX_hero - centerX_archer_4
                        dy_4 = centerY_hero - centerY_archer_4
                        c_4 = (dx_4 ** 2 + dy_4 ** 2) ** 0.5

                    if len(bullets_4) > 0:
                        if c_4 > 400 and len(bullets_4) != 0:
                            enemies.remove(bullet_4)
                            entities.remove(bullet_4)
                            bullets_4.remove(bullet_4)
                        if bullet_4.rect.x < WIN_WIDTH or bullet_4.rect.x > 0 or bullet_4.rect.y < WIN_HEIGHT \
                                or bullet_4.rect.y > 0:
                            if len(bullets_4) != 0:
                                bullet_4.update(enemy_image="bomb", a=dx_4, b=dy_4, C=c_4)
                        if bullet_4.rect.x >= WIN_WIDTH or bullet_4.rect.x <= 0 or bullet_4.rect.y >= WIN_HEIGHT \
                                or bullet_4.rect.y <= 0:
                            if len(bullets_4) != 0:
                                enemies.remove(bullet_4)
                                entities.remove(bullet_4)
                                bullets_4.remove(bullet_4)

                    if ((seconds + 1) // 1) % 3 == 0 and len(bullets_5) == 0:
                        centerX_archer_5, centerY_archer_5 = archer_enemy_5.rect.center
                        bullet_5 = Enemy(centerX_archer_5, centerY_archer_5, 5, "bomb_mini")
                        bullets_5.append(bullet_5)
                        enemies.append(bullet_5)
                        entities.add(bullet_5)

                        centerX_hero, centerY_hero = hero.rect.center
                        centerX_bullet_5, centerY_bullet_5 = bullet_5.rect.center
                        dx_5 = centerX_hero - centerX_bullet_5
                        dy_5 = centerY_hero - centerY_bullet_5
                        c_5 = (dx_5 ** 2 + dy_5 ** 2) ** 0.5

                    if len(bullets_5) > 0:
                        if c_5 > 500 and len(bullets_5) != 0:
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

                    if ((seconds + 1) // 1) % 3 == 0 and len(bullets_6) == 0:
                        centerX_archer_6, centerY_archer_6 = archer_enemy_6.rect.center
                        bullet_6 = Enemy(centerX_archer_6, centerY_archer_6, 5, "bomb_mini")
                        bullets_6.append(bullet_6)
                        enemies.append(bullet_6)
                        entities.add(bullet_6)

                        centerX_hero, centerY_hero = hero.rect.center
                        centerX_bullet_6, centerY_bullet_6 = bullet_6.rect.center
                        dx_6 = centerX_hero - centerX_bullet_6
                        dy_6 = centerY_hero - centerY_bullet_6
                        c_6 = (dx_6 ** 2 + dy_6 ** 2) ** 0.5

                    if len(bullets_6) > 0:
                        if c_6 > 500 and len(bullets_6) != 0:
                            enemies.remove(bullet_6)
                            entities.remove(bullet_6)
                            bullets_6.remove(bullet_6)
                        if bullet_6.rect.x < WIN_WIDTH or bullet_6.rect.x > 0 or bullet_6.rect.y < WIN_HEIGHT \
                                or bullet_6.rect.y > 0:
                            bullet_6.update(enemy_image="bomb_mini", a=dx_6, b=dy_6, C=c_6)
                        if bullet_6.rect.x >= WIN_WIDTH or bullet_6.rect.x <= 0 or bullet_6.rect.y >= WIN_HEIGHT \
                                or bullet_6.rect.y <= 0:
                            if len(bullets_6) > 0:
                                enemies.remove(bullet_6)
                                entities.remove(bullet_6)
                                bullets_6.remove(bullet_6)

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
                        running_3_2 = 2
                        switch_pause = True
                    if event.type == MOUSEBUTTONDOWN:
                        try:
                            if abs(centerX_boss_right - centerX_hero) < 90 and abs(centerY_hero - centerY_boss_right) < 102:
                                boss_right.health -= 4
                            if abs(centerX_boss_left - centerX_hero) < 90 and abs(centerY_hero - centerY_boss_left) < 102:
                                boss_left.health -= 4
                            if bullet.color == "green":
                                centerX_hero, centerY_hero = hero.rect.center
                                centerX_bullet, centerY_bullet = bullet.rect.center
                                if 120 > centerX_bullet - centerX_hero > 0:
                                    enemies.remove(bullet)
                                    entities.remove(bullet)
                                    bullets.remove(bullet)

                                    bullet = Enemy(centerX_bullet, centerY_bullet, 20, "bomb_big_green")
                                    bullets.append(bullet)
                                    enemies.append(bullet)
                                    entities.add(bullet)
                                    hurt = True

                                    centerX_hero, centerY_hero = hero.rect.center
                                    centerX_bullet, centerY_bullet = bullet.rect.center
                                    dx = centerX_boss_right - centerX_bullet
                                    dy = centerY_boss_right - centerY_bullet
                                    c = (dx ** 2 + dy ** 2) ** 0.5

                                if len(bullets) > 0:
                                    if bullet.rect.x < WIN_WIDTH or bullet.rect.x > 0 or bullet.rect.y < WIN_HEIGHT \
                                            or bullet.rect.y > 0:
                                        bullet.update(enemy_image="bomb_big_green", a=-dx, b=-dy, C=c)
                                    if bullet.rect.x >= WIN_WIDTH or bullet.rect.x <= 0 or bullet.rect.y >= WIN_HEIGHT \
                                            or bullet.rect.y <= 0:
                                        enemies.remove(bullet)
                                        entities.remove(bullet)
                                        bullets.remove(bullet)
                        except:
                            pass
                try:
                    for b in bullets:
                        if sprite.collide_rect(boss_right, b) and hurt:
                            boss_right.health -= 10
                            hurt = False
                            enemies.remove(bullet)
                            entities.remove(bullet)
                            bullets.remove(bullet)
                except:
                    pass

                if boss_right.health < 0:
                    boss_right.health = 0
                if boss_left.health < 0:
                    boss_left.health = 0

                if boss_right.health <= 0 or boss_left.health <= 0:
                    your_time = time_delta_3
                    timestr = f'{your_time}'
                    ftr = [3600, 60, 1, 10 ** (-6)]
                    your_time_seconds = sum([a * b for a, b in zip(ftr, map(float, timestr.split(':')))])
                    try:
                        if your_time_seconds < dict["your_time_seconds_3"]:
                            dict["your_time_seconds_3"] = your_time_seconds
                    except KeyError:
                        dict["your_time_seconds_3"] = your_time_seconds


                    dict["health"] = hero.health
                    dict["is_karasev"] = 1
                    progress = (dict["is_einstein"] + dict["is_landay"] + dict["is_karasev"] + dict["is_red_key"] +
                                dict["is_yellow_key"]
                                + dict["amount_passed_levels"] + is_1 + is_2 + is_3) * 100 // 11
                    #with open("saves.json", 'w') as foo:
                        #json.dump(dict, foo)
                    #with open("saves.json", 'r') as foo:
                        #dict = json.load(foo)

                    menu_music = False
                    is_pass_level_screen = True
                    while is_pass_level_screen:
                        pass_level_screen(bg, screen, your_time, your_time_seconds)
                    run = False
                entities.draw(screen)  # отображение

                if hero.health == 100:
                    xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(xp, (PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                    if dict["is_yellow_key"] == 1:
                        empty_double_xp = pygame.image.load("Textures/hud_heartEmpty.png")
                        screen.blit(empty_double_xp, (5 * PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                elif hero.health == 200:
                    xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(xp, (PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))
                    double_xp = pygame.image.load("Textures/hud_heartFull.png")
                    screen.blit(double_xp, (5 * PLATFORM_WIDTH / 2, PLATFORM_HEIGHT / 2))

                date_time_obj3 = datetime.datetime.now()
                time_delta_2 = date_time_obj3 - date_time_obj1 - dt

                time_button = Button(RED, PLATFORM_WIDTH * 43, PLATFORM_HEIGHT / 2,
                                     0.000001,
                                     0.000001, f'{time_delta_2}')
                time_button.draw(screen, Color=WHITE, size=36)

                for l in lavas:
                    if sprite.collide_rect(hero, l):
                        hero.health = 0
                        invisible_time = 0
                        running_3_1 = 0
                        is_game_over = True

                pygame.display.update()

            elif hero.health <= 0 and god_mode == 0:
                Number_of_level = 31
                is_game_over = True
                run = False
                running_3_2 = 0
                game_over(bg, screen)
            pygame.display.update()  # обновление и вывод всех изменений на экран
        elif running_3_2 == 2:
            if switch_pause:
                date_time_obj4 = datetime.datetime.now()
                switch_pause = False
            while running_3_2 == 2:
                pause_menu(bg, screen)
        elif running_3_2 == 0:
            run = False

    return is_game_over, running_3_1, running_3_1, is_landay, is_menu, menu_music, Number_of_level, \
           amount_passed_levels, switch_pause, is_pass_level_screen, is_red_key


def main():
    pygame.init()  # Инициация PyGame, обязательная строчка
    pygame.mixer.pre_init(44100, -16, 2, 512)
    mixer.init()
    screen = pygame.display.set_mode(DISPLAY)
    # screen = pygame.display.set_mode(DISPLAY, pygame.DOUBLEBUF | pygame.OpenGL)  # Создаем окошко
    pygame.display.set_caption("SUPER FOPF BOY")  # Пишем в шапку
    # pygame.display.set_icon(pygame.image.load("icon.png"))
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности, будем использовать как фон
    # glClearColor(BACKGROUND_COLOR/255, 1)
    # bg = pygame.image.load("Textures/Background.png")
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
        elif running_3_1 != 0:
            while running_3_1:
                level_3_1(bg, screen)
        elif is_game_over:
            while is_game_over:
                game_over(bg, screen)
        elif is_restart:
            restart()
        elif is_achievements_menu:
            while is_achievements_menu:
                achievements_menu(bg, screen)
        elif is_hiryanov_menu:
            while is_hiryanov_menu:
                hiryanov_menu(bg, screen)
        else:
            runnin = False


if __name__ == "__main__":
    main()
