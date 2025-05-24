# Life

A minimal implementation of John Horton Conway's [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in Python.

## Running locally

1. Ensure you have Python 3 installed.
2. From this directory, run:
   ```bash
   python3 life.py
   ```
3. The simulation will display generations in your terminal. Press `Ctrl+C` to stop.

### Starting patterns

By default the board begins with a random collection of live cells. Use the `--pattern` option to start with one of several predefined patterns such as `glider`, `pulsar` or `gosper`:

```bash
python3 life.py --pattern glider
```

The option also works together with graphical mode:

```bash
python3 life.py --gui --pattern gosper
```

### Graphical Mode

To see the Game of Life in a simple graphical window, run the script with the `--gui` flag:

```bash
python3 life.py --gui
```

You can still pipe `stty size` to specify a window size or edit `WIDTH` and `HEIGHT` in `life.py`.

### New features

The board is now unbounded. When running in GUI mode you can use the arrow keys to pan around the infinite board and `+` or `-` to zoom in and out.

The board now automatically scales to your terminal size. You can also pipe the
output of `stty size` to specify a custom size:

```bash
stty size | python3 life.py
```

You can still edit `WIDTH` and `HEIGHT` at the top of `life.py` if you want to
specify fixed dimensions regardless of your terminal size.

### Performance

The evolution step now uses `collections.Counter` under the hood which
provides a noticeable speed boost when many cells are alive.
