# from pygame import sprite
# from pygame.color import Color
# from pygame.rect import Rect
# from pygame.surface import Surface
import os

from pygame import *
import ctypes

# некотрые необходимые константы
user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55

PLATFORM_WIDTH = WIN_WIDTH / 48
PLATFORM_HEIGHT = WIN_HEIGHT / 25.25
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами


class Platform(sprite.Sprite):
    def __init__(self, x, y, texture="platform", platform_height=PLATFORM_HEIGHT):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, platform_height))
        self.image = image.load(f"%s/Textures/{texture}.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, platform_height)
