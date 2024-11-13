# Python 3

from queue import PriorityQueue
from generate_start_state import generate_shuffled_board, get_solved_board

SIZE = 20


class PuzzleState:
    def __init__(self, board, g=0, h=0, parent=None):
        self.board = board
        self.g = g  # current cost
        self.h = h  # heuristic estimate to the goal
        self.f = g + h  # total estimated cost
        self.parent = parent  # for backtracking solution

    def __lt__(self, other):
        return self.f < other.f


def get_elem_idxs(goal, elem):
    n = len(goal)
    if not 0 <= elem < n * n:
        raise ValueError(f"Elem has to be in range(0,{n*n-1}) inclusive, got {elem}")
    for x in range(n):
        for y in range(n):
            if goal[x][y] == elem:
                return x, y


def manhattan_distance(state, goal):
    n = len(goal)
    distance = 0
    for i in range(n):
        for j in range(n):
            tile = state[i][j]
            if tile != 0:
                goal_x, goal_y = get_elem_idxs(goal, tile)
                distance += abs(goal_x - i) + abs(goal_y - j)
    return distance


def get_neighbors(state):
    n = len(state.board)
    neighbors = []
    blank_x, blank_y = get_elem_idxs(state.board, 0)

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for move in moves:
        new_x, new_y = blank_x + move[0], blank_y + move[1]
        if 0 <= new_x < n and 0 <= new_y < n:
            new_board = [row[:] for row in state.board]
            new_board[blank_x][blank_y], new_board[new_x][new_y] = (
                new_board[new_x][new_y],
                new_board[blank_x][blank_y],
            )
            neighbors.append(PuzzleState(new_board, g=state.g + 1, parent=state))
    return neighbors


def a_star(start, goal):
    open_list = PriorityQueue()
    start_state = PuzzleState(start, g=0, h=manhattan_distance(start, goal))
    open_list.put((start_state.f, start_state))
    visited = set()

    while not open_list.empty():
        current_f, current = open_list.get()
        print(current_f)
        visited.add(tuple(map(tuple, current.board)))

        if current.board == goal:
            return reconstruct_path(current)

        for neighbor in get_neighbors(current):
            if tuple(map(tuple, neighbor.board)) not in visited:
                neighbor.h = manhattan_distance(neighbor.board, goal)
                neighbor.f = neighbor.g + neighbor.h
                open_list.put((neighbor.f, neighbor))
    return None


def reconstruct_path(state):
    path = []
    while state:
        path.append(state.board)
        state = state.parent
    return path[::-1]


def main():
    # goal_state = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]
    # start_state = [[1, 2, 3, 4], [5, 0, 6, 8], [9, 10, 7, 12], [13, 14, 11, 15]]
    # start_state = [[1, 3, 4, 8], [2, 9, 6, 12], [0, 14, 10, 7], [5, 13, 11, 15]]

    goal_state = get_solved_board(SIZE)
    start_state = generate_shuffled_board(100, SIZE)

    # goal_state = [
    #     [1,2,3],
    #     [4,5,6],
    #     [7,8,0]
    # ]
    # start_state = [
    #     [1,2,3],
    #     [4,5,0],
    #     [7,8,6]
    # ]

    path = a_star(start_state, goal_state)

    if path:
        for step in path:
            for row in step:
                print(row)
            print("-----")
        print(f"This took {len(path)-1} moves to solve")
    else:
        print("No solution found.")

    # REQUIRES PYGAME
    from visualizer import run_visualizer

    run_visualizer(path, "base.JPG")
    # run_visualizer(path, "base04.png")
    # run_visualizer(path, "base12.png")


if __name__ == "__main__":
    main()
