#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from pygame import *
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


class Player(sprite.Sprite):
    def __init__(self, x, y, HEALTH=100):
        sprite.Sprite.__init__(self)
        self.x_vel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.y_vel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.health = HEALTH
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
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.y_vel = -JUMP_POWER
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
            if Up:
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

    def collide_enemy(self, enemies, hero):
        for en in enemies:
            if sprite.collide_rect(self, en):
                hero.health -= 100

    # def get_hurt(self, yvel, health, platforms):  # получение урона от падения
    #     for p in platforms:
    #         if not sprite.collide_rect(self, p):
    #             if yvel > 15:
    #                 if sprite.collide_rect(self, p):
    #                     health -= yvel*2

    # def draw(self, screen):  # Выводим себя на экран
    # screen.blit(self.image, (self.rect.x, self.rect.y))
