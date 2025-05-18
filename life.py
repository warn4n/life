import random
import time
import os
import sys
import shutil
import argparse

try:
    import tkinter as tk
except ImportError:
    tk = None

# Simple implementation of Conway's Game of Life

WIDTH = 20
HEIGHT = 10
ALIVE = 'O'
DEAD = ' '

CELL_SIZE = 10  # pixel size of a cell when using GUI mode


def get_board_size(default_width, default_height):
    """Determine board size using stdin or terminal size."""
    width, height = default_width, default_height
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip().split()
        if len(data) >= 2 and all(part.isdigit() for part in data[:2]):
            height, width = int(data[0]), int(data[1])
            return width, height
    try:
        size = shutil.get_terminal_size()
        width, height = size.columns, size.lines - 1
    except OSError:
        pass
    return width, height

def random_grid(width, height):
    return [[random.choice([True, False]) for _ in range(width)] for _ in range(height)]

def print_grid(grid):
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in grid:
        print(''.join(ALIVE if cell else DEAD for cell in row))


def draw_grid_tk(canvas, grid):
    """Render the grid on a tkinter canvas."""
    canvas.delete("all")
    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            if grid[y][x]:
                canvas.create_rectangle(
                    x * CELL_SIZE,
                    y * CELL_SIZE,
                    (x + 1) * CELL_SIZE,
                    (y + 1) * CELL_SIZE,
                    fill="black",
                    outline=""
                )
    canvas.update()

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


def run_gui(grid):
    """Run the simulation using a tkinter window."""
    if tk is None:
        raise RuntimeError("tkinter is not available")

    root = tk.Tk()
    canvas = tk.Canvas(root, width=WIDTH * CELL_SIZE, height=HEIGHT * CELL_SIZE, bg="white")
    canvas.pack()
    generation = 0

    def update():
        nonlocal grid, generation
        draw_grid_tk(canvas, grid)
        root.title(f"Game of Life - Generation {generation}")
        generation += 1
        grid = step(grid)
        root.after(500, update)

    update()
    root.mainloop()

def main():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("--gui", action="store_true", help="display the game in a graphical window")
    args = parser.parse_args()

    global WIDTH, HEIGHT
    WIDTH, HEIGHT = get_board_size(WIDTH, HEIGHT)
    grid = random_grid(WIDTH, HEIGHT)

    if args.gui:
        run_gui(grid)
        return

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
