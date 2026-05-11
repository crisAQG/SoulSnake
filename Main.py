import sys
import pygame

from Data.Modules.Window import Window


if __name__ == '__main__':
    w = Window()
    w.loop()
    pygame.quit()
    sys.exit()