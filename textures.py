# from pygame import sprite
# from pygame.color import Color
# from pygame.rect import Rect
# from pygame.surface import Surface
import os
from pygame import *
import ctypes

# Объявляем переменные
user32 = ctypes.windll.user32
WIN_WIDTH = user32.GetSystemMetrics(0)
WIN_HEIGHT = user32.GetSystemMetrics(1) - 55

PLATFORM_WIDTH = WIN_WIDTH / 48
PLATFORM_HEIGHT = WIN_HEIGHT / 25.25
PLATFORM_COLOR = "#FF6262"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("%s/Textures/platform.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Level_exit(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image = image.load("%s/Textures/exit_door.png" % ICON_DIR)
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


# class Gallery_feature(sprite.Sprite):
#     def __init__(self, x, y, feature_image):
#         sprite.Sprite.__init__(self)
#         self.image = Surface(PLATFORM_WIDTH, PLATFORM_HEIGHT)
#         self.image = image.load(f"%s/Textures/{feature_image}.png" % ICON_DIR)
#         self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
