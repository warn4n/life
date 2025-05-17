# Life

A minimal implementation of John Horton Conway's [Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life) in Python.

## Running locally

1. Ensure you have Python 3 installed.
2. From this directory, run:
   ```bash
   python3 life.py
   ```
3. The simulation will display generations in your terminal. Press `Ctrl+C` to stop.

The board now automatically scales to your terminal size. You can also pipe the
output of `stty size` to specify a custom size:

```bash
stty size | python3 life.py
```

You can still edit `WIDTH` and `HEIGHT` at the top of `life.py` if you want to
specify fixed dimensions regardless of your terminal size.
