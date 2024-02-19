import pygame
import numpy as np

# Game Setup
pygame.init()
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 5, 5
SQUARE_SIZE = WIDTH // COLS
RED, GREEN, BLUE, WHITE, BLACK = (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (0, 0, 0)

board = np.zeros((ROWS, COLS), dtype=int)
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chain Reaction AI Game")

def draw_orb(win, row, col, color, count):
    radius = SQUARE_SIZE // 4
    border_radius = radius + 2
    offset = radius // 2
    positions = [(0, 0), (-offset, 0), (offset, 0), (0, -offset), (0, offset)]
    
    for i in range(min(count, 5)):
        x_offset, y_offset = positions[i]
        x = col * SQUARE_SIZE + SQUARE_SIZE // 2 + x_offset
        y = row * SQUARE_SIZE + SQUARE_SIZE // 2 + y_offset
        pygame.draw.circle(win, BLACK, (x, y), border_radius)
        pygame.draw.circle(win, color, (x, y), radius)

def draw_board(win, board):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(win, GREEN, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            orb_count = abs(board[row][col])
            if orb_count > 0:
                color = RED if board[row][col] > 0 else GREEN
                draw_orb(win, row, col, color, orb_count)
    pygame.display.update()

def add_orb(board, row, col, player, currentPlayer):
    if board[row][col] == 0 or board[row][col] / currentPlayer > 0:
        board[row][col] += currentPlayer
        check_explosions(board, row, col, currentPlayer)
        return True
    return False

def check_explosions(board, row, col, currentPlayer, exploded=None):
    if exploded is None:
        exploded = set()

    critical_mass = 2 if (row in [0, ROWS-1] and col in [0, COLS-1]) else 3 if row in [0, ROWS-1] or col in [0, COLS-1] else 4

    if (row, col) in exploded:
        return
    
    if abs(board[row][col]) >= critical_mass:
        exploded.add((row, col))
        board[row][col] = 0

        for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            new_row, new_col = row + dx, col + dy
            if 0 <= new_row < ROWS and 0 <= new_col < COLS:
                if board[new_row][new_col] * currentPlayer > 0:
                    board[new_row][new_col] += currentPlayer
                else:
                    board[new_row][new_col] = currentPlayer * (1 if board[new_row][new_col] == 0 else abs(board[new_row][new_col]) + 1)
                check_explosions(board, new_row, new_col, currentPlayer, exploded)

def minimax(board, depth, alpha, beta, maximizingPlayer):
    if depth == 0 or game_over(board):
        return evaluate_board(board)

    if maximizingPlayer:
        maxEval = -float('inf')
        for move in get_all_possible_moves(board, 1):
            new_board = simulate_move(board, move, 1)
            eval = minimax(new_board, depth - 1, alpha, beta, False)
            maxEval = max(maxEval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval
    else:
        minEval = float('inf')
        for move in get_all_possible_moves(board, -1):
            new_board = simulate_move(board, move, -1)
            eval = minimax(new_board, depth - 1, alpha, beta, True)
            minEval = min(minEval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval

def get_all_possible_moves(board, player):
    possible_moves = []
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player or board[row][col] == 0:
                possible_moves.append((row, col))
    return possible_moves

def simulate_move(board, move, player):
    new_board = np.copy(board)
    row, col = move
    add_orb(new_board, row, col, player, player)
    return new_board

def evaluate_board(board):
    player_score = np.sum(board == 1)
    ai_score = np.sum(board == -1)
    return ai_score - player_score  # difference between number of orbs

def game_over(board):
    if np.all(board > 0) or np.all(board < 0):
        return True

    player_moves = get_all_possible_moves(board, 1)
    opponent_moves = get_all_possible_moves(board, -1)
    if not player_moves or not opponent_moves:
        return True
    
    return False

def ai_move(board, player):
    best_score = -float('inf')
    best_move = None
    for move in get_all_possible_moves(board, player):
        new_board = simulate_move(board, move, player)
        score = minimax(new_board, 3, -float('inf'), float('inf'), False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def main():
    currentPlayer = 1
    run = True
    while run:
        draw_board(win, board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if currentPlayer == 1 and event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                col, row = mouseX // SQUARE_SIZE, mouseY // SQUARE_SIZE
                if add_orb(board, row, col, currentPlayer, currentPlayer):
                    currentPlayer = -1

        if currentPlayer == -1:
            ai_result = ai_move(board, -1)
            if ai_result is not None:
                row, col = ai_result
                add_orb(board, row, col, -1, -1)
                currentPlayer = 1

        if game_over(board):
            print("Game Over")
            run = False

        pygame.display.update()
    pygame.quit()

main()
