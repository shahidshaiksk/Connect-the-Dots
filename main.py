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


class Data:
    def __init__(self, size):
        self.vertical = numpy.array([[0] * size] * (size - 1))
        self.horizontal = numpy.array([[0] * (size - 1)] * size)
        self.cells = numpy.array([[0] * (size - 1)] * (size - 1))
        self.counter = 0
        self.scores = [0]*2
        self.playing = 0
        self.player_change = False
        self.colors = ((192, 23, 96), (37, 89, 151))
        self.font = pygame.font.Font("freesansbold.ttf", 32)


def show_scores(data):
    text = data.font.render(str(data.scores[0]), True, data.colors[0], (250, 237, 205))
    textRect = text.get_rect()
    textRect.center = (80, 320)
    screen.blit(text, textRect)
    text = data.font.render(str(data.scores[1]), True, data.colors[1], (250, 237, 205))
    textRect = text.get_rect()
    textRect.center = (720, 320)
    screen.blit(text, textRect)


def show_current_player(data):
    text = data.font.render("P"+str(data.playing+1), True, data.colors[data.playing], (250, 237, 205))
    text_rect = text.get_rect()
    text_rect.center = (400, 60)
    screen.blit(text, text_rect)


def player_change(data):
    data.playing = (data.playing + 1) % 2


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


def click(data):
    left, middle, right = pygame.mouse.get_pressed()
    if left:
        x, y = pygame.mouse.get_pos()
        # print(x,y)
        if (y - 120) % change <= sensitivity or (y - 120) % change >= change - sensitivity:
            click_horizontal(x, y, data)
        elif (x - 200) % change <= sensitivity or (x - 200) % change >= change - sensitivity:
            click_vertical(x, y, data)


def draw_structure():
    screen.fill((250, 237, 205))
    for i in range(120, 521, 400 // (k - 1)):
        pygame.draw.line(screen, (200, 200, 200), (200, i), (600, i), 3)
    for i in range(200, 601, 400 // (k - 1)):
        pygame.draw.line(screen, (200, 200, 200), (i, 120), (i, 520), 3)
    for i in range(200, 601, 400 // (k - 1)):
        for j in range(120, 521, 400 // (k - 1)):
            pygame.draw.circle(screen, (45, 45, 45), (i, j), 4, 0)


def click_in_result():
    left, middle, right = pygame.mouse.get_pressed()
    if left:
        x, y = pygame.mouse.get_pos()
        if 270 < x < 530 and 455 < y < 505:
            gameplay()


def show_result(data):
    screen.fill((250, 237, 205))
    data.font = pygame.font.Font('freesansbold.ttf', 48)
    running = True
    try:
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if data.scores[0] > data.scores[1]:
                text = data.font.render('Player 1 is winner!', True, data.colors[0], (250, 237, 205))
                text_rect = text.get_rect()
                text_rect.center = (400, 160)
                screen.blit(text, text_rect)
            elif data.scores[1] > data.scores[0]:
                text = data.font.render('Player 2 is winner!', True, data.colors[1], (250, 237, 205))
                text_rect = text.get_rect()
                text_rect.center = (400, 160)
                screen.blit(text, text_rect)
            else:
                text = data.font.render('Match drawn', True, (0, 0, 0), (250, 237, 205))
                text_rect = text.get_rect()
                text_rect.center = (400, 160)
                screen.blit(text, text_rect)
            text = data.font.render('Play Again', True, (0, 0, 0), (150, 190, 205))
            text_rect = text.get_rect()
            text_rect.center = (400, 480)
            screen.blit(text, text_rect)
            click_in_result()
            pygame.display.update()
            pygame.display.flip()
    except (KeyboardInterrupt, pygame.error):
        pass


def gameplay():
    data = Data(k)
    draw_structure()
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
            click(data)
            pygame.display.update()
            pygame.display.flip()
            if data.counter == 100:
                running = False
        show_result(data)
    except (pygame.error, KeyboardInterrupt):
        pass


gameplay()
