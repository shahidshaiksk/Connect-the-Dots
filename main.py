import pygame
import numpy

# initialize pygame
pygame.init()
# create screen
screen = pygame.display.set_mode((800, 640))
# interface
pygame.display.set_caption("Connect the Dots")
icon = pygame.image.load('dots.png')
pygame.display.set_icon(icon)
# matrix size
k = 11
change = 400 // (k - 1)
sensitivity = change // 5
font = pygame.font.Font("freesansbold.ttf", 32)
font1 = pygame.font.Font("freesansbold.ttf", 48)
font2 = pygame.font.Font("freesansbold.ttf", 24)
scores_pos = ((80, 230), (80, 290), (80, 350), (80, 410))


class Data:
    def __init__(self, size, num_of_players):
        self.vertical = numpy.array([[0] * size] * (size - 1))
        self.horizontal = numpy.array([[0] * (size - 1)] * size)
        self.cells = numpy.array([[0] * (size - 1)] * (size - 1))
        self.counter = 0
        self.num_of_players = num_of_players
        self.scores = [0] * num_of_players
        self.playing = 0
        self.player_change = False
        self.colors = ((192, 23, 96), (37, 89, 151), (54, 98, 65), (139, 88, 138))


def play_music():
    pygame.mixer.music.load("music.mp3")
    pygame.mixer.music.play(-1)


def show_scores(data):
    text = font2.render('Scoreboard', True, (117, 34, 34), (250, 237, 205))
    text_rect = text.get_rect()
    text_rect.center = (80, 170)
    screen.blit(text, text_rect)
    for player in list(range(data.num_of_players)):
        text = font.render(str(data.scores[player]), True, data.colors[player], (250, 237, 205))
        text_rect = text.get_rect()
        text_rect.center = scores_pos[player]
        screen.blit(text, text_rect)
    text = font.render('TOP', True, data.colors[data.scores.index(max(data.scores))], (250, 237, 205))
    text_rect = text.get_rect()
    text_rect.center = (720, 270)
    screen.blit(text, text_rect)
    text = font1.render('P' + str(data.scores.index(max(data.scores)) + 1), True,
                        data.colors[data.scores.index(max(data.scores))], (250, 237, 205))
    text_rect = text.get_rect()
    text_rect.center = (720, 320)
    screen.blit(text, text_rect)


def show_current_player(data):
    text = font.render('P' + str(data.playing + 1), True, data.colors[data.playing], (250, 237, 205))
    text_rect = text.get_rect()
    text_rect.center = (400, 60)
    screen.blit(text, text_rect)


def player_change(data):
    data.playing = (data.playing + 1) % data.num_of_players


def check_horizontal(x, y, data):
    data.player_change = True
    if x == 0:
        if check_down(x, y, data):
            data.cells[x, y] = 1
            data.counter += 1
            data.scores[data.playing] += 1
            pygame.draw.rect(screen, data.colors[data.playing], (
                200 + y * change + sensitivity, 120 + x * change + sensitivity, change - 2 * sensitivity,
                change - 2 * sensitivity))
            data.player_change = False
    elif x == k - 1:
        if check_up(x, y, data):
            data.cells[x - 1, y] = 1
            data.counter += 1
            data.scores[data.playing] += 1
            pygame.draw.rect(screen, data.colors[data.playing], (
                200 + y * change + sensitivity, 80 + x * change + sensitivity, change - 2 * sensitivity,
                change - 2 * sensitivity))
            data.player_change = False
    else:
        if check_down(x, y, data):
            data.cells[x, y] = 1
            data.counter += 1
            data.scores[data.playing] += 1
            pygame.draw.rect(screen, data.colors[data.playing], (
                200 + y * change + sensitivity, 120 + x * change + sensitivity, change - 2 * sensitivity,
                change - 2 * sensitivity))
            data.player_change = False
        if check_up(x, y, data):
            data.cells[x - 1, y] = 1
            data.counter += 1
            data.scores[data.playing] += 1
            pygame.draw.rect(screen, data.colors[data.playing], (
                200 + y * change + sensitivity, 80 + x * change + sensitivity, change - 2 * sensitivity,
                change - 2 * sensitivity))
            data.player_change = False
    return data.player_change


