# Flappy Bird Multiplayer

## Game Description

This is a multiplayer version of the classic Flappy Bird game implemented in Python using the Pygame library. Two players can compete simultaneously in the same game session. Player 1 controls their bird using mouse clicks, while Player 2 uses keyboard controls (SPACE or UP arrow keys). The objective is to navigate the birds through a series of pipes without colliding with them or the ground/top boundaries. Each pipe successfully passed awards points to the respective player. The game features high score tracking, dynamic visual effects, and adjustable difficulty settings.

## How to Play

- **Player 1 (Mouse Control)**: Click the left mouse button to make the bird flap upward and counteract gravity. The bird will fall if no input is provided.
- **Player 2 (Keyboard Control)**: Press the SPACE bar or UP arrow key to make the bird flap. Similar to Player 1, the bird falls due to gravity without input.

The game begins when either player makes their first move (jump/flap). Both players play on the same screen with the same obstacles. The game ends when both birds have collided with pipes or boundaries. Scores are tracked individually, and the highest score achieved is saved as the high score.

## Features

- **Multiplayer Support**: Two-player simultaneous gameplay with different control schemes.
- **Individual Scoring**: Each player earns points separately for pipes passed.
- **High Score Persistence**: The best score (maximum of both players' scores) is saved to `highscore.txt`.
- **Visual Effects**: Bird animation, rotation based on velocity, scrolling background, clouds, and ground.
- **Difficulty Adjustments**: Adjustable FPS via F6/F7 keys to change game speed.
- **Debug Features**: Toggle collision detection (F2), reset game (R), clear high score (F10).
- **Responsive Design**: Game uses a virtual resolution scaled to fit any window size while preserving aspect ratio.

## Code Overview

The game script `FlappyBird.py` is structured as follows:

### Initialization and Setup

- **Imports**: Essential modules like `pygame`, `random`, `sys`, `os` are imported.
- **resource_path(relative_path)**: A utility function to handle file paths, especially for bundled executables created with tools like PyInstaller.
- **Timing and Resolution**: Sets up a clock for FPS control (default 60 FPS), defines a virtual resolution (648x702) for consistent gameplay, and creates a resizable window that scales the virtual surface.
- **Display Setup**: Initializes Pygame, sets window caption to "Flappy Bird - Multiplayer", and prepares surfaces for drawing.

### Asset Loading

- **Images**: Loads background, ground, restart button, game over text, cloud sheets, bird animation frames for both players, and pipe images. Images are scaled appropriately (e.g., birds to 51x36 pixels, clouds downscaled by 0.6).
- **Fonts**: Defines fonts for UI text - "Bauhaus 93" for scores and "Consolas" for FPS display.
- **Colors**: Predefines color constants like WHITE, YELLOW, BLUE, etc., for consistent theming.

### Game Variables and Constants

- **Physics**: `scrollSpeed = 4`, `birdFallSpeed = 8`, `birdJumpSpeed = 10`, `pipeGap = 175`, `pipeFrequency = 1500` (ms).
- **States**: `gameOver`, `startGame`, `enableCollision`, `enableInput`.
- **Scoring**: `score_p1`, `score_p2`, `high_score`.
- **Clouds**: Timer, interval (2500ms), lanes, cycle index for spawning.
- **Other**: FPS thresholds (30-120), reset cooldown, bird rotation controller (1.25).

### Utility Functions

- **load_high_score()**: Reads the high score from `highscore.txt`. Creates the file with "0" if it doesn't exist.
- **save_high_score(val)**: Writes the high score to `highscore.txt`.
- **draw_text(surface, text, font_obj, color, x, y)**: Renders text on the given surface at specified position.
- **draw_text_shadow(surface, text, font_obj, color, x, y, shadow_offset=2)**: Draws text with a black shadow for better visibility.
- **reset_game()**: Resets all game elements - empties pipe group, repositions birds, resets scores and states, applies a short cooldown.
- **can_spawn_cloud()**: Checks if a new cloud can be spawned without overlapping existing ones (minimum spacing of 350 pixels).
- **spawn_cloud()**: Creates and adds a cloud sprite in a random lane, cycling through cloud images.
- **handle_scoring()**: Checks if birds have passed pipes and awards points accordingly (score_p1 for mouse player, score_p2 for keyboard).
- **handle_collisions()**: Detects collisions between birds and pipes/ground/top, marks birds as dead, and sets game over when both are dead.
- **draw_ground(surface)**: Draws the scrolling ground by blitting the ground image twice and offsetting for seamless loop.

### Classes

- **Bird(pygame.sprite.Sprite)**: Represents a player-controlled bird.
  - \***\*init**(self, x, y, control_type, color_tag)\*\*: Initializes with position, control type ("mouse" or "keyboard"), loads appropriate frames, sets up rect and attributes.
  - **update(self)**: Applies gravity if flying and alive, handles input for jumping, updates animation frames, rotates image based on velocity (self.image = pygame.transform.rotate(self.frames[self.index], self.velocity \* -2 / birdRotationController)).
  - Attributes: frames (list of images), index (animation), counter, rect, velocity, clicked (input debounce), flying, control_type, passed_pipe, alive, color_tag.

- **Pipe(pygame.sprite.Sprite)**: Represents pipe obstacles.
  - \***\*init**(self, x, y, position)\*\*: Creates top or bottom pipe at position, flips image for top pipes.
  - **update(self)**: Moves pipe left at scrollSpeed if game started, removes when off-screen.

- **Button()**: Simple button class for restart functionality.
  - \***\*init**(self, x, y, image)\*\*: Sets position and image.
  - **draw(self, target_surface)**: Blits image (click detection handled externally).

- **Cloud(pygame.sprite.Sprite)**: Background decoration.
  - \***\*init**(self, image, lane_y)\*\*: Sets image and position in lane.
  - **update(self)**: Moves left slower than pipes (speed = max(1, scrollSpeed // 3)), removes when off-screen.

### Sprite Groups and Instances

- **birdGroup**: Contains both Bird instances (player1 and player2).
- **pipeGroup**: Manages Pipe sprites.
- **cloudGroup**: Manages Cloud sprites.
- **Players**: player1 (mouse, "P1"), player2 (keyboard, "P2").
- **UI**: button instance for restart.

### Main Game Loop

- **Event Handling**: Processes quit, key presses (toggles, controls), mouse clicks.
- **Updates**: Updates clouds, birds, pipes; spawns new pipes/clouds; handles scoring and collisions; scrolls ground.
- **Drawing**: Blits background, clouds, birds, pipes, ground, UI text (scores, high score, FPS, start prompt, game over screen).
- **Scaling and Display**: Scales virtual surface to window size preserving aspect ratio, applies letterboxing, updates display.

### Bird Flying Mechanics

Birds simulate flight through physics:

- **Gravity**: Velocity increases by 0.5 each frame when flying, capped at `birdFallSpeed` (8 pixels/frame).
- **Jumping**: Input sets velocity to `-birdJumpSpeed` (-10), causing upward movement.
- **Rotation**: Image rotates based on velocity: `rotation = velocity * -2 / birdRotationController` (controller = 1.25). Positive velocity (falling) rotates downward, negative (rising) upward, creating a tilting effect.
- **Animation**: Cycles through 3 frames every 5 frames, stopped and frozen at -90 degrees when dead.
- **Death**: Continues falling with slight backward drift, animation frozen.

### Difficulty Management

- **Base Difficulty**: Fixed parameters like pipe gap (175), spawn frequency (1500ms), scroll speed (4), ensuring consistent challenge.
- **FPS Adjustment**: F6 decreases FPS (minimum 30), F7 increases (maximum 120), affecting game speed and responsiveness. Lower FPS makes it easier, higher harder.
- **Collision Toggle**: F2 enables/disables collision detection for testing or practice.
- **Other**: Pipe heights randomized (-100 to 100), cloud spawning at fixed intervals without overlap.

### Scoring System

- **Individual Scores**: `score_p1` for Player 1, `score_p2` for Player 2, incremented when their bird passes a pipe.
- **High Score**: Max of both scores, persisted to file.
- **Total Score**: Displayed as `(score_p1 * 2) + score_p2` on game over screen.
- **Detection**: Uses pipe positions to check if bird is in gap and has passed completely.

This README provides a comprehensive overview of the game's mechanics, code structure, and features, directly referencing the implementation in `FlappyBird.py`.
