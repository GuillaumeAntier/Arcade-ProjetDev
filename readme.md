# Tank Battle Game

A two-player tank battle game with predefined maps.

## Features

- Two-player tank combat
- Multiple predefined maps
- Randomly selected map at game start
- Map obstacles for strategic gameplay
- Support for both Arduino joysticks and keyboard controls

## Controls

### Arduino Joysticks
- Joystick 1: Controls Player 1's tank
- Joystick 2: Controls Player 2's tank
- Button A: Fire
- Button B: Not used currently

### Keyboard Controls (when Arduino is not connected)
#### Player 1:
- W, A, S, D: Move tank
- Space: Fire
- Q: Not used currently

#### Player 2:
- Arrow keys: Move tank
- Enter: Fire
- Right Shift: Not used currently

### Game Controls
- R: Reset the game with a new random map

## Maps

The game includes several predefined maps:

1. **Empty Arena**: A simple open area with no obstacles
2. **Four Corners**: Four large obstacles in each corner of the map
3. **Central Fortress**: A central fortress with small obstacles in the corners
4. **Maze**: A maze-like map with vertical and horizontal walls
5. **Corridors**: A map with corridor-like passages

## How to Play

1. Start the game
2. A random map will be selected
3. Control your tank to navigate the map
4. Shoot the other player to reduce their health
5. The last player standing wins
6. Press R to reset the game with a new random map

## Requirements

- Python 3.x
- Pygame
- Arduino (optional for joystick controls)

## Installation

1. Install Python 3.x
2. Install Pygame: `pip install pygame`
3. Install pyserial (for Arduino communication): `pip install pyserial`
4. Place tank and bullet images in the 'graphics' folder:
   - green-tank-00.png through green-tank-05.png
   - red-tank-00.png through red-tank-05.png
   - bullet.png

## Running the Game

Run the game with: `python main.py`