#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from pygame import *
import ctypes

COLOR = "#888888"
user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55
WIDTH = WIN_WIDTH * 16 / 960
HEIGHT = WIN_HEIGHT * 7 / 135
GRAVITY = WIN_HEIGHT * 5.4 / 21600
JUMP_POWER = WIN_HEIGHT/108
MOVE_SPEED = WIN_WIDTH * 8 / 1920
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
up = False


class Player(sprite.Sprite):
    def __init__(self, x, y, HEALTH=100):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image.fill(Color(COLOR))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.yvel = 0  # скорость вертикального перемещения
        self.onGround = False  # На земле ли я?
        self.health = HEALTH

    def update(self,  left, right, up, platforms):
        if up:
            if self.onGround:  # прыгаем, только когда можем оттолкнуться от земли
                self.yvel = -JUMP_POWER
        if left:
            self.xvel = -MOVE_SPEED  # Лево
 
        if right:
            self.xvel = MOVE_SPEED  # Право
         
        if not(left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
        if not self.onGround:
            self.yvel += GRAVITY
        self.onGround = False  # Мы не знаем, когда мы на земле((
        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, platforms)
    
    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p):  # если есть пересечение платформы с игроком

                if xvel > 0:                      # если движется вправо
                    self.rect.right = p.rect.left  # то не движется вправо

                if xvel < 0:                      # если движется влево
                    self.rect.left = p.rect.right  # то не движется влево

                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0                 # и энергия падения пропадает

                if yvel < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom  # то не движется вверх
                    self.yvel = 0                 # и энергия прыжка пропадает

    def collide_enemy(self, enemies, hero):
        for en in enemies:
            if sprite.collide_rect(self, en):
                hero.health = 0

    # def get_hurt(self, yvel, health, platforms):  # получение урона от падения
    #     for p in platforms:
    #         if not sprite.collide_rect(self, p):
    #             if yvel > 15:
    #                 if sprite.collide_rect(self, p):
    #                     health -= yvel*2

    # def draw(self, screen):  # Выводим себя на экран
    # screen.blit(self.image, (self.rect.x, self.rect.y))
