from pygame import *
import ctypes

user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
WHITE = (255, 255, 255)


class Enemy(sprite.Sprite):
    def __init__(self, x, y, move_direction=1, enemy_image="typical_enemy"):
        sprite.Sprite.__init__(self)
        self.image = image.load(f'Textures/{enemy_image}.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = move_direction
        self.move_counter = 0

    def update(self, move_counter=50, enemy_image="typical_enemy", a=1, b=0, C=1):
        if enemy_image == "typical_enemy":
            self.rect.x += self.move_direction
            self.move_counter += 1
            if abs(self.move_counter) > move_counter:
                self.move_direction *= -1
                self.move_counter *= -1
        if enemy_image == "bomb":
            self.rect.x += self.move_direction * a / C
            self.rect.y += self.move_direction * b / C
