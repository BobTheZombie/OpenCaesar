# OpenCaesar

OpenCaesar is an open-source, Linux-native prototype inspired by the classic
Caesar II city-building series. The goal of the project is to provide a modern,
Python-powered foundation for experimenting with Roman urban planning and
economic management games.

## Features

- **Tile-based city grid** with free placement for a handful of core building
  types (insulae, farms, markets, wells, and roads).
- **Simple economic simulation** that tracks population, food, treasury, and
  happiness across discrete ticks.
- **Accessible controls** using mouse placement and keyboard shortcuts similar
  to classic Caesar titles.
- **Cross-platform Python implementation** with a focus on running smoothly on
  Linux desktops using SDL2/Pygame.

## Getting Started

### Prerequisites

- Python 3.10 or newer
- SDL2 development libraries (usually provided by your distribution)

Install the game and its dependencies with `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### Running the Game

Once installed, launch the game module from anywhere on your system:

```bash
python -m open_caesar.game
```

### Running Tests

To execute the automated test suite, install the optional development
dependencies and run `pytest`:

```bash
pip install -e .[dev]
pytest
```

Use the mouse to place buildings on the grid. Left click constructs the current
selection if you can afford it, right click demolishes an existing structure.

### Controls

| Action                    | Input                     |
|---------------------------|---------------------------|
| Cycle buildings           | `Tab`                     |
| Select building directly  | Number keys `1-5`         |
| Place building            | Left mouse button         |
| Demolish building         | Right mouse button        |
| Advance simulation tick   | `Space`                   |
| Quit                      | `Esc`                     |

## Project Structure

```
src/open_caesar/      # Game code
    buildings.py      # Building definitions and stats
    city.py           # Simulation logic and grid management
    game.py           # Pygame loop and input handling
    ui.py             # Rendering helpers for the HUD and map
requirements.txt      # Python dependencies
tests/                # Pytest suite for core systems
```

## Contributing

OpenCaesar is at an early prototype stage. Contributions are welcome! Suggested
ideas include improving art assets, expanding the economy model, or porting the
engine to additional platforms. Please open an issue or submit a pull request
with your ideas.

## License

This project is released under the MIT License. See `LICENSE` for details.

