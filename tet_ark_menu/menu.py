import pygame
import random
import sys

# окно
window = pygame.display.set_mode((750, 670))

# холст
screen = pygame.Surface((750, 670))


# меню
class Menu:
    def __init__(self, buttons):
        self.buttons = buttons

    def render(self, screen, font, num_button):
        for button in self.buttons:
            if num_button == button['number']:
                screen.blit(font.render(button['name'], 1, button['active_color']), (button['x'], button['y'] - 30))
            else:
                screen.blit(font.render(button['name'], 1, button['color']), (button['x'], button['y'] - 30))

    def menu(self):
        done = True
        pygame.display.set_caption('Menu')
        pygame.mouse.set_visible(True)
        pygame.key.set_repeat(0, 0)

        font_menu = pygame.font.Font('data/font/font.ttf', 50)
        button = 0

        while done:
            screen.fill((0, 0, 0))

            mp = pygame.mouse.get_pos()

            for i in self.buttons:
                if i['x'] < mp[0] < i['x'] + 100 and i['y'] < mp[1] < i['y'] + 100:
                    button = i['number']

            self.render(screen, font_menu, button)
            # управление кнопками и мышью
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        if button == 0:
                            done = False
                            done = False
                            func = [but for but in self.buttons if but['number'] == button][0].get('func')

                            if func:
                                func()
                        if button == 1:
                            done = False
                            func = [but for but in self.buttons if but['number'] == button][0].get('func')

                            if func:
                                func()

                        if button == 2:
                            sys.exit()

                    if e.key == pygame.K_ESCAPE:
                        sys.exit()
                    if e.key == pygame.K_UP:
                        if button == 2:
                            button -= 1
                    if e.key == pygame.K_DOWN:
                        if button == 0:
                            button += 2
                        elif button == 1:
                            button += 1
                    if e.key == pygame.K_RIGHT:
                        if button == 0:
                            button += 1
                    if e.key == pygame.K_LEFT:
                        if button == 1:
                            button -= 1

                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if button == 0:
                        done = False
                        func = [but for but in self.buttons if but['number'] == button][0].get('func')

                        if func:
                            func()

                    if button == 1:
                        done = False
                        func = [but for but in self.buttons if but['number'] == button][0].get('func')

                        if func:
                            func()

                    if button == 2:
                        sys.exit()

            for i in range(100):
                pygame.draw.rect(screen, (255, 255, 0), (random.random() * 750, random.random() * 670, 2, 2), 1)

            window.blit(screen, (0, 0))
            pygame.display.update()
