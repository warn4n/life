import random
import time
import os

# Simple implementation of Conway's Game of Life

WIDTH = 20
HEIGHT = 10
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

def main():
    grid = random_grid(WIDTH, HEIGHT)
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
