import pygame
from random import randrange

from tet_ark_menu.menu import Menu


def arkanoid():
    from tet_ark_menu.tetris import tetris

    width, height = 750, 670
    fps = 60
    start_arkanoid = True
    lose = False
    start = True
    lose_p = True
    pygame.display.set_caption('Arkanoid')

    # рисуем платформу
    platform_w = 230
    platform_h = 35
    platform_speed = 15
    x = width // 2 - platform_w // 2
    platform = pygame.Rect(x, height - platform_h - 10, platform_w, platform_h)

    # рисуем шарик
    ball_radius = 20
    ball_speed = 5
    ball_rect = int(ball_radius * 2 ** 0.5)
    ball = pygame.Rect(randrange(ball_rect, width - ball_rect), height // 2, ball_rect, ball_rect)
    dx, dy = 1, -1

    # заполнеям список с блоками нужным количеством блоков, делаем рандомные цвета
    block_list = [pygame.Rect(20 + 120 * i, 10 + 70 * j, 100, 50) for i in range(6) for j in range(4)]
    color_list = [(randrange(30, 256), randrange(30, 256), randrange(30, 256)) for i in range(6) for j in range(4)]

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    # шрифт, звуки, картинки, надписи
    main_font_st = pygame.font.Font('data/font/font.ttf', 35)
    st = main_font_st.render('Press "SPACE to restart game"', True, pygame.Color('white'))
    img = pygame.image.load('data/img/arkonoid_game.jpg').convert()
    lose_sound = pygame.mixer.Sound('data/sounds/lose.mp3')
    win_sound = pygame.mixer.Sound('data/sounds/win.mp3')
    blocks = pygame.mixer.Sound('data/sounds/block.mp3')

    # делаем доступ к меню
    buttons = [
        {'x': 120, 'y': 240, 'name': 'Tetris', 'color': (250, 250, 30), 'active_color': (0, 100, 200), 'number': 0,
         'func': tetris},
        {'x': 400, 'y': 240, 'name': 'Arkanoid', 'color': (250, 250, 30), 'active_color': (0, 100, 200), 'number': 1,
         'func': arkanoid},
        {'x': 300, 'y': 320, 'name': 'Quit', 'color': (250, 250, 30), 'active_color': (0, 100, 200), 'number': 2}
    ]

    game = Menu(buttons)

    # функция для обнаружения столкновений
    def detect_collision(dx, dy, ball, rect):
        if dx > 0:
            delta_x = ball.right - rect.left
        else:
            delta_x = rect.right - ball.left
        if dy > 0:
            delta_y = ball.bottom - rect.top
        else:
            delta_y = rect.bottom - ball.top

        if abs(delta_x - delta_y) < 10:
            dx, dy = -dx, -dy
        elif delta_x > delta_y:
            dy = -dy
        elif delta_y > delta_x:
            dx = -dx
        return dx, dy

    while start_arkanoid:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        screen.blit(img, (0, 0))

        # отрисовываем шарик, платформу, блоки
        [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate(block_list)]
        pygame.draw.rect(screen, pygame.Color('darkorange'), platform)
        pygame.draw.circle(screen, pygame.Color('white'), ball.center, ball_radius)

        # движение шарика
        ball.x += ball_speed * dx
        ball.y += ball_speed * dy

        # столкновения с левой/правой стороной
        if ball.centerx < ball_radius or ball.centerx > width - ball_radius:
            dx = -dx

        # столкновения с потолком
        if ball.centery < ball_radius:
            dy = -dy

        # столкновения с платформой
        if ball.colliderect(platform) and dy > 0:
            dx, dy = detect_collision(dx, dy, ball, platform)

        # столкновения с блоками
        hit_index = ball.collidelist(block_list)
        if hit_index != -1:
            hit_rect = block_list.pop(hit_index)
            hit_color = color_list.pop(hit_index)
            dx, dy = detect_collision(dx, dy, ball, hit_rect)
            # чтобы когда шарик попадал по блоку, создавался эффект что он взрывается
            hit_rect.inflate_ip(ball.width * 1.5, ball.height * 1.5)
            pygame.draw.rect(screen, hit_color, hit_rect)
            # уменьшаем платформу
            platform_w -= 5
            platform = pygame.Rect(x, height - platform_h - 10, platform_w, platform_h)
            x += 2.5
            # воспроизводим звук и ускоряем шарик
            blocks.play()
            fps += 2

        # проигрыш
        if ball.bottom > height:
            ball_speed = 0
            lose = True
            if lose_p:
                lose_sound.play()
                lose_p = False
            if lose:
                screen.blit(st, (60, 280))
                key = pygame.key.get_pressed()

                if key[pygame.K_SPACE]:
                    lose_sound.stop()
                    arkanoid()

                if key[pygame.K_ESCAPE]:
                    lose_sound.stop()
                    game.menu()
        # победа
        elif not len(block_list):
            y = -670
            image = pygame.image.load("data/img/you_won.png")
            win_sound.play()
            while True:
                clock.tick(60)
                for i in pygame.event.get():
                    if i.type == pygame.QUIT:
                        exit()
                if y < 0:
                    y += 5
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    game.menu()
                if key[pygame.K_SPACE]:
                    arkanoid()
                screen.blit(image, (0, y))
                pygame.display.update()

        # управление платформой
        key = pygame.key.get_pressed()
        if lose_p:
            if key[pygame.K_LEFT] and platform.left > 0:
                platform.left -= platform_speed
                x -= platform_speed

            if key[pygame.K_RIGHT] and platform.right < width:
                platform.right += platform_speed
                x += platform_speed

            if key[pygame.K_ESCAPE]:
                game.menu()

        pygame.display.flip()
        clock.tick(fps)
