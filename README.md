# Imposter Race 🎮

Imposter Race is a local multiplayer game where players try to blend in with AI characters while racing to the finish line. Players can only make one decisive move to eliminate a character and must avoid standing out until the final sprint.

## ⚡ Features

Local multiplayer (up to 4 players) with controllers.

AI characters blend in, making it harder to spot human players.

One-shot elimination mechanic for human players.

Fullscreen mode with automatic scaling and centered game field.

## 🖥️ Installation

Install Python 3.10+ from python.org

Clone or download the project repository:
git clone <repository-url>

Navigate into the project folder:
cd <project-folder>

Install the required Python dependency:
pip install pygame

Run the game:
python main.py

## 🎮 Fullscreen & Display

The game automatically scales to fullscreen while keeping the game field proportional.

The game field is centered with a black background.

Press ESC to exit fullscreen and close the game.

## 🎮 Controls

- **Joystick/Gamepad**:  
  - Movement buttons → Move the player
  - Button 0 → Shoot (once per round)  
  - Button 1 → Walk
  - Button 2 → Run (end sprint)
  - Butto 3 → Blink/Taunt
- **ESC** → Quit the game immediately. 

Only human players can perform actions. AI characters have limited behaviors to stay inconspicuous.

## ⚙️ Game Mechanics

Players are assigned to randomly chosen characters.

First players will need to find out, which character is theirs.

AI characters move and idle to mimic human players.

Players try to avoid standing out while racing.

Players get one shot each to shoot a suspect and take him out of the game.

The finish line determines the winner.


## 📝 Credits

Developed in Python using Pygame.

Assets (characters, fonts, sounds) are included in the assets folder.

Inspired by the indie game Hidden in Plain Sight.
