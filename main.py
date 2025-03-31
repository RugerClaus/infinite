import pygame
from window import Window
print(f"Pygame Version: {pygame.__version__}")

window = Window(1000, 800)
window.main_loop()
