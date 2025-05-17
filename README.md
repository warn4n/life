# Life

A minimal implementation of John Horton Conway's [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in Python.
The board automatically sizes itself to your terminal (fallback 20x10).

## Running locally

1. Ensure you have Python 3 installed.
2. From this directory, run:
   ```bash
   python3 life.py
   ```
3. The simulation will display generations in your terminal. Press `Ctrl+C` to stop.

By default the board uses your terminal's current size. If detection fails, you can supply dimensions using:

```bash
stty size | python3 life.py
```
