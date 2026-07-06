<div align="center">
    <i>This project has been created as part of the 42 curriculum by npillet and bbeaurai</i>
    <h1>Pac-Man</h1>
    <h3>Ghosts! More ghosts!</h3>
</div>

## Description
This project's goal is to recreate a complete and playable Pac-Man in python.

## Instructions
With these commands, once entered inside the terminal, the program will be able to run.
``` bash
make # Runs the program after installing the necessary dependencies

python3 pac-man.py config.json # Runs the program
```

## Configuration
A few parameters need to be defined inside the configuration file, such as:
| Key | Value |
| --- | --- |
| highscore_filename | / |
| level | array with the width and height |
| lives | 3 |
| pacgum | 42 |
| points_per_pacgum | 10 |
| points_per_super_pacgum | 50 |
| points_per_ghost | 200 |
| seed | 42 |
| level_max_time | 90 |

Each of these parameters are used to define the aspects of the game.<br>
The `highscore_filename` is the file inside which the highest players score are kept. The `level` defines one or more levels dimensions (the width and the height). `lives` defines the players number of lives, the `pacgum` is (percentage or number of pacgum) available on the level.<br>
For `points_per_pacgum`, `points_per_super_pacgum` and `points_per_ghost` defines the points received for eating the pacgums, the super pacgums and the ghosts respectively. The `seed` defines a specific maze generation. Finally, the `level_max_time` defines the maximum time to complete the level.

## Highscore
*explaining how the highscore system works and why you decided to implement it this way*

## Maze Generation
*explaining how the assigned A-Maze-ing package is used to generate mazes*

## Implementation
*technical summary of your implementation*

## General Software Architecture
*high-level overview of the software architecture (modules, classes and their relationships)*<br>
*(graph)*

## Project Management
*brief overview of how you managed the project and a link to the dedicated project management directory*

## Resources
### Notions
- 

### GitHub
- 