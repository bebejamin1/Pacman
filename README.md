<div align="center">
    <i>This project has been created as part of the 42 curriculum by npillet and bbeaurai</i>
    <h1>Pac-Man</h1>
    <h3>Ghosts! More ghosts!</h3>
</div>

## Description
**Pac-Man** was first created in 1980 by Namco. It has four ghosts who each have their own algorithm.</br>
This project's goal is to recreate a complete and playable Pac-Man game in Python.
It has to be a deployment-ready package suitable for distribution on a public gaming platform.

## Instructions
With these commands, once entered inside the terminal, the program will be able to run.
``` bash
make # Run the program after installing the necessary dependencies

python3 pac-man.py config.json # Runs the program
```

And below, you will find other commands:
| Command | Description |
| :---: | --- |
| `make install` | Install the project's dependencies |
| `make run` | Execute the program (like the `make` command) |
| `make debug` | Run the script using the the Python built-in debugger |
| `make clean` | Remove temporary files and caches |
| `make lint` | Execute the `flake8` and `mypy` commands |
| `make lint-strict` | Execute the `flake8` and a stricter version of `mypy` commands |

## Configuration
A few parameters need to be defined inside the configuration file, such as:
| Key | Value |
| :---: | :---: |
| `highscore_filename` | / |
| `level` | Array with the width and height |
| `lives` | 3 |
| `pacgum` | 42 |
| `points_per_pacgum` | 10 |
| `points_per_super_pacgum` | 50 |
| `points_per_ghost` | 200 |
| `seed` | 42 |
| `level_max_time` | 90 |

Each of these parameters is used to define the aspects of the game.<br>
The `highscore_filename` is the file inside which the highest players' score are kept. The `level` defines one or more level dimensions (the width and the height). `lives` defines the players' number of lives, the `pacgum` is (percentage or number of pacgum) available on the level.<br>
For `points_per_pacgum`, `points_per_super_pacgum` and `points_per_ghost` define the points received for eating the pacgums, the super pacgums and the ghosts respectively. The `seed` defines a specific maze generation. Finally, the `level_max_time` defines the maximum time to complete the level.

The config file passed on the command line is always resolved under the `data/` folder (a bare filename is prefixed with `data/` automatically), which keeps every configuration and leaderboard file in one place. If the file does not exist yet, is not valid JSON, or is missing/invalid keys, it is regenerated with the default configuration below, a message is printed to explain what happened, and the game still starts — so the player is never blocked by a faulty config file.

The default configuration is given in the collapsible section below.
<details>
<summary>Default configuration</summary>

```json
{
  "highscore_filename": "data/leaderboard.json",
  "live": 3,
  "pacgum_points": 10,
  "super_pacgum_points": 50,
  "ghost_points": 200,
  "seed": 42,
  "level_max_time": 90,
  "level": [
    {
      "name": "Level 1",
      "width": 12,
      "height": 10
    },
    {
      "name": "Level 2",
      "width": 18,
      "height": 12
    },
    {
      "name": "Level 3",
      "width": 10,
      "height": 10
    },
    {
      "name": "Level 4",
      "width": 10,
      "height": 20
    },
    {
      "name": "Level 5",
      "width": 15,
      "height": 19
    },
    {
      "name": "Level 6",
      "width": 14,
      "height": 10
    },
    {
      "name": "Level 7",
      "width": 15,
      "height": 10
    },
    {
      "name": "Level 8",
      "width": 12,
      "height": 16
    },
    {
      "name": "Level 9",
      "width": 14,
      "height": 10
    },
    {
      "name": "Level 10",
      "width": 20,
      "height": 20
    }
  ]
}
```
</details>

## Highscore
The path to `leaderboard.json` has to be inside the root data folder.<br>
This file is presented like this:
```json
{
  "scores": [
    {
      "player_name": "erreip56",
      "player_score": 23280
    },
    {
      "player_name": "zorb",
      "player_score": 8400
    }
  ]
}
```
It contains the name of the person and their score and is ordered from highest to lowest score.
To display them in the menu, the file is parsed.</br>
To display them, the rank, the name and the score are aligned from one line to another, like in the example below.
<img src="assets/README/leaderboard.png" />