def check_vertical(x, y, data):
    data.player_change = True
    if y == 0:
        if check_right(x, y, data):
            data.cells[x, y] = 1
            data.counter += 1
            data.scores[data.playing] += 1
            pygame.draw.rect(screen, data.colors[data.playing], (
                200 + y * change + sensitivity, 120 + x * change + sensitivity, change - 2 * sensitivity,
                change - 2 * sensitivity))
            data.player_change = False
    elif y == k - 1:
        if check_left(x, y, data):
            data.cells[x, y - 1] = 1
            data.counter += 1
            data.scores[data.playing] += 1
            pygame.draw.rect(screen, data.colors[data.playing], (
                160 + y * change + sensitivity, 120 + x * change + sensitivity, change - 2 * sensitivity,
                change - 2 * sensitivity))
            data.player_change = False
    else:
        if check_right(x, y, data):
            data.cells[x, y] = 1
            data.counter += 1
            data.scores[data.playing] += 1
            pygame.draw.rect(screen, data.colors[data.playing], (
                200 + y * change + sensitivity, 120 + x * change + sensitivity, change - 2 * sensitivity,
                change - 2 * sensitivity))
            data.player_change = False
        if check_left(x, y, data):
            data.cells[x, y - 1] = 1
            data.counter += 1
            data.scores[data.playing] += 1
            pygame.draw.rect(screen, data.colors[data.playing], (
                160 + y * change + sensitivity, 120 + x * change + sensitivity, change - 2 * sensitivity,
                change - 2 * sensitivity))
            data.player_change = False
    return data.player_change


def check_down(x, y, data):
    return data.cells[x, y] == 0 and data.horizontal[x + 1, y] and data.vertical[x, y] and data.vertical[x, y + 1]


def check_up(x, y, data):
    return data.cells[x - 1, y] == 0 and data.horizontal[x - 1, y] and data.vertical[x - 1, y] and data.vertical[
        x - 1, y + 1]


def check_right(x, y, data):
    return data.cells[x, y] == 0 and data.vertical[x, y + 1] and data.horizontal[x, y] and data.horizontal[x + 1, y]


def check_left(x, y, data):
    return data.cells[x, y - 1] == 0 and data.vertical[x, y - 1] and data.horizontal[x, y - 1] and data.horizontal[
        x + 1, y - 1]


