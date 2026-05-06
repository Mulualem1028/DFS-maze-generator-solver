import pygame
import sys
import random # Added for picking start/end locations

# =========================
# CONFIGURATION
# =========================
ROWS, COLS, CELL_SIZE = 20, 20, 30
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
PANEL_WIDTH = 220
WINDOW_WIDTH = WIDTH + PANEL_WIDTH

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
pygame.display.set_caption("DFS Maze Generator - Step 2")

# =========================
# COLORS
# =========================
WHITE=(245,247,250)
BLACK=(40,45,50)
GRAY=(210,215,220)
GREEN=(0,200,83)  # Color for Start
YELLOW=(255,193,7) # Color for End

# =========================
# MAZE STRUCTURE
# =========================
north = [[1]*COLS for _ in range(ROWS+1)]
east = [[1]*(COLS+1) for _ in range(ROWS)]

# NEW: Variables to track where the maze begins and ends
start = (random.randrange(ROWS), 0)
end = (random.randrange(ROWS), COLS-1)

# Open the outer walls for the entrance and exit
east[start[0]][0] = 0
east[end[0]][COLS] = 0

def handle_events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def draw():
    screen.fill(WHITE)
    
    # Draw background area
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, WHITE, (2, 2, WIDTH-4, HEIGHT-4))

    # NEW: Draw Start and End rectangles
    if start:
        r, c = start
        pygame.draw.rect(screen, GREEN, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if end:
        r, c = end
        pygame.draw.rect(screen, YELLOW, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw the walls
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE, r * CELL_SIZE
            if north[r][c]:
                pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)
            if east[r][c+1]:
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)

    # Boundary walls
    for c in range(COLS):
        if north[ROWS][c]:
            pygame.draw.line(screen, BLACK, (c*CELL_SIZE, HEIGHT), ((c+1)*CELL_SIZE, HEIGHT), 3)
    for r in range(ROWS):
        if east[r][0]:
            pygame.draw.line(screen, BLACK, (0, r*CELL_SIZE), (0, (r+1)*CELL_SIZE), 3)

    pygame.display.flip()

def main():
    while True:
        handle_events()
        draw()

if __name__ == "__main__":
    main()