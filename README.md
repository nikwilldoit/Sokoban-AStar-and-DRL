# SOKOBAN AI SOLVER

An AI-based solver for the classic **Sokoban** puzzle, implemented using the **A\*** search algorithm with heuristic evaluation and deadlock detection.

---

## Game Rules

At the start of the program, the user is prompted to select the desired **Sokoban level difficulty**.

- If a solution exists, **each player move** is printed until the final state is reached.
- At every step, the **heuristic value (`h`)** and the **total cost (`f`)** are displayed.
- If no solution exists, an appropriate message is printed.

### Goal State
The objective is to place **each box onto a target**.

- Each target can hold **exactly one box**
- **Multiple boxes on the same target are not allowed**
- The correspondence must be **one-to-one (1–1)**

---

## Symbol Mappings

| Symbol | Meaning              |
|------:|----------------------|
| `1`   | Player               |
| `0`   | Box                  |
| `#`   | Wall                 |
| `$`   | Target               |
| `*`   | Box on Target        |
| `+`   | Player on Target     |

---

## File Structure

- **Main.java**  
  Entry point of the application. Handles level selection, initialization, and execution of the A* solver.

- **AStarSolver.java**  
  Implements the core A* search algorithm and reconstructs the final solution path.

- **BoardUtils.java**  
  Provides utility methods for board manipulation, including move validation, board updates, player localization, state copying, and board preprocessing.

- **DeadlockDetector.java**  
  Implements deadlock detection techniques (corner and corridor deadlocks) used to cut down unsolvable states and significantly reduce the search space.

- **GameLevels.java**  
  Stores the predefined Sokoban levels used for testing and evaluation.

- **HeuristicEvaluator.java**  
  Implements the heuristic function used by A*. Combines Manhattan distance between boxes and goals with an IDS-based estimation of the player's distance to the nearest box.

- **Node.java**  
  Represents a single search state, including the board configuration, player position, path cost (`g`), heuristic value (`h`), evaluation function (`f`), and parent reference for solution reconstruction.
  
---

## Highlights

- A* search with heuristic state evaluation
- IDS-enhanced heuristic calculation
- Deadlock detection for pruning unsolvable states
- Corner and corridor deadlock recognition
- Automatic solution path reconstruction
- Step-by-step solution visualization

---

## Why IDS Instead of BFS or DFS?

The heuristic requires estimating the shortest distance between the player and the nearest box. Iterative Deepening Search (IDS) combines the completeness of Breadth-First Search (BFS) with the low memory requirements of Depth-First Search (DFS), making it particularly suitable for repeated heuristic evaluations.

Unlike BFS, IDS does not require storing an entire frontier in memory, while unlike DFS, it guarantees finding the shallowest reachable target. This provides a good balance between memory efficiency and solution quality during A* search.

---

### Example: Sokoban Hard Level Solution (A*)

The following images illustrate the execution of the **A\*** search algorithm on a **hard Sokoban level**.

- **Step 0** shows the initial state of the puzzle.
  - The heuristic value is `h = 10`
  - The total cost is `f = 10`
  - The player, boxes, walls, and targets are represented using the predefined symbol mapping.

- **Step 389** shows the final (goal) state.
  - All boxes have been successfully placed on distinct targets (1–1 correspondence).
  - The heuristic value has reached `h = 0`
  - The total path cost is `f = 389`

This example demonstrates:
- The effectiveness of the A\* algorithm on complex Sokoban configurations
- The gradual reduction of the heuristic value until the goal state is reached
- The use of deadlock detection to avoid invalid or unsolvable states
- 18 seconds for solution
  
![alt text](step0-HardLevel.png)
![alt text](step389-HardLevel.png)


