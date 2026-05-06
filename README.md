🧩 DFS Maze Generator & Solver
A real-time visualization of maze generation and pathfinding algorithms built with Python and Pygame. This project demonstrates the implementation of the Depth-First Search (DFS) algorithm to create "perfect" mazes and navigate through them.

🚀 Current Milestone: Grid Architecture & Logic Gates
In this second phase of development, the project has evolved from a simple window to a functional coordinate system. The focus was on establishing the "skeleton" of the maze and defining the entry and exit parameters.

Key Features Added:
Dynamic Grid Data Structure: Implementation of 2D arrays (north and east) to manage wall states independently.

Randomized Start/End Points: Automated generation of entrance (Green) and exit (Yellow) nodes on the grid boundaries using the random library.

Passage Logic: Implementation of logic to remove outer wall segments, allowing "flow" into and out of the system.

UI Framework: Enhanced rendering loop to support color-coded nodes and clean grid lines.

🛠️ Technical Details
The Coordinate System
The maze is structured as a grid of 20x20 cells. To represent walls efficiently without duplicating lines, we use two separate matrices:

North Walls: An array representing horizontal barriers.

East Walls: An array representing vertical barriers.

This dual-matrix approach allows the generation algorithm to "carve" a path by simply switching a value from 1 (Wall) to 0 (Passage) without affecting the coordinates of the surrounding cells.