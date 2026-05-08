﻿# DFS Maze Generator & Solver

## Project Overview

This project implements a fully animated Maze Generator and Solver using Python and Pygame.

The maze is generated using a Depth-First Search (DFS) Recursive Backtracking algorithm, where an imaginary “mouse” carves paths through walls to create a valid maze structure.

Once the maze is generated, another DFS-based backtracking solver automatically finds a path from the randomly generated entrance to the exit while visually showing:

- Current traversal path  
- Dead-end backtracking  
- Stack behavior  
- Real-time maze exploration  

The project also includes a Bonus Challenge Mode that introduces cycles into the maze by randomly removing extra walls.

---

## Features

- Perfect maze generation using DFS  
- Stack-based recursive backtracking  
- Animated real-time visualization  
- Dynamic DFS maze solver  
- Dead-end detection and visualization  
- Interactive UI side panel  
- Randomized start and end positions  
- Optional cycle-generation challenge mode  
- Clean algorithm visualization using Pygame  

---

## Algorithms Used

### 1. Maze Generation — DFS Recursive Backtracking

The maze generation process works as follows:

1. Start from a random cell  
2. Mark the cell as visited  
3. Randomly select an unvisited neighboring cell  
4. Remove the wall between the cells  
5. Push the current cell onto a stack  
6. Continue exploration recursively  
7. Backtrack when no unvisited neighbors remain  

This creates a **Perfect Maze**, meaning:

- Every cell is reachable  
- No isolated sections exist  
- Exactly one unique path exists between any two cells  

---

### 2. Maze Solving — DFS Backtracking

The maze solver uses another DFS-based traversal algorithm:

1. Begins at the start cell  
2. Moves only through open paths  
3. Tracks visited cells  
4. Backtracks when reaching dead ends  
5. Continues until the exit is found  

---

## Visualization Colors

| Color | Meaning |
|---|---|
| Green | Start Position |
| Yellow | End Position |
| Red | Current DFS Path |
| Blue | Dead-End / Backtracked Cell |

---

## Maze Representation

The maze uses two 2D arrays:

```
north[row][col]
east[row][col]
```

### Wall Meaning

| Value | Meaning |
|---|---|
| 1 | Wall Exists |
| 0 | Open Passage |

This structure efficiently represents all maze connections while avoiding redundant wall storage.

---

## Bonus Challenge Mode

The project includes an optional challenge mode:

```
ENABLE_CYCLE_CHALLENGE = True
```

When enabled:

- Extra random walls are removed  
- Cycles are introduced into the maze  
- Multiple possible paths can exist  
- The maze is no longer a perfect tree  

This demonstrates how DFS behaves in graphs containing cycles.

---

## User Interface

The application includes a live side panel displaying:

- Current program phase  
- Stack size  
- Number of dead ends  
- Color legend  
- Challenge mode indicator  

The maze generation and solving processes are fully animated in real time.

---

## Installation

### Requirements

- Python 3.11+  
- Pygame  

### Install Dependencies

```
pip install pygame
```

---

## Running the Project

Run the program using:

```
python maze.py
```

---

## Loom Demonstration

https://www.loom.com/share/b44d4b0ee58a4311bbddf2bbcac6cea5

---

## Author

| Information | Details |
|---|---|
| Name | MULUALEM GEBREEGZIABHER |
| ID No | UGR/2363/16 |

---

## Project Information

Data Structures & Algorithms Project implemented using Python and Pygame.

Developed as a university project focused on:

- Graph traversal algorithms  
- DFS recursive backtracking  
- Algorithm visualization  
- Interactive animation using Pygame  

---

## Final Notes

This project demonstrates how graph traversal algorithms can be visualized interactively through maze generation and pathfinding simulations.

The implementation focuses on:

- Clean algorithmic structure  
- Visual clarity  
- Educational demonstration  
- Interactive animation  