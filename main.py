import pygame
from window import Window
print(f"Pygame Version: {pygame.__version__}")

window = Window(1000, 800)
window.main_loop()


#this will probably be the only file I don't change. Debugging is its own program.