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
- [noemiepi](https://github.com/noemiepi/A-Maze-ing)


## Known Parsing Inconsistencies (TODO)

Issues found in `src/parsing/` while comparing with the subject. Listed
here on purpose: the parsing rework is planned, nothing below is fixed
yet.

- `#` comment lines in the JSON config are not stripped (subject V.2):
  a commented config crashes `json.load`, gets caught by the wrong
  `except` and shows a misleading "path is not accessible" message.
- On a missing or invalid value the parser prints an error and exits,
  while the subject (V.3) asks to clamp to a safe default, log a
  message and continue.
- Unknown keys are rejected (max 8 top-level keys, exactly 3 fields per
  level, level names forced to "Level N" in ascending order) while the
  subject says unknown keys must be ignored.
- `python3 pac-man.py` without argument prints the usage message but
  does not stop, then crashes with an `IndexError` traceback.
- The config path is forced under `data/` (`parser(f"data/{argv[1]}")`),
  so an absolute or external config path cannot be used.
- `parse_leaderbord`: a name of 10 characters or less containing an
  invalid character raises `UnboundLocalError` (`error` is only defined
  in the "name too long" branch).
- The `except TypeError` branch of `parse_conf` does not exit, so the
  function can then return `path_leaderbord` while it is unbound.
- `leaderbord_update` does not validate the player name on insert, does
  not protect file accesses with try/except, and depends on a
  `global leaderbord_path` set by `parser()` (crashes if called first).
- The Configuration table above documents `lives` / `pacgum` /
  `points_per_pacgum` while the actual config keys are `live` /
  `pacgum_points` / etc.
- A leaderboard entry with a score of 0 is rejected
  (`not p.get("player_score")` treats 0 as a missing value), while the
  subject allows non-negative scores, 0 included.
- `make lint` currently fails because of `src/parsing/`: mypy reports
  6 errors there (`leaderbord_path` undefined at module level, a
  missing annotation on `default_leaderbord`, an `Any` return in
  `parse_leaderbord`).


[] Strip des lignes # avant json.load (V.2)

[] Valeur manquante/invalide → défaut + message + continuer (remplacer tous les exit()) (V.3)

[] Ignorer les clés inconnues (supprimer : max 8 clés, 3 champs par level, nom Level N ordonné)

[] Supprimer le préfixe data/ forcé sur le chemin du config

[] Fix UnboundLocalError : error non défini pour un nom court invalide

[] Fix branche except TypeError : ne pas retourner path_leaderbord non défini

[] Accepter un score de 0 dans le leaderboard (0 traité comme « absent » actuellement)

[] leaderbord_update : valider le nom (≤10, alphanum+espaces), try/except sur les I/O, supprimer le global

[] Corriger les 6 erreurs mypy de src/parsing/ → make lint doit passer

[] Aligner le tableau Configuration du README avec les vraies clés (live, pacgum_points…)

[] Remettre les docstrings à la fin du chantier
