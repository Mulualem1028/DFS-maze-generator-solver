import pygame
import random
import sys

# =========================
# CONFIGURATION
# =========================
ROWS, COLS, CELL_SIZE = 20, 20, 30
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
PANEL_WIDTH = 220
WINDOW_WIDTH = WIDTH + PANEL_WIDTH

# Toggle this for your Bonus demonstration
ENABLE_CYCLE_CHALLENGE =False
EXTRA_WALL_PROBABILITY = 0.05

GEN_SPEED = 10
SOLVE_SPEED = 30

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
pygame.display.set_caption("DFS Maze Generator & Solver - Final Version")

# =========================
# COLORS
# =========================
WHITE = (245, 247, 250)
BLACK = (40, 45, 50)
PANEL = (37, 47, 63)
RED   = (255, 82, 82)   # Path
BLUE  = (68, 138, 255)  # Dead End
GREEN = (0, 200, 83)    # Start
YELLOW = (255, 193, 7)   # End
GRAY  = (210, 215, 220)
TEXT  = (235, 239, 244)

FONT1 = pygame.font.SysFont("Arial", 18, bold=True)
FONT2 = pygame.font.SysFont("Arial", 14)
FONT_B = pygame.font.SysFont("Arial", 16, bold=True, italic=True)

phase = "Preparing"

# =========================
# MAZE STRUCTURE
# =========================
north = [[1] * COLS for _ in range(ROWS + 1)]
east  = [[1] * (COLS + 1) for _ in range(ROWS)]
visited_gen = [[0] * COLS for _ in range(ROWS)]
start = end = None

# =========================
# EVENT HANDLER
# =========================
def handle_events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# =========================
# DRAW FUNCTION
# =========================
def txt(t, x, y, f, c):
    # Added str() to prevent crashes with integers
    screen.blit(f.render(str(t), True, c), (x, y))

