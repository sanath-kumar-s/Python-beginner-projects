import pygame
import sys
import json
import os

pygame.init()

# Screen
WIDTH, HEIGHT = 600, 650
CELL_SIZE = WIDTH // 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Font
font = pygame.font.SysFont(None, 40)

# Load images
board_img = pygame.image.load("Tick-Tack-Toe/assets/board.jpg")
x_img = pygame.image.load("Tick-Tack-Toe/assets/X.png")
o_img = pygame.image.load("Tick-Tack-Toe/assets/O.png")

board_img = pygame.transform.scale(board_img, (WIDTH, WIDTH))
x_img = pygame.transform.scale(x_img, (150, 150))
o_img = pygame.transform.scale(o_img, (150, 150))

# Load / Create scores
SCORE_FILE = "Tick-Tack-Toe/scores.json"

if not os.path.exists(SCORE_FILE):
    with open(SCORE_FILE, "w") as f:
        json.dump({"X": 0, "O": 0}, f)

with open(SCORE_FILE, "r") as f:
    scores = json.load(f)

# Game state
board = [[None]*3 for _ in range(3)]
player = "X"
game_over = False
winner = None

def draw():
    screen.fill((255, 255, 255))
    screen.blit(board_img, (0, 0))

    # Draw moves
    for r in range(3):
        for c in range(3):
            if board[r][c] == "X":
                screen.blit(x_img, (c * CELL_SIZE + 25, r * CELL_SIZE + 25))
            elif board[r][c] == "O":
                screen.blit(o_img, (c * CELL_SIZE + 25, r * CELL_SIZE + 25))

    # UI Text
    if not game_over:
        turn_text = font.render(f"Turn: {player}", True, (0,0,0))
    else:
        if winner == "Draw":
            turn_text = font.render("Draw!", True, (0,0,0))
        else:
            turn_text = font.render(f"{winner} Wins!", True, (0,0,0))

    score_text = font.render(f"X: {scores['X']}   O: {scores['O']}", True, (0,0,0))

    screen.blit(turn_text, (20, WIDTH + 10))
    screen.blit(score_text, (350, WIDTH + 10))

def check_winner():
    # Rows & cols
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0]:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i]:
            return board[0][i]

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0]:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2]:
        return board[0][2]

    # Draw
    if all(all(cell is not None for cell in row) for row in board):
        return "Draw"

    return None

def save_scores():
    with open(SCORE_FILE, "w") as f:
        json.dump(scores, f)

def reset():
    global board, player, game_over, winner
    pygame.time.wait(1500)
    board = [[None]*3 for _ in range(3)]
    player = "X"
    game_over = False
    winner = None

# Main loop
while True:
    draw()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_scores()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos

            if y < WIDTH:
                row = y // CELL_SIZE
                col = x // CELL_SIZE

                if board[row][col] is None:
                    board[row][col] = player

                    # SWITCH PLAYER AFTER MOVE
                    player = "O" if player == "X" else "X"

                    # NOW check winner AFTER move is placed
                    winner = check_winner()

                    if winner:
                        game_over = True
                        if winner in scores:
                            scores[winner] += 1
                            save_scores()

    if game_over:
        reset()