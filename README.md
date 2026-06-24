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

## Heuristic Function

The heuristic used by the A* algorithm consists of two components:

h(n)=h₁(n)+h₂(n)

where:

- **h₁(n)**: Sum of the minimum Manhattan distances between each box and its nearest goal.
- **h₂(n)**: Distance from the player to the nearest box, estimated using Iterative Deepening Search (IDS).

The final heuristic value is therefore:

h(n) = Σ min(ManhattanDistance(Boxᵢ, Goalⱼ))
       + IDS(Player, NearestBox)

This heuristic combines box-to-goal proximity with player accessibility, providing a more informed estimate of the remaining effort required to solve the puzzle.

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

The `IDSPlayertobox(...)` method computes the distance between the player and the nearest reachable box using **Iterative Deepening Search (IDS)**.

IDS was selected instead of Breadth-First Search (BFS) because BFS must store all nodes of the current frontier in memory. For a branching factor **b** and solution depth **d**, BFS requires:

- **Time Complexity:** O(bᵈ)
- **Space Complexity:** O(bᵈ)

In Sokoban, the search space can become extremely large, making BFS memory-intensive.

Depth-First Search (DFS), on the other hand, requires significantly less memory:

- **Time Complexity:** O(bᵈ)
- **Space Complexity:** O(bd)

However, DFS is neither optimal nor guaranteed to find the shortest path, which is important for an accurate heuristic estimate.

IDS combines the advantages of both approaches:

- **Time Complexity:** O(bᵈ)
- **Space Complexity:** O(bd)

IDS repeatedly performs depth-limited searches with limits 0,1,2,... until a box is reached. Because shallower levels are explored first, IDS guarantees that the first solution found corresponds to the shortest player-to-box distance, similarly to BFS, while requiring memory proportional only to the search depth.

Although IDS revisits nodes across successive iterations, its overall asymptotic running time remains O(bᵈ), comparable to BFS. In practice, the additional overhead is limited because many branches are quickly discarded due to walls, invalid moves, and deadlock conditions.

As a result, IDS provides an optimal distance estimate while maintaining low memory consumption, making it particularly suitable for Sokoban environments where the state space can grow rapidly.

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


