#импортируем необходимое
import pygame.draw
from Taz_Main import *
import ctypes
#Константы
user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


class Enemy(sprite.Sprite):
    def __init__(self, x, y, move_direction=1, enemy_image="typical_enemy", health=100, color="purple"):
        sprite.Sprite.__init__(self)
        self.image = image.load(f'Textures/{enemy_image}.png')
        self.color = color
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = move_direction
        self.move_counter = 0
        self.health = health
        self.onGround = False

    def update(self, move_counter=50, enemy_image="typical_enemy", a=1, b=0, C=1, d=100,
               screen=pygame.display.set_mode(DISPLAY), bottomleftX=0, bottomleftY=0, bottomrightX=0, topleftX=0,
               topleftY=0, s=2):
        if enemy_image == "typical_enemy":#Движение "Богданова"
            self.rect.x += self.move_direction
            self.move_counter += 1 #счетчик для того чтобы понять когда двигаться обратно
            if abs(self.move_counter) > move_counter: #Движение в обратную сторону 
                self.move_direction *= -1
                self.move_counter *= -1
        if enemy_image == "bomb" or enemy_image == "bomb_mini" or enemy_image == "bomb_big_green" \
                or enemy_image == "bomb_big_purple":#Движение всех бомбочек
            self.rect.x += self.move_direction * a / C
            self.rect.y += self.move_direction * b / C
        if enemy_image == "boss_1_right" or enemy_image == "boss_1_left" or enemy_image == "boss_1":#Движение босса
            self.rect.x += self.move_direction
            self.move_counter += 1
            pygame.draw.rect(screen, GREEN, (bottomleftX, bottomleftY, (bottomrightX-bottomleftX)*d, PLATFORM_HEIGHT/4))#Полоска с hp босса
            pygame.draw.rect(screen, RED, (bottomleftX+(bottomrightX-bottomleftX)*d, bottomleftY,
                                           (bottomrightX-bottomleftX)*(1-d), PLATFORM_HEIGHT/4))
            if abs(self.move_counter) > move_counter:
                self.move_direction *= -1
                self.move_counter *= -1
            if b != 0:
                self.rect.y += b/abs(b) * abs(self.move_direction)
            if b == 0:
                self.rect.y = self.rect.y
        if enemy_image == "enemy_2_straight":
            if not self.onGround:
                self.rect.y += JUMP_POWER / 10
            else:
                pass