## Maze Generation
In the class `GameEngine`, the function `new_maze()` creates the game's levels that are used inside the class `Maze` to draw them.<br>
The first level's maze is generated and stored by the function `generate_first_maze()`, which the game view then loads into its first `Maze`.

## General Software Architecture & Implementation
### General Software Architecture
#### Initialization
`pac-man.py` is the entry point: it parses the config file (`src/parsing/`), then creates and runs the `GameEngine` (`src/renderer/game_engine.py`), which builds every view once and shows the main menu.
1. `main(conf_path)` calls `parser(conf_path)`, which loads/validates the config and the leaderboard.
2. `GameEngine()` is created (an `arcade.Window` subclass) and loads the shared music tracks.
3. `GameEngine.set_view()` instantiates every view listed below.
4. `GameEngine.start_game()` shows the main menu and starts the Arcade event loop.

#### Algorithm (`src/engine/algo.py`)
- Greddy
  - The Ghosts' algorithm
- Personality(Enum)
  - Different personalities of the ghost
- Mode(Enum)
  - Different states of the ghost

#### Game (`src/engine/game.py`)
- Cheats
  - States of a few implemented cheats, shared between the game view and the cheat menu

#### Maze
- Level (`src/engine/level.py`)
  - Stores level information (walls, corridors, spawns, pacgum/super-pacgum positions) derived from the generated maze grid
- Maze (`src/renderer/in_game/maze.py`)
  - Builds and draws the on-screen sprites for one level's maze

#### Entities (`src/renderer/in_game/`)
- Player (`characters.py`)
- Enemies (`characters.py`)
- Object (`sprite.py`)
  - Takes care of the pacgums and super-pacgums

#### Manager (`src/renderer/game_engine.py`)
- GameEngine
  - Handles every view of the game and the game window

#### Views (`src/renderer/`)
Different views rendering every state of the game:
- GameView (`game_mode.py`)
  - Handles the game progression
- MenuView (`ui/menu_screen.py`)
  - Shows the main game menu from which you can either: start the game, look at the instructions or the leaderboard or quit the game
- InstructionsView (`ui/instructions_screen.py`)
  - Shows the game's instructions
- HighscoreView (`ui/highscore_screen.py`)
  - Shows the name and scores registered inside `leaderboard.json`
- PauseView (`ui/pause_screen.py`)
  - Pause menu of the game
- CheatView (`ui/cheat_screen.py`)
  - Activate or deactivate different cheats
- EndView (`ui/end_screen.py`)
  - Register the name and score of the player in `leaderboard.json`


Here is a brief overview of how the game works.
```mermaid
graph LR
    classDef start fill:#eceff1,stroke:#607d8b,stroke-width:2px,color:#333;
    classDef start_sub stroke:#eceff1,stroke-width:2px;
    classDef menu fill:#fff3e0,stroke:#f57c00,stroke-width:2px,color:#333;
    classDef menu_sub stroke:#fff3e0,stroke-width:2px;
    classDef levels fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px,color:#333;
    classDef levels_sub stroke:#f3e5f5,stroke-width:2px;
    classDef finish fill:#e8f5e9,stroke:#388e3c,stroke-width:2px,color:#333;
    classDef finish_sub stroke:#e8f5e9,stroke-width:2px;

    subgraph Sub1["Beginning"]
      A(Start) --> B(Main Menu)
    end
    class Sub1 start_sub;
    class A,B start;

    subgraph Sub2["Menu"]
      B --> C{Decision?}
      C -->|Game| D(Start Level 1)
      C <-->|Instructions| E(Shows Instructions)
      C <-->|Highscore| F(Shows Highscores)
      C -->|Exit| G(Quits Game)
    end
    class Sub2 menu_sub;
    class C,D,E,F,G menu;

    subgraph Sub3["Levels"]
      D --> H(Level n)
      H --> I{Win ?}
      I -->|Yes| J{Completed every level?}
      J -->|No| M(Next Level)
      M --> H
    end
    class Sub3 levels_sub;
    class H,I,J,M levels;

    subgraph Sub4["Finish Screen"]
      direction RL
      I -->|No| K(Defeat Screen)
      J -->|Yes| L(Victory Screen)
      K --> N(Enter Name)
      L --> N
      N --> B
    end
    class Sub4 finish_sub;
    class K,L,N finish;

    linkStyle default stroke:gray;
```

