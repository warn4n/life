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

# Simple implementation of Conway's Game of Life using an unbounded board

# Initial area of random live cells
WIDTH = 20
HEIGHT = 10

ALIVE = 'O'
DEAD = ' '

# Visualisation defaults
CELL_SIZE = 10  # pixel size of a cell when using GUI mode

# panning/zooming
OFFSET_X = 0
OFFSET_Y = 0


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


# ---------------------------------------------------------------------------
# Data helpers operating on a set of live cell coordinates
# ---------------------------------------------------------------------------

def random_cells(width, height):
    cells = set()
    for y in range(height):
        for x in range(width):
            if random.choice([True, False]):
                cells.add((x, y))
    return cells


def bounding_box(cells):
    if not cells:
        return 0, 0, 0, 0
    xs = [c[0] for c in cells]
    ys = [c[1] for c in cells]
    return min(xs), min(ys), max(xs), max(ys)


def print_cells(cells):
    os.system('cls' if os.name == 'nt' else 'clear')
    min_x, min_y, max_x, max_y = bounding_box(cells)
    for y in range(min_y, max_y + 1):
        row = ''
        for x in range(min_x, max_x + 1):
            row += ALIVE if (x, y) in cells else DEAD
        print(row)


def step(cells):
    """Compute the next generation for an unbounded board."""
    neighbor_counts = {}
    for (x, y) in cells:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                key = (x + dx, y + dy)
                neighbor_counts[key] = neighbor_counts.get(key, 0) + 1
    new_cells = set()
    for cell, count in neighbor_counts.items():
        if count == 3 or (count == 2 and cell in cells):
            new_cells.add(cell)
    return new_cells


# ---------------------------------------------------------------------------
# Tkinter visualisation with panning and zooming
# ---------------------------------------------------------------------------

def draw_cells_tk(canvas, cells, offset_x, offset_y, cell_size):
    canvas.delete("all")
    for x, y in cells:
        sx = (x - offset_x) * cell_size
        sy = (y - offset_y) * cell_size
        canvas.create_rectangle(
            sx,
            sy,
            sx + cell_size,
            sy + cell_size,
            fill="black",
            outline="",
        )
    canvas.update()


def run_gui(cells):
    """Run the simulation using a tkinter window."""
    if tk is None:
        raise RuntimeError("tkinter is not available")

    global OFFSET_X, OFFSET_Y, CELL_SIZE

    root = tk.Tk()
    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack(fill="both", expand=True)
    root.focus_set()

    generation = 0

    def update():
        nonlocal cells, generation
        draw_cells_tk(canvas, cells, OFFSET_X, OFFSET_Y, CELL_SIZE)
        root.title(f"Game of Life - Generation {generation}")
        generation += 1
        cells = step(cells)
        root.after(500, update)

    def on_key(event):
        global CELL_SIZE, OFFSET_X, OFFSET_Y
        if event.keysym == 'Up':
            OFFSET_Y -= 5
        elif event.keysym == 'Down':
            OFFSET_Y += 5
        elif event.keysym == 'Left':
            OFFSET_X -= 5
        elif event.keysym == 'Right':
            OFFSET_X += 5
        elif event.keysym in ('plus', 'equal'):
            CELL_SIZE = min(int(CELL_SIZE * 1.2), 50)
        elif event.keysym in ('minus', 'underscore'):
            CELL_SIZE = max(int(CELL_SIZE / 1.2), 2)
        draw_cells_tk(canvas, cells, OFFSET_X, OFFSET_Y, CELL_SIZE)

    root.bind('<Key>', on_key)

    update()
    root.mainloop()


# ---------------------------------------------------------------------------
# Main loop for terminal mode
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument("--gui", action="store_true", help="display the game in a graphical window")
    args = parser.parse_args()

    global WIDTH, HEIGHT
    WIDTH, HEIGHT = get_board_size(WIDTH, HEIGHT)
    cells = random_cells(WIDTH, HEIGHT)

    if args.gui:
        run_gui(cells)
        return

    generation = 0
    try:
        while True:
            print_cells(cells)
            print(f"Generation: {generation}")
            generation += 1
            cells = step(cells)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nSimulation stopped.")



if __name__ == "__main__":
    main()
