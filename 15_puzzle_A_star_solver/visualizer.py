import pygame
import sys


def smoothing_func(x):  # map linear[0,1] -> smoothed[0,1]
    return 4 * x**3 if x < 0.5 else 1 - ((-2 * x + 2) ** 3) / 2


def load_and_slice_image(image_path, n):
    image = pygame.image.load(image_path)
    img_size = 800 // n
    image = pygame.transform.scale(image, (n * img_size, n * img_size))
    tile_size = image.get_width() // n
    tile_size = img_size
    tiles = []
    for i in range(n):
        for j in range(n):
            rect = pygame.Rect(j * tile_size, i * tile_size, tile_size, tile_size)
            tile = image.subsurface(rect).copy()
            tiles.append(tile)
    return tiles


def init_pygame(n):
    pygame.init()
    img_size = 800 // n
    screen = pygame.display.set_mode((n * img_size, n * img_size))
    pygame.display.set_caption("15-Puzzle Solver Visualization")
    return screen


def render_puzzle(screen, tiles, board_state, moving_tile=None):
    screen.fill((100, 100, 100))
    tile_size = tiles[0].get_width()
    n = len(board_state)
    for i in range(n):
        for j in range(n):
            tile_index = board_state[i][j]
            if tile_index != 0 and tile_index != moving_tile:
                screen.blit(tiles[tile_index - 1], (j * tile_size, i * tile_size))

    # pygame.display.flip()


def slide_tile(screen, tiles, board_state, tile_from, tile_to, steps=30):
    tile_size = tiles[0].get_width()
    from_x, from_y = tile_from[1] * tile_size, tile_from[0] * tile_size
    to_x, to_y = tile_to[1] * tile_size, tile_to[0] * tile_size

    dt = 1 / steps

    tile_index = board_state[tile_from[0]][tile_from[1]]
    for step in range(steps):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        render_puzzle(screen, tiles, board_state, tile_index)
        screen.blit(
            tiles[tile_index - 1],
            (
                from_x + (to_x - from_x) * smoothing_func(dt * step),
                from_y + (to_y - from_y) * smoothing_func(dt * step),
            ),
        )
        pygame.display.flip()
        pygame.time.delay(20)


def animate_solution(screen, tiles, solution_path):
    for i in range(1, len(solution_path)):
        current_state = solution_path[i - 1]
        next_state = solution_path[i]
        n = len(current_state)
        for row in range(n):
            for col in range(n):
                if current_state[row][col] != next_state[row][col]:
                    if current_state[row][col] == 0:
                        tile_from = (row, col)
                    else:
                        tile_to = (row, col)

        slide_tile(screen, tiles, current_state, tile_to, tile_from)

        # render_puzzle(screen, tiles, next_state)
        # pygame.display.flip()
        pygame.time.delay(100)


# def animate_solution(screen, tiles, solution_path):
#     for state in solution_path:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()

#         render_puzzle(screen, tiles, state)
#         time.sleep(1)  # Adjust the speed as needed


def run_visualizer(solution_path, image_path="base.JPG"):
    n = len(solution_path[0])
    screen = init_pygame(n)
    tiles = load_and_slice_image(image_path, n)

    animate_solution(screen, tiles, solution_path)

    pygame.quit()
