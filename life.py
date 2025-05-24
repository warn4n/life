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

# Initial area dimensions for random or centered patterns
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


def initial_cells(pattern, width, height):
    """Return a set of starting cells for the given pattern."""
    if pattern == "random":
        return random_cells(width, height)
    cells = PATTERNS.get(pattern, set())
    offset_x = width // 2
    offset_y = height // 2
    return {(x + offset_x, y + offset_y) for (x, y) in cells}


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


NEIGHBOR_OFFSETS = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),            (1, 0),
    (-1, 1),  (0, 1),  (1, 1),
]

# Some interesting starting patterns defined relative to (0, 0)
PATTERNS = {
    "glider": {
        (1, 0), (2, 1),
        (0, 2), (1, 2), (2, 2),
    },
    "pulsar": {
        (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
        (0, 2), (5, 2), (7, 2), (12, 2),
        (0, 3), (5, 3), (7, 3), (12, 3),
        (0, 4), (5, 4), (7, 4), (12, 4),
        (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
        (2, 7), (3, 7), (4, 7), (8, 7), (9, 7), (10, 7),
        (0, 8), (5, 8), (7, 8), (12, 8),
        (0, 9), (5, 9), (7, 9), (12, 9),
        (0, 10), (5, 10), (7, 10), (12, 10),
        (2, 12), (3, 12), (4, 12), (8, 12), (9, 12), (10, 12),
    },
    "gosper": {
        (0, 4), (0, 5), (1, 4), (1, 5),
        (10, 4), (10, 5), (10, 6),
        (11, 3), (11, 7),
        (12, 2), (12, 8),
        (13, 2), (13, 8),
        (14, 5),
        (15, 3), (15, 7),
        (16, 4), (16, 5), (16, 6),
        (17, 5),
        (20, 2), (20, 3), (20, 4),
        (21, 2), (21, 3), (21, 4),
        (22, 1), (22, 5),
        (24, 0), (24, 1), (24, 5), (24, 6),
        (34, 2), (34, 3),
        (35, 2), (35, 3),
    },
}


def step(cells):
    """Compute the next generation for an unbounded board."""
    from collections import Counter

    # Use Counter for neighbor accumulation which is implemented in C and is
    # generally faster than manually updating a dict in Python.
    counts = Counter(
        (x + dx, y + dy)
        for (x, y) in cells
        for (dx, dy) in NEIGHBOR_OFFSETS
    )
    return {
        pos
        for pos, count in counts.items()
        if count == 3 or (count == 2 and pos in cells)
    }


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
    root.update_idletasks()

    # Center view on starting pattern
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    min_x, min_y, max_x, max_y = bounding_box(cells)
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    OFFSET_X = center_x - canvas_width / (2 * CELL_SIZE)
    OFFSET_Y = center_y - canvas_height / (2 * CELL_SIZE)
    root.focus_set()

    generation = 0

    def zoom(factor):
        global CELL_SIZE, OFFSET_X, OFFSET_Y
        new_size = int(CELL_SIZE * factor)
        new_size = min(max(new_size, 2), 50)
        if new_size == CELL_SIZE:
            return
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        center_x = OFFSET_X + canvas_width / (2 * CELL_SIZE)
        center_y = OFFSET_Y + canvas_height / (2 * CELL_SIZE)
        CELL_SIZE = new_size
        OFFSET_X = center_x - canvas_width / (2 * CELL_SIZE)
        OFFSET_Y = center_y - canvas_height / (2 * CELL_SIZE)

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
            zoom(1.2)
        elif event.keysym in ('minus', 'underscore'):
            zoom(1 / 1.2)
        draw_cells_tk(canvas, cells, OFFSET_X, OFFSET_Y, CELL_SIZE)

    root.bind('<Key>', on_key)

    update()
    root.mainloop()


# ---------------------------------------------------------------------------
# Main loop for terminal mode
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Conway's Game of Life")
    parser.add_argument(
        "--help-all",
        action="store_true",
        help="show extended help including available patterns and GUI controls",
    )
    parser.add_argument(
        "--gui", action="store_true", help="display the game in a graphical window"
    )
    parser.add_argument(
        "--pattern",
        choices=["random"] + sorted(PATTERNS.keys()),
        default="random",
        help="starting pattern to use",
    )
    args = parser.parse_args()

    if args.help_all:
        parser.print_help()
        print("\nAvailable patterns:")
        for name in sorted(PATTERNS.keys()):
            print(f"  {name}")
        print("\nGUI controls:\n  Arrow keys move the view\n  + or - zoom in and out")
        return

    global WIDTH, HEIGHT
    WIDTH, HEIGHT = get_board_size(WIDTH, HEIGHT)
    cells = initial_cells(args.pattern, WIDTH, HEIGHT)

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