def click_horizontal(x, y, data):
    if (x - 200) % change <= sensitivity or (x - 200) % change >= change - sensitivity:
        return
    if 120 - sensitivity <= y <= 120 + sensitivity:
        y = 120  # vertical[0]
    elif 520 - sensitivity <= y <= 520 + sensitivity:
        y = 520  # vertical[-1]
    elif 120 + sensitivity < y < 520 - sensitivity:
        if (y - 120) % change <= sensitivity:
            y = 120 % change + y // change * change
        elif (y - 120) % change >= change - sensitivity:
            y = 120 % change + y // change * change + change
        else:
            return
    else:
        return
    if 200 + sensitivity < x < 600 - sensitivity:
        x = x // change * change
    else:
        return
    if data.horizontal[(y - 120) // change, (x - 200) // change] == 0:
        data.horizontal[(y - 120) // change, (x - 200) // change] = 1
        pygame.draw.line(screen, (82, 82, 82), (x, y), (x + change, y), 3)
        # print(x, y, "\n", data.horizontal)
        data.player_change = check_horizontal((y - 120) // change, (x - 200) // change, data)
        if data.player_change:
            player_change(data)
        else:
            # print(data.scores)
            show_scores(data)
    else:
        return


def click_vertical(x, y, data):
    if (y - 120) % change <= sensitivity or (y - 120) % change >= change - sensitivity:
        return
    if 200 - sensitivity <= x <= 200 + sensitivity:
        x = 200  # horizontal[0]
    elif 600 - sensitivity <= x <= 600 + sensitivity:
        x = 600  # horizontal[-1]
    elif 200 + sensitivity < x < 600 - sensitivity:
        if (x - 200) % change <= sensitivity:
            x = 200 % change + x // change * change
        elif (x - 200) % change >= change - sensitivity:
            x = 200 % change + x // change * change + change
        else:
            return
    else:
        return
    if 120 + sensitivity < y < 520 - sensitivity:
        y = y // change * change
    else:
        return
    if data.vertical[(y - 120) // change, (x - 200) // change] == 0:
        data.vertical[(y - 120) // change, (x - 200) // change] = 1
        pygame.draw.line(screen, (82, 82, 82), (x, y), (x, y + change), 3)
        # print(x, y, "\n", data.vertical)
        data.player_change = check_vertical((y - 120) // change, (x - 200) // change, data)
        if data.player_change:
            player_change(data)
        else:
            # print(data.scores)
            show_scores(data)
    else:
        return


def click(data, text_rect):
    left, middle, right = pygame.mouse.get_pressed()
    if left:
        x, y = pygame.mouse.get_pos()
        # print(x,y)
        if text_rect.center[0] - text_rect.width//2 < x < text_rect.center[0] + text_rect.width//2 and text_rect.center[1] - text_rect.height//2 < y < text_rect.center[1] + text_rect.height//2:
            menu()
        elif (y - 120) % change <= sensitivity or (y - 120) % change >= change - sensitivity:
            click_horizontal(x, y, data)
        elif (x - 200) % change <= sensitivity or (x - 200) % change >= change - sensitivity:
            click_vertical(x, y, data)


def draw_structure():
    screen.fill((250, 237, 205))
    text = font2.render(' Main Menu ', True, (250, 237, 205), (117, 34, 34))
    text_rect = text.get_rect()
    text_rect.center = (700, 40)
    screen.blit(text, text_rect)
    for i in range(120, 521, 400 // (k - 1)):
        pygame.draw.line(screen, (200, 200, 200), (200, i), (600, i), 3)
    for i in range(200, 601, 400 // (k - 1)):
        pygame.draw.line(screen, (200, 200, 200), (i, 120), (i, 520), 3)
    for i in range(200, 601, 400 // (k - 1)):
        for j in range(120, 521, 400 // (k - 1)):
            pygame.draw.circle(screen, (45, 45, 45), (i, j), 4, 0)
    return text_rect


def click_in_result(text_rect):
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if text_rect.collidepoint(event.pos):
                        menu()
            pygame.display.update()
            pygame.display.flip()
    except (KeyboardInterrupt, pygame.error):
        pass


def show_result(data):
    text_rect = draw_result(data)
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_in_result(text_rect)
            pygame.display.update()
            pygame.display.flip()
    except (KeyboardInterrupt, pygame.error):
        pass


def draw_result(data):
    screen.fill((250, 237, 205))
    if data.scores.count(max(data.scores)) == 1:
        text = font1.render('Player ' + str(data.scores.index(max(data.scores)) + 1) + ' is winner!', True,
                            data.colors[data.scores.index(max(data.scores))], (250, 237, 205))
        text_rect = text.get_rect()
        text_rect.center = (400, 160)
        screen.blit(text, text_rect)
    else:
        text = font1.render('Match drawn', True, (0, 0, 0), (250, 237, 205))
        text_rect = text.get_rect()
        text_rect.center = (400, 160)
        screen.blit(text, text_rect)
    text = font.render(' Main Menu ', True, (0, 0, 0), (150, 190, 205))
    text_rect2 = text.get_rect()
    text_rect2.center = (400, 480)
    screen.blit(text, text_rect2)
    return text_rect2


def gameplay(data):
    main_menu_button = draw_structure()
    show_scores(data)
    running = True
    try:
        while running:
            show_current_player(data)
            if data.counter == 100:
                running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            click(data, main_menu_button)
            pygame.display.update()
            pygame.display.flip()
            if data.counter == 100:
                running = False
        show_result(data)
    except (pygame.error, KeyboardInterrupt):
        pass


def draw_menu():
    screen.fill((250, 237, 205))
    img = pygame.image.load('Connect the Dots.png').convert_alpha()
    img = pygame.transform.scale(img, (600, 400))
    img_rect = img.get_rect()
    img_rect.center = (400, 100)
    screen.blit(img, img_rect)
    text = font.render(' Play Game ', True, (250, 237, 205), (69, 117, 171))
    text_rect = text.get_rect()
    text_rect.center = (150, 220)
    screen.blit(text, text_rect)
    return text_rect


def click_in_menu(text_rect):
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if text_rect.collidepoint(event.pos):
                        text_rect1, text_rect2, text_rect3 = draw_select_num_of_players()
                        select_num_of_players(text_rect1, text_rect2, text_rect3)
            pygame.display.update()
            pygame.display.flip()
    except (pygame.error, KeyboardInterrupt):
        pass


def draw_select_num_of_players():
    screen.fill((250, 237, 205))
    text = font1.render('Select number of players:', True, (69, 117, 171), (250, 237, 205))
    text_rect = text.get_rect()
    text_rect.center = (400, 280)
    screen.blit(text, text_rect)
    text = font.render(' 2 Players ', True, (250, 237, 205), (69, 117, 171))
    text_rect1 = text.get_rect()
    text_rect1.center = (200, 550)
    screen.blit(text, text_rect1)
    text = font.render(' 3 Players ', True, (250, 237, 205), (69, 117, 171))
    text_rect2 = text.get_rect()
    text_rect2.center = (400, 550)
    screen.blit(text, text_rect2)
    text = font.render(' 4 Players ', True, (250, 237, 205), (69, 117, 171))
    text_rect3 = text.get_rect()
    text_rect3.center = (600, 550)
    screen.blit(text, text_rect3)
    return text_rect1, text_rect2, text_rect3


def select_num_of_players(text_rect1, text_rect2, text_rect3):
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if text_rect1.collidepoint(event.pos):
                        gameplay(Data(k, 2))
                    elif text_rect2.collidepoint(event.pos):
                        gameplay(Data(k, 3))
                    elif text_rect3.collidepoint(event.pos):
                        gameplay(Data(k, 4))
            pygame.display.update()
            pygame.display.flip()
    except (pygame.error, KeyboardInterrupt):
        pass


def menu():
    text_rect = draw_menu()
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
            click_in_menu(text_rect)
            pygame.display.update()
            pygame.display.flip()
    except (pygame.error, KeyboardInterrupt):
        pass


clock = pygame.time.Clock()
clock.tick(60)
play_music()
menu()
