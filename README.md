# Snake Game with Pygame

#### Video Demo:
[Video Demo](https://youtu.be/h-lET5zv2TQ)

A modern implementation of the classic **Snake** game written in **Python** using
the **Pygame** library. The project focuses on clean object-oriented design,
modular game logic, and custom-built graphical assets.

## Overview

This project recreates the traditional Snake gameplay while emphasizing
maintainable code structure and explicit separation of game entities.
The game logic is implemented in `project.py`, and all visual assets are
stored in the `assets/` directory.

All sprites were designed specifically for this project using
[pikselapp.com](https://pikselapp.com).

## Installation

### Prerequisites

- Python 3.8 or later
- `pip` package manager

### Setup

```bash
git clone https://github.com/USERNAME/Snake-Game.git
cd Snake-Game
pip install -r requirements.txt
```

## Gameplay

- Control the snake using the **arrow keys**
- Collect apples to increase the snake’s length and score
- Avoid collisions with:
  - the game boundaries
  - the snake’s own body

The game ends upon collision.

## Architecture and Design

The game is structured around two primary classes: `Snake` and `Apple`.
This approach was chosen to keep state management explicit and to support
future extensibility.

### Apple

The `Apple` class represents a consumable game object. Upon initialization,
it randomly generates valid grid coordinates for placement on the game board.

### Snake

The `Snake` class manages:

- The snake’s initial position
- A list of body segments
- Separation between head and body logic
- Directional state and sprite rotation
- Game-over state tracking

Each segment of the snake is represented using Pygame `Rect` objects. The head
and tail store rotation values (`0`, `90`, `180`, `270`) to determine correct
sprite orientation during rendering.

### Movement System

Early versions of the game implemented movement by directly updating the snake’s
head position. As the visual complexity increased, movement logic was refactored
to track directional state separately from positional updates.

User input updates the snake’s heading, and the snake advances one tile per frame
in the active direction.

The `move()` function was initially implemented as a method of the `Snake` class.
It was later extracted into a standalone function to better coordinate interactions
between the `Snake` and `Apple` objects and reduce unnecessary coupling.

### Rendering Pipeline

Rendering was originally handled by a single drawing function. As the project grew,
this logic was split into multiple rendering functions to improve readability and
allow more granular control over draw order and update timing.

The codebase was refactored multiple times throughout development to improve
clarity, modularity, and maintainability.

## Known Issue

A known rendering issue occurs when the snake collides with its own body.
Upon game-over, the sprite of the body segment that the head collides with
rotates in place. The underlying cause of this behavior remains unresolved.

## Technologies

- Python 3
- Pygame

## Project Structure


