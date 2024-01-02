import pygame
import random
import sys

# визначаємо константу затримки кадрів
# та інші константи
FPS = 120

WIDTH_DISPLAY = 500
HEIGHT_DISPLAY = 500

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)
BLUE_COLOR = (0, 0, 255)
ORANGE_COLOR = (255, 150, 100)
RED_COLOR = (190, 37, 37)
BACKGROUND_COLOR = (102, 153, 153)
BACKGROUND_COLOR_FILL = (102, 153, 153, 0)

tank_color = RED_COLOR
enemies_color = ORANGE_COLOR
splach_color = WHITE_COLOR

COORD_X = 50
COORD_Y = 50
WIDTH_RECTANGLE = 30
HEIGHT_RECTANGLE = 30
DELTA_STEP_START = 10
DELTA_TANK_DOWN = 5

TANK_WIDTH = 50
TANK_HEIGHT = 30
TANK_DET_WIDTH = round(50 / 3)
TANK_DET_HEIGHT = round(30 / 3)

ENEMIES_WIDTH = 20
ENEMIES_HEIGHT = 10
SPLACH_RADIUS = 3

splachlist = []
enemieslist = []

# ініціалізація та створення об'єктів
pygame.init()

gameDisplay = pygame.display.set_mode((WIDTH_DISPLAY, HEIGHT_DISPLAY))

pygame.display.set_caption("SPACE WARRIORS")

clock = pygame.time.Clock()

pygame.font.init()
font36Arial = pygame.font.SysFont("Arial", 36)
title_font = pygame.font.SysFont("Arial", 40)

gameOver = False
gameScore = 0
gameScoreWin = 100

def show_level_selection_menu():
    levels = [{"name": "Super Easy",    "difficulty": 1},
              {"name": "Easy",          "difficulty": 2},
              {"name": "Medium",        "difficulty": 3},
              {"name": "Hard",          "difficulty": 4},
              {"name": "Very Hard",     "difficulty": 5}]

    # Очистити екран
    gameDisplay.fill(BLACK_COLOR)

    # Відобразити заголовок
    title = title_font.render("SELECT LEVEL", True, WHITE_COLOR)
    gameDisplay.blit(title, (150, 100))

    # Відобразити рівні
    for i, level in enumerate(levels):
        level_font = pygame.font.SysFont("Arial", 20)
        level_text = level_font.render(level['name'], True, WHITE_COLOR)
        gameDisplay.blit(level_text, (100, 200 + i * 50))

    # Оновити дисплей
    pygame.display.update()

    while True:
        # Обробити події
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Обробити натискання миші
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Визначити, який рівень вибрав гравець
                for i, level in enumerate(levels):
                    if (pygame.mouse.get_pos()[0] > 100 and pygame.mouse.get_pos()[0] < 500
                            and pygame.mouse.get_pos()[1] > 200 + i * 50
                                and pygame.mouse.get_pos()[1] < 250 + i * 50):
                        return level['difficulty']


def show_start_instruction():
    lenrange = 3
    for i in range(lenrange):
        numberrestart = 3 - i
        gameDisplay.fill(BACKGROUND_COLOR)
        pygame.display.update()

        instructiontext = font36Arial.render('USE KEYS: LEFT, RIGHT, SPACE', True, BLUE_COLOR)
        gameDisplay.blit(instructiontext, (30, 100))
        instructiontext = font36Arial.render('ENTER - CHOOSE LEVEL', True, BLUE_COLOR)
        gameDisplay.blit(instructiontext, (60, 150))

        newgametext = font36Arial.render(str(numberrestart), True, BLUE_COLOR)
        gameDisplay.blit(newgametext, (250, 200))
        pygame.display.update()
        pygame.time.delay(1000)


