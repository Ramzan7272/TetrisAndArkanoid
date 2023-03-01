import pygame

from tet_ark_menu.arkanoid import arkanoid
from tet_ark_menu.menu import Menu
from tet_ark_menu.tetris import tetris

pygame.init()

buttons = [{'x': 120, 'y': 240, 'name': 'Tetris', 'color': (250, 250, 30), 'active_color': (0, 100, 200), 'number': 0,
            'func': tetris},
           {'x': 400, 'y': 240, 'name': 'Arkanoid', 'color': (250, 250, 30), 'active_color': (0, 100, 200), 'number': 1,
            'func': arkanoid},
           {'x': 300, 'y': 320, 'name': 'Quit', 'color': (250, 250, 30), 'active_color': (0, 100, 200), 'number': 2}
           ]

game = Menu(buttons)
game.menu()
