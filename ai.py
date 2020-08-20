import math
import random

PLAYER_PIECE = 1
AI_PIECE = 2

CONNECT_NUM = 4

N_COLS = 7
N_ROWS = 7

WINDOW_LENGTH = 4

def check_win(grid, player):
    """
    Returns true if a winning connection exists in the board,
    false otherwise.
    """
    n_cols = N_COLS
    n_rows = N_ROWS
    connect_num = 4

    # Check horizontal
    for c in range(n_cols - (connect_num - 1)):
        for r in range(n_rows):
            count = 0
            for i in range(connect_num):
                if grid[r][c+i] == player:
                    count += 1
                if count == connect_num:
                    return True

    # Check vertical
    for c in range(n_cols):
        for r in range(n_rows - (connect_num - 1)):
            count = 0
            for i in range(connect_num):
                if grid[r+i][c] == player:
                    count += 1
                if count == connect_num:
                    return True

    # Check left diagonal
    for c in range(n_cols - (connect_num - 1)):
        for r in range(n_rows - (connect_num - 1)):
            count = 0
            for i in range(connect_num):
                if grid[r+i][c+i] == player:
                    count += 1
                if count == connect_num:
                    return True

    # Check right diagonal
    for c in range(n_cols - (connect_num - 1)):
        for r in range((connect_num - 1), n_rows):
            count = 0
            for i in range(connect_num):
                if grid[r-i][c+i] == player:
                    count += 1
                if count == connect_num:
                    return True
    return False

def is_terminal_node(grid):

    return (check_win(grid, PLAYER_PIECE) or
            check_win(grid, AI_PIECE) or
            len(get_valid_locations(grid)) == 0)

def get_valid_locations(grid):
    valid_locations = []
    for col in range(7):
        if is_valid_location(grid, col):
            valid_locations.append(col)
    return valid_locations

def is_valid_location(grid, col):
    return grid[0][col] == 0

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, N_COLS//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(N_ROWS):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(N_COLS-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(N_COLS):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(N_ROWS-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score posiive sloped diagonal
    for r in range(N_ROWS-3):
        for c in range(N_COLS-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score posiive sloped diagonal
    for r in range(N_ROWS-3):
        for c in range(N_COLS-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score

def minimax(grid, depth, alpha, beta, maximizing_player):
    valid_locations = get_valid_locations(grid)
    is_terminal = is_terminal_node(grid)

    if depth == 0 or is_terminal:
        if is_terminal:
            if check_win(grid, AI_PIECE):
                return (None, 100000000000000)
            elif check_win(grid, PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(grid, AI_PIECE))

    if maximizing_player:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(grid, col)
            b_copy = grid.copy()
            b_copy[row][col] = AI_PIECE
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(grid, col)
            b_copy = grid.copy()
            b_copy[row][col] = PLAYER_PIECE
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def best_move(board):
    col, _ = minimax(board.grid, 5, -math.inf, math.inf, True)
    print(col)
    return col


# col, minimax_score = minimax(board, 5, -math.inf, math.inf, True

def get_next_open_row(grid, col):
    """
    Finds the topmost vacant cell in column `col`, in `board`'s grid.
    Returns that cell's corresponding row index.
    """
    n_rows = N_ROWS

    # check row by row, from bottom row to top row ([0][0] is topleft of grid)
    for row in range(n_rows - 1, -1, -1):
        if grid[row][col] == 0:
            return row

    # so pylint doesn't complain
    return None
