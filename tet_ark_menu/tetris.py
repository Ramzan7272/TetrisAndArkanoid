import pygame
from copy import deepcopy
from random import choice, randrange

from tet_ark_menu.menu import Menu


def tetris():
    from tet_ark_menu.arkanoid import arkanoid

    w, h = 10, 14
    tile = 45
    game_res = w * tile, h * tile
    res = 750, 670
    fps = 60
    pygame.display.set_caption('Tetris')
    sc = pygame.display.set_mode(res)
    game_sc = pygame.Surface(game_res)
    clock = pygame.time.Clock()
    # создаем поле игры
    grid = [pygame.Rect(x * tile, y * tile, tile, tile) for x in range(w) for y in range(h)]
    # определяем координаты фигур по которым они и будут рисоваться
    figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                   [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                   [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                   [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    figures = [[pygame.Rect(x + w // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
    figure_rect = pygame.Rect(0, 0, tile - 2, tile - 2)
    field = [[0 for i in range(w)] for j in range(h)]

    anim_count, anim_speed, anim_limit = 0, 0, 0
    # звуки
    fig_land_sound = pygame.mixer.Sound('data/sounds/stuk.mp3')
    line_cr_sound = pygame.mixer.Sound('data/sounds/line.mp3')
    game_over_sound = pygame.mixer.Sound('data/sounds/game_over.mp3')
    # картинки
    bg = pygame.image.load('data/img/tetris.jpg').convert()
    game_bg = pygame.image.load('data/img/tetris_game.jpg').convert()
    # шрифты
    main_font = pygame.font.Font('data/font/font.ttf', 65)
    main_font_st = pygame.font.Font('data/font/font.ttf', 35)
    font = pygame.font.Font('data/font/font.ttf', 45)
    pause_f = pygame.font.Font('data/font/font.ttf', 1)
    # надписи в самой игре
    st = main_font_st.render('Press "SPACE to start game"', True, pygame.Color('white'))
    pause = pause_f.render('PAUSE', True, pygame.Color('darkorange'))
    title_tetris = main_font.render('TETRIS', True, pygame.Color('darkorange'))
    title_score = font.render('score:', True, pygame.Color('darkgreen'))
    title_record = font.render('record:', True, pygame.Color('purple'))
    title_line = font.render('line:', True, pygame.Color('darkgrey'))
    # рандомный цвет
    get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))
    # сразу берем по две рандомных фигуры из списка, и два цвета
    figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
    color, next_color = get_color(), get_color()
    # переменные и словари для подсчета результатов
    score, lines, lini = 0, 0, 0
    scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}
    line1 = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
    t_f = False
    start = True
    start_tetris = True
    pause_t_f = False

    # функция для проверки границ игрового поля
    def check_borders():
        if figure[i].x < 0 or figure[i].x > w - 1:
            return False
        elif figure[i].y > h - 1 or field[figure[i].y][figure[i].x]:
            return False
        return True

    # функия для записывания рекорда
    def get_record():
        try:
            with open('record') as f:
                return f.readline()
        except FileNotFoundError:
            with open('record', 'w') as f:
                f.write('0')

    # функия для получения рекорда
    def set_record(record, score):
        rec = max(int(record), score)
        with open('record', 'w') as f:
            f.write(str(rec))

    # доступ к меню
    buttons = [
        {'x': 120, 'y': 240, 'name': 'Tetris', 'color': (250, 250, 30), 'active_color': (0, 100, 200), 'number': 0,
         'func': tetris},
        {'x': 400, 'y': 240, 'name': 'Arkanoid', 'color': (250, 250, 30), 'active_color': (0, 100, 200), 'number': 1,
         'func': arkanoid},
        {'x': 300, 'y': 320, 'name': 'Quit', 'color': (250, 250, 30), 'active_color': (0, 100, 200), 'number': 2}
    ]

    game = Menu(buttons)

    while start_tetris:
        record = get_record()
        dx, rotate = 0, False
        sc.blit(bg, (0, 0))
        sc.blit(game_sc, (20, 20))
        game_sc.blit(game_bg, (0, 0))

        # задержка для собранных линий
        for i in range(lines):
            pygame.time.wait(200)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            # заставка для начала игры, чтоб нужно было нажать пробел
            if start == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        st = pause_f.render('Press "SPACE to start game"', True, pygame.Color('white'))
                        anim_count, anim_speed, anim_limit = 0, 60, 2000
                        t_f = True
                        start = False
                        pause_t_f = True
                    elif event.key == pygame.K_ESCAPE:
                        game.menu()
            # пауза
            if pause_t_f:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if x in range(690, 731) and y in range(80, 121):
                        k = anim_speed
                        anim_speed = 0
                        t_f = False
                        pause = font.render('PAUSE', True, pygame.Color('darkorange'))
                    if x in range(640, 681) and y in range(80, 121) and not t_f:
                        anim_speed = k
                        t_f = True
                        pause = pause_f.render('PAUSE', True, pygame.Color('darkorange'))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.menu()
            # управление фигурами
            if t_f == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_DOWN:
                        anim_limit = 100
                    elif event.key == pygame.K_UP:
                        rotate = True
                    elif event.key == pygame.K_ESCAPE:
                        game.menu()

        # движение по горизонтали
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break

        # по вертикали, ускорение, накладывание фигур друг на друга
        anim_count += anim_speed

        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)

            for i in range(4):
                figure[i].y += 1

                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color

                    fig_land_sound.play()
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break

        # вращение фигур
        center = figure[0]
        figure_old = deepcopy(figure)

        if rotate:
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y

                if not check_borders():
                    figure = deepcopy(figure_old)
                    break

        # убираем собранные линии
        line, lines = h - 1, 0

        for row in range(h - 1, -1, -1):
            count = 0

            for i in range(w):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]

            if count < w:
                line -= 1
            else:
                line_cr_sound.play()
                anim_speed += 3
                lines += 1

        # начисляем счет
        score += scores[lines]
        lini += line1[lines]

        # рисуем сетку
        [pygame.draw.rect(game_sc, (70, 70, 70), i_rect, 1) for i_rect in grid]

        # рисуем сами фигуры
        for i in range(4):
            figure_rect.x = figure[i].x * tile
            figure_rect.y = figure[i].y * tile
            pygame.draw.rect(game_sc, color, figure_rect)

        # отрисовываем фигуры на карте игрового поля, чтоб их было видно
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * tile, y * tile
                    pygame.draw.rect(game_sc, col, figure_rect)

        # рисуем следующую фигуру
        for i in range(4):
            figure_rect.x = next_figure[i].x * tile + 380
            figure_rect.y = next_figure[i].y * tile + 185
            pygame.draw.rect(sc, next_color, figure_rect)

        # рисуем надписи и кнопки паузы
        sc.blit(st, (60, 280))
        sc.blit(pause, (160, 250))
        sc.blit(title_tetris, (485, -20))
        sc.blit(title_score, (500, 320))
        sc.blit(font.render(str(score), True, pygame.Color('white')), (500, 370))
        sc.blit(title_record, (500, 520))
        sc.blit(font.render(record, True, pygame.Color('gold')), (500, 570))
        sc.blit(title_line, (500, 420))
        sc.blit(font.render(str(lini), True, pygame.Color('white')), (500, 470))
        pygame.draw.circle(sc, (255, 0, 0), (710, 100), 20)
        pygame.draw.rect(sc, (0, 0, 0), (700, 90, 8, 20))
        pygame.draw.rect(sc, (0, 0, 0), (713, 90, 8, 20))
        pygame.draw.circle(sc, (0, 255, 0), (660, 100), 20)
        pygame.draw.polygon(sc, (0, 0, 0), [(653, 90), (653, 110), (673, 100)])

        # проигрыш
        for i in range(w):
            if field[0][i]:
                game_over_sound.play()
                set_record(record, score)

                field = [[0 for i in range(w)] for i in range(h)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                k = 60
                score = 0
                lini = 0

                for i_rect in grid:
                    pygame.draw.rect(game_sc, get_color(), i_rect)
                    sc.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(100)

        pygame.display.flip()
        clock.tick(fps)
