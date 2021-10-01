import sys
import numpy as np
import pygame

# Anand Thakur
# 10/1/2021

# Always Initialise pygame
pygame.init()

# Constants for Dimensions
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROW = 3
BOARD_COLS = 3
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

# Color (RGB)
WHITE = (255, 255, 255)
BG_COLOR = (27, 18, 18)
CIRCLE_COLOR = (255, 255, 0)
CROSS_COLOR = (255, 0, 0)
# Making a screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Title
pygame.display.set_caption("TIC TAC TOE")

# Add colors
screen.fill(BG_COLOR)

# Board
board = np.zeros((BOARD_ROW, BOARD_COLS))


# Adding Lines
def draw_lines():
    # 1st Horizontal line
    pygame.draw.line(screen, WHITE, (0, 200), (600, 200), LINE_WIDTH)
    # 2nd Horizontal Line
    pygame.draw.line(screen, WHITE, (0, 400), (600, 400), LINE_WIDTH)

    # 1st Vertical Line
    pygame.draw.line(screen, WHITE, (200, 0), (200, 600), LINE_WIDTH)
    # 2nd Vertical Line
    pygame.draw.line(screen, WHITE, (400, 0), (400, 600), LINE_WIDTH)


# Draw X and O
def draw_figures(i, j):
    if board[i][j] == 1:
        # Drawing CIRCLE
        pygame.draw.circle(screen, CIRCLE_COLOR, (int(j * 200 + 100), int(i * 200 + 100)), CIRCLE_RADIUS,
                           CIRCLE_WIDTH)
    elif board[i][j] == 2:
        # Drawing CROSS
        pygame.draw.line(screen, CROSS_COLOR, (j * 200 + SPACE, i * 200 + 200 - SPACE),
                         (j * 200 + 200 - SPACE, i * 200 + SPACE), CROSS_WIDTH)
        pygame.draw.line(screen, CROSS_COLOR, (j * 200 + SPACE, i * 200 + SPACE),
                         (j * 200 + 200 - SPACE, i * 200 + 200 - SPACE), CROSS_WIDTH)


# Mark the square as per requirement
def mark_square(row, col, play):
    board[row][col] = play
    draw_figures(row, col)


# Check availability of slots
def available_square(row, col):
    return board[row][col] == 0


# Return True if full else False
def is_board_full():
    for i in range(BOARD_ROW):
        for j in range(BOARD_COLS):
            if board[i][j] == 0:
                return False
    return True


# Check Winner
def check_win(players):
    win = False
    # vertical win check
    for col in range(BOARD_COLS):
        if board[0][col] == players and board[1][col] == players and board[2][col] == players:
            draw_vertical_winning_line(col, players)
            win = True

    # Horizontal win check
    for row in range(BOARD_ROW):
        if board[row][0] == players and board[row][1] == players and board[row][2] == players:
            draw_horizontal_winning_line(row, players)
            win = True

    # asc diagonal win check
    if board[2][0] == players and board[1][1] == players and board[0][2] == players:
        draw_asc_diagonal(players)
        win = True

    # asc diagonal win check
    if board[0][0] == players and board[1][1] == players and board[2][2] == players:
        draw_desc_diagonal(players)
        win = True
    return win


# Draw winning shapes
def draw_vertical_winning_line(col, players):
    pos_x = col * 200 + 100

    if players == 1:
        color = CIRCLE_COLOR
    else:
        color = CROSS_COLOR

    pygame.draw.line(screen, color, (pos_x, 15), (pos_x, HEIGHT - 15), 15)


def draw_horizontal_winning_line(row, players):
    pos_y = row * 200 + 100
    color = CROSS_COLOR
    if players == 1:
        color = CIRCLE_COLOR

    pygame.draw.line(screen, color, (15, pos_y), (WIDTH - 15, pos_y), 15)


def draw_asc_diagonal(players):
    color = CIRCLE_COLOR
    if players == 2:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), 15)


def draw_desc_diagonal(players):
    color = CIRCLE_COLOR
    if players == 2:
        color = CROSS_COLOR
    pygame.draw.line(screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), 15)


# Restart the game
def restart():
    screen.fill(BG_COLOR)
    draw_lines()
    global game_status
    game_status = False
    global player
    player = 1
    for row in range(BOARD_ROW):
        for col in range(BOARD_COLS):
            board[row][col] = 0


draw_lines()
# Giving player 1 chance first
player = 1
# Status of game
game_status = False
# mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_status:
            # Capture Click
            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            # Determine Row and Columns
            clicked_row = int(mouseY // 200)
            clicked_col = int(mouseX // 200)

            # Check and store info on board
            if available_square(clicked_row, clicked_col):
                if player == 1:
                    mark_square(clicked_row, clicked_col, 1)
                    game_status = check_win(player)
                    player = 2

                elif player == 2:
                    mark_square(clicked_row, clicked_col, 2)
                    game_status = check_win(player)
                    player = 1
        # Press r to restart
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
    pygame.display.update()
