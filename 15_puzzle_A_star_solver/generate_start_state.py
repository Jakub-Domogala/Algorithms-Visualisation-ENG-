import random

MOVES = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


def find_blank(board, n=4):
    for i in range(n):
        for j in range(n):
            if board[i][j] == 0:
                return i, j


def is_valid_move(blank_row, blank_col, move, n=4):
    new_row = blank_row + move[0]
    new_col = blank_col + move[1]
    return 0 <= new_row < n and 0 <= new_col < n


def make_move(board, blank_pos, move):
    blank_row, blank_col = blank_pos
    new_row = blank_row + move[0]
    new_col = blank_col + move[1]

    board[blank_row][blank_col], board[new_row][new_col] = (
        board[new_row][new_col],
        board[blank_row][blank_col],
    )

    new_blank = (new_row, new_col)
    return new_blank


def get_solved_board(resolution=4):
    board = [
        [x + 1 + y * resolution for x in range(resolution)] for y in range(resolution)
    ]
    board[-1][-1] = 0
    return board


def generate_shuffled_board(n_moves=10, resolution=4):
    board = get_solved_board(resolution)
    blank_pos = find_blank(board, resolution)

    move = random.choice(list(MOVES.values()))
    for _ in range(n_moves):
        prev_move = move
        while (not is_valid_move(blank_pos[0], blank_pos[1], move, resolution)) or (
            move == prev_move
        ):
            move = random.choice(list(MOVES.values()))
        blank_pos = make_move(board, blank_pos, move)
    return board
