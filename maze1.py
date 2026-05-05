import pygame
import sys

# =========================
# CONFIGURATION
# =========================
ROWS, COLS, CELL_SIZE = 20, 20, 30
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
PANEL_WIDTH = 220
WINDOW_WIDTH = WIDTH + PANEL_WIDTH

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
pygame.display.set_caption("Interactive DFS Maze Generator")

# =========================
# COLORS
# =========================
WHITE=(245,247,250)
BLACK=(40,45,50)
GRAY=(210,215,220)

# =========================
# MAZE STRUCTURE
# =========================
# 1 represents a wall, 0 represents a passage
north = [[1]*COLS for _ in range(ROWS+1)]
east = [[1]*(COLS+1) for _ in range(ROWS)]

def handle_events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def draw():
    screen.fill(WHITE)
    
    # Draw the background grid area
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, WHITE, (2, 2, WIDTH-4, HEIGHT-4))

    # Draw the walls
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE, r * CELL_SIZE
            if north[r][c]:
                pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)
            if east[r][c+1]:
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)

    # Bottom and Left boundary walls
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