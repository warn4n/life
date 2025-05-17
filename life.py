import random
import time
import os
import sys
import shutil

# Simple implementation of Conway's Game of Life

DEFAULT_WIDTH = 20
DEFAULT_HEIGHT = 10
ALIVE = 'O'
DEAD = ' '

def random_grid(width, height):
    return [[random.choice([True, False]) for _ in range(width)] for _ in range(height)]

def print_grid(grid):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in grid:
        print(''.join(ALIVE if cell else DEAD for cell in row))

def count_neighbors(grid, x, y):
    height = len(grid)
    width = len(grid[0])
    count = 0
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height:
                if grid[ny][nx]:
                    count += 1
    return count

def step(grid):
    height = len(grid)
    width = len(grid[0])
    new_grid = [[False] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            neighbors = count_neighbors(grid, x, y)
            if grid[y][x]:
                new_grid[y][x] = neighbors in (2, 3)
            else:
                new_grid[y][x] = neighbors == 3
    return new_grid

def get_board_size():
    """Determine board size from terminal or piped input."""
    width = height = None
    try:
        size = shutil.get_terminal_size()
        width, height = size.columns, size.lines
    except OSError:
        pass

    if (width is None or height is None) and not sys.stdin.isatty():
        data = sys.stdin.read().strip().split()
        if len(data) >= 2 and data[0].isdigit() and data[1].isdigit():
            height = int(data[0])
            width = int(data[1])

    if width is None or height is None:
        width = DEFAULT_WIDTH
        height = DEFAULT_HEIGHT

    return width, height


def main():
    width, height = get_board_size()
    grid = random_grid(width, height)
    generation = 0
    try:
        while True:
            print_grid(grid)
            print(f"Generation: {generation}")
            generation += 1
            grid = step(grid)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nSimulation stopped.")

if __name__ == "__main__":
    main()
