import math

import pygame
import random
pygame.init()
tick = 50
class drawing_information:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE
    GRADIENTS = [
        (50, 50, 50),
        (80, 80, 80),
        (110, 110, 110),
    ]

    SIDE_PAD = 100
    TOP_PAD = 150
    FONT = pygame.font.SysFont('arialblack', 30)
    LARGE_FONT = pygame.font.SysFont('Arialblack', 40)
    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Alg Visualisation")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def generate_starting_list(n, min_val, max_val):
    return [random.randint(min_val, max_val) for _ in range(n)]

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 5))

    controls = draw_info.FONT.render("R - reset | SPACE - start sort | A - ascending | D - descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, ( draw_info.width/2 - controls.get_width()/2, 65))

    sorting = draw_info.FONT.render("I - insertion | B - bubble | C - count | Q - quick | M - merge", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, ( draw_info.width/2 - sorting.get_width()/2, 95))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2,
                      draw_info.TOP_PAD,
                      draw_info.width - draw_info.SIDE_PAD,
                      draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.block_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height
        color = draw_info.GRADIENTS[i%3]
        if i in color_positions:
            color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.block_height*val))

    if clear_bg:
        pygame.display.update()

def swap(list, a, b):
    list[a], list[b] = list[b], list[a]

def bubble_sort(draw_info, ascending = True, val_range=(0,100)):
    lst = draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                swap(lst, j, j+1)
                draw_list(draw_info, {j: draw_info.GREEN, j+1: draw_info.RED}, True)
                yield True
    return lst

def insertion_sort(draw_info, ascending=True, val_range=(0, 100)):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
            lst[i] = lst[i - 1]
            i = i-1
            lst[i] = current
            draw_list(draw_info, {i-1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst

def counting_sort(draw_info, ascending=True, val_range=(0, 100)):
    A = draw_info.lst
    lst = A[:]
    n = len(lst)
    k = val_range[1] + 1
    C = [0]*k
    B = [0] * n
    for i in range(n):
        C[lst[i]] += 1
        draw_list(draw_info, {i: draw_info.GREEN}, True)
        yield True


    if ascending:
        for i in range(1, k):
            C[i] += C[i-1]
    else:
        for i in range(k-1, 0, -1):
            C[i - 1] += C[i]


    for i in range(n-1, -1, -1):
        C[lst[i]] -= 1
        B[C[lst[i]]] = lst[i]
        draw_info.lst[C[lst[i]]] = lst[i]
        draw_list(draw_info, {C[lst[i]]: draw_info.GREEN, i: draw_info.RED}, True)
        yield True
    return A

def partition(arr, l, h, draw_info, ascending):

    i = (l - 1)
    x = arr[h]

    for j in range(l, h):
        if arr[j] <= x and ascending or arr[j] >= x and not ascending:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
            draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
            pygame.time.Clock().tick(tick)
    arr[i + 1], arr[h] = arr[h], arr[i + 1]
    return (i + 1)


def quickSortIterative(draw_info, ascending, useless_min_max):
    arr = draw_info.lst
    l = 0
    h = len(arr) - 1
    size = h - l + 1
    stack = [0] * (size)
    top = 0
    stack[top] = l
    top += 1
    stack[top] = h
    while top >= 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    return
        h = stack[top]
        top -= 1
        l = stack[top]
        top -= 1
        p = partition(arr, l, h, draw_info, ascending)
        if p - 1 > l:
            top += 1
            stack[top] = l
            top += 1
            stack[top] = p - 1
        if p + 1 < h:
            top += 1
            stack[top] = p + 1
            top += 1
            stack[top] = h

def merge(arr, start, mid, end, draw_info, ascending):
    start2 = mid + 1
    if (arr[mid] <= arr[start2]):
        return 1
    while (start <= mid and start2 <= end):
        if (arr[start] <= arr[start2]):
            start += 1
        else:
            value = arr[start2]
            index = start2
            dict = {}

            while (index != start):
                arr[index] = arr[index - 1]
                dict[index] = draw_info.RED


                index -= 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        return None
            arr[start] = value
            dict[start] = draw_info.GREEN
            draw_list(draw_info, dict, True)
            pygame.time.Clock().tick(60)
            start += 1
            mid += 1
            start2 += 1
    return 1


def mergeSort(arr, l, r, draw_info, ascending):
    if (l < r):
        m = l + (r - l) // 2
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:
                    return None
        if(mergeSort(arr, l, m, draw_info, ascending) == None): return None
        if(mergeSort(arr, m + 1, r, draw_info, ascending) == None): return None

        if(merge(arr, l, m, r, draw_info, ascending) == None): return None
    return 1

def mSort(draw_info, ascending, useless_min_max):
    mergeSort(draw_info.lst, 0, len(draw_info.lst) - 1, draw_info, ascending)

def main():
    global tick
    run = True
    clock = pygame.time.Clock()
    n = 50
    min_val = 0
    max_val = 100
    tick_speed_static = 60
    tick = tick_speed_static
    lst = generate_starting_list(n, min_val, max_val)
    draw_info = drawing_information(1000, 800, lst)

    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algorithm_generator = None
    while run:
        clock.tick(tick)

        if sorting:
            try:
                if(next(sorting_algorithm_generator) == None): draw_info.set_list(generate_starting_list(n, min_val, max_val))
            except (TypeError, StopIteration):
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and not sorting:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(draw_info, ascending, (draw_info.min_val, draw_info.max_val))
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                tick = tick_speed_static
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                tick = tick_speed_static
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"
            elif event.key == pygame.K_c and not sorting:
                tick = math.floor(tick*0.7)
                sorting_algorithm = counting_sort
                sorting_algo_name = "Counting Sort"
            elif event.key == pygame.K_q and not sorting:
                tick = tick_speed_static
                sorting_algorithm = quickSortIterative
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_m and not sorting:
                tick = tick_speed_static
                sorting_algorithm = mSort
                sorting_algo_name = "Merge Sort"
    pygame.quit()

if __name__ == "__main__":
    main()