def draw(cur=None, path=None, dead=None):
    screen.fill(WHITE)
    path = path or []
    dead = dead or set()

    # Draw Background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, WHITE, (2, 2, WIDTH - 4, HEIGHT - 4))

    # Draw Start/End Base
    if start:
        r, c = start
        pygame.draw.rect(screen, GREEN, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if end:
        r, c = end
        pygame.draw.rect(screen, YELLOW, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw Cells (Path and Dead ends)
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE, r * CELL_SIZE
            if (r, c) in dead:
                pygame.draw.rect(screen, BLUE, (x + 6, y + 6, CELL_SIZE - 12, CELL_SIZE - 12))
            elif (r, c) in path:
                pygame.draw.rect(screen, RED, (x + 6, y + 6, CELL_SIZE - 12, CELL_SIZE - 12))

            # Draw Walls
            if north[r][c]:
                pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), 2)
            if east[r][c + 1]:
                pygame.draw.line(screen, BLACK, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE), 2)

    # Draw Boundaries
    for c in range(COLS):
        if north[ROWS][c]:
            pygame.draw.line(screen, BLACK, (c * CELL_SIZE, HEIGHT), ((c + 1) * CELL_SIZE, HEIGHT), 3)
    for r in range(ROWS):
        if east[r][0]:
            pygame.draw.line(screen, BLACK, (0, r * CELL_SIZE), (0, (r + 1) * CELL_SIZE), 3)

    # Draw Cursor
    if cur:
        r, c = cur
        pygame.draw.circle(screen, BLACK, (c * CELL_SIZE + CELL_SIZE // 2, r * CELL_SIZE + CELL_SIZE // 2), 7)

    # SIDE PANEL UI
    pygame.draw.rect(screen, PANEL, (WIDTH, 0, PANEL_WIDTH, HEIGHT))
    pygame.draw.line(screen, BLACK, (WIDTH, 0), (WIDTH, HEIGHT), 2)

    txt("DFS Maze System", WIDTH + 15, 20, FONT1, TEXT)
    txt(f"Phase: {phase}", WIDTH + 15, 55, FONT2, TEXT)

    # BONUS TEXT: Only shows if challenge is enabled
    if ENABLE_CYCLE_CHALLENGE:
        txt("CHALLENGE ACTIVE", WIDTH + 15, 80, FONT_B, YELLOW)
        txt("Extra walls 'eaten'", WIDTH + 15, 100, FONT2, TEXT)

    txt("Legend:", WIDTH + 15, 130, FONT1, TEXT)
    
    # Legend Items
    pygame.draw.rect(screen, GREEN, (WIDTH + 15, 160, 15, 15))
    txt("Start Point", WIDTH + 40, 158, FONT2, TEXT)

    pygame.draw.rect(screen, YELLOW, (WIDTH + 15, 190, 15, 15))
    txt("End Point", WIDTH + 40, 188, FONT2, TEXT)

    pygame.draw.rect(screen, RED, (WIDTH + 15, 220, 15, 15))
    txt("Current Stack", WIDTH + 40, 218, FONT2, TEXT)

    pygame.draw.rect(screen, BLUE, (WIDTH + 15, 250, 15, 15))
    txt("Dead End (Popped)", WIDTH + 40, 248, FONT2, TEXT)

    # Counters
    txt(f"Stack Size: {len(path)}", WIDTH + 15, 300, FONT2, TEXT)
    txt(f"Cells Popped: {len(dead)}", WIDTH + 15, 325, FONT2, TEXT)

    pygame.display.flip()

# =========================
# GENERATE (DFS)
# =========================
def generate():
    global start, end, phase
    start = (random.randrange(ROWS), 0)
    end   = (random.randrange(ROWS), COLS - 1)
    east[start[0]][0] = 0
    east[end[0]][COLS] = 0

    phase = "Generating Maze"
    r, c = random.randrange(ROWS), random.randrange(COLS)
    stack = [(r, c)]
    visited_gen[r][c] = 1

    while stack:
        handle_events()
        r, c = stack[-1]
        draw((r, c), stack) # Passing stack to see generation path
        pygame.time.delay(GEN_SPEED)

        n = []
        for dr, dc, d in [(-1, 0, 'N'), (1, 0, 'S'), (0, 1, 'E'), (0, -1, 'W')]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and not visited_gen[nr][nc]:
                n.append((nr, nc, d))

        if n:
            nr, nc, d = random.choice(n)
            if d == 'N': north[r][c] = 0
            elif d == 'S': north[nr][nc] = 0
            elif d == 'E': east[r][c + 1] = 0
            else: east[r][c] = 0
            visited_gen[nr][nc] = 1
            stack.append((nr, nc))
        else:
            stack.pop()

# =========================
# BONUS CYCLES
# =========================
def add_cycles():
    for r in range(1, ROWS - 1):
        for c in range(1, COLS - 1):
            if random.random() < EXTRA_WALL_PROBABILITY:
                if random.choice([True, False]): 
                    north[r][c] = 0
                else: 
                    east[r][c+1] = 0

# =========================
# SOLVE (DFS)
# =========================
def solve():
    global phase
    phase = "Solving Path"
    stack = [start]
    vis = {start}
    dead = set()

    while stack:
        handle_events()
        r, c = stack[-1]
        draw((r, c), stack, dead)
        pygame.time.delay(SOLVE_SPEED)

        if (r, c) == end:
            phase = "Success!"
            return stack

        moved = False
        dirs = [(-1, 0, 'N'), (1, 0, 'S'), (0, 1, 'E'), (0, -1, 'W')]
        for dr, dc, d in dirs:
            nr, nc = r + dr, c + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and (nr, nc) not in vis:
                ok = (d == 'N' and not north[r][c]) or \
                     (d == 'S' and not north[nr][nc]) or \
                     (d == 'E' and not east[r][c + 1]) or \
                     (d == 'W' and not east[r][c])
                if ok:
                    stack.append((nr, nc))
                    vis.add((nr, nc))
                    moved = True
                    break
        if not moved:
            dead.add(stack.pop())
    return []

# =========================
# MAIN
# =========================
def main():
    generate()
    if ENABLE_CYCLE_CHALLENGE:
        add_cycles()
    
    final_solution = solve()
    
    while True:
        handle_events()
        draw(path=final_solution)

if __name__ == "__main__":
    main()