def play_game(level):

    totalRun = 0
    POSITION_X_DELTA = 0

    gameOver = False
    gameScore = 0
    totalStep = 1

    match level:
        case 1:
            totalStep = 25
            SPLACH_LIMIT = 10
        case 2:
            totalStep = 15
            SPLACH_LIMIT = 15
        case 3:
            totalStep = 10
            SPLACH_LIMIT = 20
        case 4:
            totalStep = 5
            SPLACH_LIMIT = 25
        case 5:
            totalStep = 2
            SPLACH_LIMIT = 50

    while True:
        totalRun += 1

        pygame.time.delay(30)

        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #####################--GAMEOVER--#######################
        if gameOver:

            # Згенерувати текст
            textGM = font36Arial.render("GAME OVER!", True, BLUE_COLOR)
            textRS = font36Arial.render("PRESS ENTER TO RESTART", True, BLUE_COLOR)

            # Відобразити текст на екрані
            gameDisplay.blit(textGM, (150, 200))
            gameDisplay.blit(textRS, (50, 250))
            pygame.display.update()

            pressed_continiue = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pressed_continiue = True

            if pressed_continiue or keys[pygame.K_KP_ENTER]:
                gameOver = False
                gameDisplay.fill(BACKGROUND_COLOR, (0, 200, 500, 200))
                pygame.display.update()

                newgametext = font36Arial.render("NEW GAME BEGIN!", True, BLUE_COLOR)
                gameDisplay.blit(newgametext, (100, 200))
                pygame.display.update()
                pygame.time.delay(1000)

                start_game(level)
            continue

        #####################--ITERATION--#######################

        for each in splachlist:
            # splach_x, splach_y = each.get('x'), each.get('y')
            each['y'] -= 5

        if totalRun % totalStep == 0:
            for each in enemieslist:
                # enemies_x, enemies_y = each.get('x'), each.get('y')
                each['y'] += 5

        #####################--KEY--#######################

        choose_level = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                choose_level = True

        if choose_level or keys[pygame.K_KP_ENTER]:
            start_game()

        DELTA_STEP = DELTA_STEP_START
        if keys[pygame.K_LEFT]:
            # if POSITION_X_DELTA + DELTA_STEP >= -WIDTH_DISPLAY/2 + TANK_WIDTH:
            if POSITION_X_DELTA >= -WIDTH_DISPLAY / 2 + TANK_WIDTH / 2:
                POSITION_X_DELTA -= DELTA_STEP

        if keys[pygame.K_RIGHT]:
            if POSITION_X_DELTA + DELTA_STEP_START <= WIDTH_DISPLAY / 2 - TANK_WIDTH / 2:
                POSITION_X_DELTA += DELTA_STEP

        if keys[pygame.K_SPACE]:
            if len(splachlist) < SPLACH_LIMIT:
                splashNew = {'x': POSITION_X_DELTA + WIDTH_DISPLAY / 2, 'y': HEIGHT_DISPLAY - TANK_HEIGHT - TANK_DET_HEIGHT}
                splachlist.append(splashNew)

        if totalRun % totalStep == 0:
            enemiesPosition = random.randint(int(TANK_WIDTH), WIDTH_DISPLAY - TANK_WIDTH)
            enemiesNew = {'x': enemiesPosition, 'y': 0}
            enemieslist.append(enemiesNew)

        gameDisplay.fill((BACKGROUND_COLOR))

        # MOVE TANK
        tankP_LH = (
            WIDTH_DISPLAY / 2 - TANK_WIDTH / 2 + POSITION_X_DELTA,
            HEIGHT_DISPLAY - TANK_HEIGHT - DELTA_TANK_DOWN)  # лівий верх
        tankP_LH2 = (WIDTH_DISPLAY / 2 - TANK_DET_WIDTH / 2 + POSITION_X_DELTA,
                     HEIGHT_DISPLAY - TANK_HEIGHT - DELTA_TANK_DOWN)  # основа дула
        tankP_H1 = (WIDTH_DISPLAY / 2 - TANK_DET_WIDTH / 2 + POSITION_X_DELTA,
                    HEIGHT_DISPLAY - TANK_HEIGHT - DELTA_TANK_DOWN - TANK_DET_HEIGHT)  # лівий край дула
        tankP_H2 = (WIDTH_DISPLAY / 2 + TANK_DET_WIDTH / 2 + POSITION_X_DELTA,
                    HEIGHT_DISPLAY - TANK_HEIGHT - DELTA_TANK_DOWN - TANK_DET_HEIGHT)  # правий край дула
        tankP_RH2 = (WIDTH_DISPLAY / 2 + TANK_DET_WIDTH / 2 + POSITION_X_DELTA,
                     HEIGHT_DISPLAY - TANK_HEIGHT - DELTA_TANK_DOWN)  # права основа дула
        tankP_RH = (WIDTH_DISPLAY / 2 + TANK_WIDTH / 2 + POSITION_X_DELTA,
                    HEIGHT_DISPLAY - TANK_HEIGHT - DELTA_TANK_DOWN)  # правий верх
        tankP_RD = (WIDTH_DISPLAY / 2 + TANK_WIDTH / 2 + POSITION_X_DELTA, HEIGHT_DISPLAY - DELTA_TANK_DOWN)  # правий низ
        tankP_LD = (WIDTH_DISPLAY / 2 - TANK_WIDTH / 2 + POSITION_X_DELTA, HEIGHT_DISPLAY - DELTA_TANK_DOWN)  # лівий низ

        tank_points = [tankP_LH, tankP_LH2, tankP_H1, tankP_H2, tankP_RH2, tankP_RH, tankP_RD, tankP_LD]
        pygame.draw.polygon(gameDisplay, tank_color, tank_points)

        # MOVE SPLACH
        for each in splachlist:
            splach_x, splach_y = each.get('x'), each.get('y')
            pygame.draw.circle(gameDisplay, splach_color, (splach_x, splach_y), SPLACH_RADIUS)

        # MOVE ENEMIES
        for i_enemies in enemieslist:
            enemies_x, enemies_y = i_enemies.get('x'), i_enemies.get('y')
            pygame.draw.rect(gameDisplay, enemies_color, [enemies_x, enemies_y, ENEMIES_WIDTH, ENEMIES_HEIGHT])

            if enemies_y >= HEIGHT_DISPLAY - TANK_HEIGHT:
                gameOver = True
                break

            # SHOOT
            enemies = pygame.Rect(enemies_x, enemies_y, ENEMIES_WIDTH, ENEMIES_HEIGHT)
            for i_splach in splachlist:
                splach = pygame.Rect(i_splach['x'] - SPLACH_RADIUS, i_splach['y'] - SPLACH_RADIUS, SPLACH_RADIUS * 2,
                                     SPLACH_RADIUS * 2)
                if enemies.colliderect(splach):
                    try:
                        enemieslist.remove(i_enemies)
                        splachlist.remove(i_splach)
                        gameScore += 1
                    except:
                        pass
                else:
                    if i_splach['y'] < 0:
                        splachlist.remove(i_splach)

        # SCORE
        font14Arial = pygame.font.SysFont("Arial", 14)
        scoretext = font14Arial.render("Score:", True, BLUE_COLOR)
        gameDisplay.blit(scoretext, (2, 10))
        scoretext = font14Arial.render(str(gameScore), True, BLUE_COLOR)
        gameDisplay.blit(scoretext, (2, 30))

        if gameScore > gameScoreWin:
            textWIN = font36Arial.render("YOU WIN", True, BLUE_COLOR)

            gameScore = 0

            # Відобразити текст на екрані
            gameDisplay.blit(textWIN, (150, 200))
            pygame.display.update()
            pygame.time.delay(2000)

            start_game()

        pygame.display.update()
        clock.tick(FPS)


def start_game(level=None):

    enemieslist.clear()
    splachlist.clear()

    if level == None:
        level = show_level_selection_menu()

    show_start_instruction()
    play_game(level)

start_game()