### Implementation
We used the arcade library for the graphical rendering and a few game logic aspects like collisions.

For the ghosts, each has their own algorithm. One will chase the player, another will hide from them, a third will try to ambush and the last has a random way of moving.</br>

## Project Management
The task realized during this project for each member is listed below:
- [**bbeaurai | bebejamin1**](https://github.com/bebejamin1)
  - Parsing
  - Leaderboard
  - Ghosts algorithm and implementation

- [**npillet | noemiepi**](https://github.com/noemiepi)
  - User interfaces (every view)
  - Assets' creation
  - README

A more detailed version of the management can be found in the [**`project_management`**](project_management/) folder at the root of this repository.

## Packaging & Itch.io
The Linux build is packaged with [PyInstaller](https://pyinstaller.org/), configured through [`pacman.spec`](pacman.spec) at the root of the repository. The steps below are run by hand (on purpose, to keep the process transparent and reproducible during peer review) to go from that spec file to a zip ready for upload.

<details>
<summary>How to (re)build the package</summary>

1. **Build the executable** from the spec file:
   ```bash
   uv run pyinstaller pacman.spec --noconfirm
   ```
   This produces `dist/pacman/` (the `pacman` executable plus its bundled libraries in `_internal/`).

2. **Fix a known PyInstaller/arcade quirk** (cosmetic only, the game runs fine without it, but it prints a confusing error otherwise): the `arcade` library's own PyInstaller hook sometimes makes PyInstaller turn its `VERSION` data file into a folder instead of a file.
   ```bash
   cd dist/pacman/_internal/arcade
   mv VERSION/VERSION VERSION.tmp && rmdir VERSION && mv VERSION.tmp VERSION
   cd -
   ```

3. **Copy the game assets and default config** next to the executable. The game loads them through plain relative paths (e.g. `assets/background/...`), resolved against the current working directory, so they must sit alongside `pacman`, not inside `_internal/`:
   ```bash
   cp -r assets dist/pacman/assets
   mkdir -p dist/pacman/data
   cp data/config.json dist/pacman/data/config.json
   ```

4. **Add minimal in-package instructions** (controls, cheats, configuration), e.g. create `dist/pacman/INSTRUCTIONS.txt` with:
   ```
   HOW TO RUN
       ./pacman data/config.json

   CONTROLS
       Move          Arrow keys or WASD
       Pause/Resume  SPACE
       Cheat menu    C (while playing)
       Back / Quit   ESCAPE

   CONFIGURATION
       Edit data/config.json (JSON, "#" comments allowed), or pass another file:
           ./pacman path/to/other_config.json
       Highscores (top 10) are saved to data/leaderboard.json.
   ```

5. **Zip it up** for upload:
   ```bash
   cd dist && zip -r pacman-linux.zip pacman
   ```

6. **Upload `dist/pacman-linux.zip` to itch.io**: new project → *Kind of project*: Downloadable → drop the zip in *Uploads* → tag it **Linux** → set visibility to **Restricted (unlisted)** or **Private** → save.

</details>

The game's page can be found [**here**](https://nomipi.itch.io/pac-man-42).

## Resources
### Notions
#### Arcade library
- https://api.arcade.academy/en/development/index.html

### GitHub
- [noemiepi](https://github.com/noemiepi/A-Maze-ing)

- [Overtekk](https://github.com/Overtekk/PacMan)

- [sousampere](https://github.com/sousampere/42_pacman)

### AI Usage:
AI (Claude Code) was used to find a few good classes and methods names and to help solve `make lint-strict` issues during development.<br>
It was also used, in a later pass, to write every missing docstring in `src/engine/` and `src/renderer/` (Google style, PEP 257: purpose, `Args`, `Returns`/`Raises`).
