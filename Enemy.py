from pygame import *
import ctypes

user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
WHITE = (255, 255, 255)


class Enemy(sprite.Sprite):
    def __init__(self, x, y, move_direction=1):
        sprite.Sprite.__init__(self)
        self.image = image.load('Textures/typical_enemy.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = move_direction
        self.move_counter = 0

    def update(self, move_counter=50):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > move_counter:
            self.move_direction *= -1
            self.move_counter *= -1
        draw.rect(display.set_mode(DISPLAY), WHITE, self.rect)
