# DANYAL_451346_._AI_PROJECT

# Snake Game with AI (A* Algorithm) and User Control

This Python code implements a simple Snake Game using the tkinter library. The game consists of two snakes - one operated by the user and the other by an AI using the A* algorithm. The objective is for both snakes to compete for 60 seconds, and the winner is determined by the length of the snakes at the end of the time limit.

## How to Run the Game:

1. Ensure you have Python installed on your system.
2. Run the Python file using the command `python snake_game.py` in the terminal.

## Game Controls:

- **User Snake (Left Canvas):**
  - Use the arrow keys (Up, Down, Left, Right) to control the movement of the snake.

## Game Rules:

- Both snakes start with a length of 3.
- The snakes grow longer by consuming red food items.
- If a snake collides with the game boundaries or itself, the game ends for that snake.
- At the end of the 60-second time limit, the game displays the result based on the lengths of both snakes.

## Code Structure:

- **UserSnake Class:**
  - Manages the user-operated snake on the left canvas.
  - Controls snake movement and updates the game state.
  - Listens for arrow key inputs to change the snake's direction.

- **AISnake Class:**
  - Manages the AI-operated snake on the right canvas.
  - Utilizes the A* algorithm to find the optimal path to the food.
  - Handles snake movement, updates, and scoring.

- **A* Algorithm:**
  - The `astar_search` method in the `AISnake` class implements the A* algorithm to find the optimal path from the snake's current position to the food.

- **Result Display:**
  - The game displays the result (winner and lengths of both snakes) after the 60-second time limit.

## Dependencies:

- The game uses the `tkinter` library for the graphical user interface.

## Notes:

- The time limit for the game is set to 60 seconds.

Feel free to explore and modify the code to enhance or customize the game further!
