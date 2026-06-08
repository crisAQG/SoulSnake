import sys
import pygame

from G5.Data.Modules.Window import Window


if __name__ == '__main__':
    w = Window()
    w.loop()
    pygame.quit()
    sys.exit()