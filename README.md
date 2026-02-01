# Asteroids

A classic Asteroids arcade game implementation built with Python and Pygame.

## Overview

Navigate your spaceship through an asteroid field, shoot asteroids to break them apart, and avoid collisions. The game features smooth movement, shooting mechanics, and dynamic asteroid splitting.

## Features

- **Player Controls:**
  - `A` / `D` - Rotate left/right
  - `W` / `S` - Move forward/backward
  - `SPACE` - Shoot (with cooldown)

- **Game Mechanics:**
  - Continuous asteroid spawning
  - Asteroid splitting when shot (breaks into smaller pieces)
  - Collision detection between player and asteroids
  - Collision detection between shots and asteroids
  - Game over on player-asteroid collision
  - Shot cooldown system to prevent spam

- **Technical Features:**
  - 60 FPS game loop with delta time
  - Sprite group management for efficient updates
  - State and event logging for debugging/analytics
  - Configurable game constants

## Requirements

- Python >= 3.12
- pygame == 2.6.1

## Installation

This project uses `uv` for dependency management. Install dependencies with:

```bash
uv sync
```

## Running the Game

```bash
uv run main.py
```

## Project Structure

- `main.py` - Game entry point and main loop
- `player.py` - Player ship implementation
- `asteroid.py` - Asteroid entity
- `asteroidfield.py` - Asteroid spawning system
- `shot.py` - Projectile implementation
- `circleshape.py` - Base class for circular game objects
- `constants.py` - Game configuration constants
- `logger.py` - State and event logging utilities

## Game Constants

All game parameters can be adjusted in `constants.py`:
- Screen dimensions
- Player speed and turn rate
- Asteroid sizes and spawn rates
- Shot properties

# TODO

- [ ] Add a scoring system
- [ ] Implement multiple lives and respawning
- [ ] Add an explosion effect for the asteroids
- [ ] Add acceleration to the player movement
- [ ] Make the objects wrap around the screen instead of disappearing
- [ ] Add a background image
- [ ] Create different weapon types
- [ ] Make the asteroids lumpy instead of perfectly round
- [ ] Make the ship have a triangular hit box instead of a circular one
- [ ] Add a shield power-up
- [ ] Add a speed power-up
- [ ] Add bombs that can be dropped
