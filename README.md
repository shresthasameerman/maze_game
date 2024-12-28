# Maze Game with Traps

This is a competitive maze game built using Python and Pygame, where the player must navigate through a maze filled with traps. The game features multiple levels, increasing difficulty, and a timer that decreases with each level.

## Features

- **Maze Generation**: Procedurally generated maze using a depth-first search algorithm.
- **Traps**: Randomly placed traps that reduce player lives upon collision. The traps increase in number as the levels progress.
- **Levels**: The game contains multiple levels with increasing difficulty. Each level has a time limit that decreases as the game progresses.
- **Player Movement**: The player moves through the maze using the arrow keys or `WASD` keys.
- **Trap Reveal**: Players can press the `H` key to toggle the visibility of traps.
- **Goal**: Reach the bottom-right corner of the maze to complete the level.
- **Time Limit**: The player has a limited time to complete each level. Time limits decrease with each level.

## Installation

To run this game on your local machine, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/your-username/maze-game.git
cd maze-game

pip install pygame

python maze_game.py
