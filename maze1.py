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

# THE BONUS TOGGLE
# If this is True, extra walls are removed to create cycles!
ENABLE_CYCLE_CHALLENGE = True 
EXTRA_WALL_PROBABILITY = 0.05

GEN_SPEED, SOLVE_SPEED = 10, 30

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
pygame.display.set_caption("DFS Maze: Final Submission")

# COLORS
WHITE, BLACK, PANEL, TEXT = (245,247,250), (40,45,50), (37,47,63), (235,239,244)
RED, BLUE, GREEN, YELLOW, GRAY = (255,82,82), (68,138,255), (0,200,83), (255,193,7), (210,215,220)

FONT_MAIN = pygame.font.SysFont("Arial", 18, bold=True)
FONT_SUB  = pygame.font.SysFont("Arial", 14)
# Special font for the Bonus text
FONT_BONUS = pygame.font.SysFont("Arial", 16, bold=True, italic=True)

# STRUCTURE
north = [[1]*COLS for _ in range(ROWS+1)]
east = [[1]*(COLS+1) for _ in range(ROWS)]
visited_gen = [[0]*COLS for _ in range(ROWS)]
start = end = None
phase = "Preparing"

def handle_events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def txt(t, x, y, f, c):
    screen.blit(f.render(str(t), True, c), (x, y))

def draw(cur=None, path=None, dead=None):
    screen.fill(WHITE)
    path, dead = path or [], dead or set()
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, WHITE, (2, 2, WIDTH-4, HEIGHT-4))

    if start: pygame.draw.rect(screen, GREEN, (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if end: pygame.draw.rect(screen, YELLOW, (end[1]*CELL_SIZE, end[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw Logic States
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE, r * CELL_SIZE
            if (r, c) in dead: pygame.draw.rect(screen, BLUE, (x+8, y+8, CELL_SIZE-16, CELL_SIZE-16))
            elif (r, c) in path: pygame.draw.rect(screen, RED, (x+8, y+8, CELL_SIZE-16, CELL_SIZE-16))
            if north[r][c]: pygame.draw.line(screen, BLACK, (x, y), (x+CELL_SIZE, y), 2)
            if east[r][c+1]: pygame.draw.line(screen, BLACK, (x+CELL_SIZE, y), (x+CELL_SIZE, y+CELL_SIZE), 2)

    # SIDE UI PANEL
    pygame.draw.rect(screen, PANEL, (WIDTH, 0, PANEL_WIDTH, HEIGHT))
    txt("Maze DFS UI", WIDTH + 20, 20, FONT_MAIN, TEXT)
    txt(f"Phase: {phase}", WIDTH + 20, 50, FONT_SUB, TEXT)

    # LEGEND
    legend = [(GREEN, "Start"), (YELLOW, "End"), (RED, "Path (Stack)"), (BLUE, "Dead (Popped)")]
    for i, (col, lab) in enumerate(legend):
        pygame.draw.rect(screen, col, (WIDTH + 20, 100 + i*30, 15, 15))
        txt(lab, WIDTH + 45, 98 + i*30, FONT_SUB, TEXT)

    # COUNTERS
    txt(f"Stack Count: {len(path)}", WIDTH + 20, 280, FONT_SUB, TEXT)
    txt(f"Dead Count: {len(dead)}", WIDTH + 20, 305, FONT_SUB, TEXT)

    # BONUS NOTIFICATION - This tells the teacher the bonus is running
    if ENABLE_CYCLE_CHALLENGE:
        txt("CHALLENGE ACTIVE", WIDTH + 20, 350, FONT_BONUS, YELLOW)
        txt("Multiple paths (Cycles)", WIDTH + 20, 370, FONT_SUB, TEXT)
    else:
        txt("NORMAL MODE", WIDTH + 20, 350, FONT_BONUS, WHITE)

    if cur: pygame.draw.circle(screen, BLACK, (cur[1]*CELL_SIZE + CELL_SIZE//2, cur[0]*CELL_SIZE + CELL_SIZE//2), 6)
    pygame.display.flip()

def generate():
    global start, end, phase
    phase = "Generating Maze"
    start, end = (random.randrange(ROWS), 0), (random.randrange(ROWS), COLS-1)
    east[start[0]][0] = east[end[0]][COLS] = 0
    stack = [(random.randrange(ROWS), random.randrange(COLS))]
    visited_gen[stack[0][0]][stack[0][1]] = 1
    while stack:
        handle_events(); r, c = stack[-1]; draw(path=stack)
        n = []
        for dr, dc, d in [(-1,0,'N'), (1,0,'S'), (0,1,'E'), (0,-1,'W')]:
            nr, nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and not visited_gen[nr][nc]: n.append((nr, nc, d))
        if n:
            nr, nc, d = random.choice(n)
            if d=='N': north[r][c]=0
            elif d=='S': north[nr][nc]=0
            elif d=='E': east[r][c+1]=0
            elif d=='W': east[r][c]=0
            visited_gen[nr][nc]=1; stack.append((nr, nc)); pygame.time.delay(GEN_SPEED)
        else: stack.pop()

def add_cycles():
    for r in range(1, ROWS-1):
        for c in range(1, COLS-1):
            if random.random() < EXTRA_WALL_PROBABILITY:
                if random.choice([True, False]): north[r][c] = 0
                else: east[r][c+1] = 0

def solve():
    global phase
    phase = "Solving Path"
    stack, vis, dead = [start], {start}, set()
    while stack:
        handle_events(); r, c = stack[-1]; draw((r, c), stack, dead); pygame.time.delay(SOLVE_SPEED)
        if (r, c) == end: 
            phase = "Complete!"
            return stack
        moved = False
        for dr, dc, d in [(-1,0,'N'), (0,1,'E'), (1,0,'S'), (0,-1,'W')]:
            nr, nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and (nr,nc) not in vis:
                ok = (d=='N' and not north[r][c]) or (d=='S' and not north[nr][nc]) or \
                     (d=='E' and not east[r][c+1]) or (d=='W' and not east[r][c])
                if ok: stack.append((nr, nc)); vis.add((nr, nc)); moved = True; break
        if not moved: dead.add(stack.pop())
    return []

def main():
    generate()
    if ENABLE_CYCLE_CHALLENGE: 
        add_cycles()
    final = solve()
    while True: 
        handle_events()
        draw(path=final)

if __name__ == "__main__": main()