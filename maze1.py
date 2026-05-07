import pygame
import random
import sys

# CONFIG
ROWS, COLS, CELL_SIZE = 20, 20, 30
WIDTH, HEIGHT = COLS * CELL_SIZE, ROWS * CELL_SIZE
PANEL_WIDTH = 220
WINDOW_WIDTH = WIDTH + PANEL_WIDTH
GEN_SPEED, SOLVE_SPEED = 10, 30

pygame.init(); pygame.font.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, HEIGHT))
pygame.display.set_caption("DFS Maze: Generation & Solving")

# COLORS
WHITE, BLACK, PANEL, TEXT = (245,247,250), (40,45,50), (37,47,63), (235,239,244)
RED, BLUE, GREEN, YELLOW, GRAY = (255,82,82), (68,138,255), (0,200,83), (255,193,7), (210,215,220)
FONT1, FONT2 = pygame.font.SysFont("Arial", 18, 1), pygame.font.SysFont("Arial", 14)

# STRUCTURE
north = [[1]*COLS for _ in range(ROWS+1)]
east = [[1]*(COLS+1) for _ in range(ROWS)]
visited_gen = [[0]*COLS for _ in range(ROWS)]
start = end = None
phase = "Preparing"

def handle_events():
    for e in pygame.event.get():
        if e.type == pygame.QUIT: pygame.quit(); sys.exit()

def txt(t, x, y, f, c): screen.blit(f.render(str(t), 1, c), (x, y))

def draw(cur=None, path=None, dead=None):
    screen.fill(WHITE)
    path, dead = path or [], dead or set()
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, WHITE, (2, 2, WIDTH-4, HEIGHT-4))
    if start: pygame.draw.rect(screen, GREEN, (start[1]*CELL_SIZE, start[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if end: pygame.draw.rect(screen, YELLOW, (end[1]*CELL_SIZE, end[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    for r in range(ROWS):
        for c in range(COLS):
            x, y = c * CELL_SIZE, r * CELL_SIZE
            if (r, c) in dead: pygame.draw.rect(screen, BLUE, (x+6, y+6, CELL_SIZE-12, CELL_SIZE-12))
            elif (r, c) in path: pygame.draw.rect(screen, RED, (x+6, y+6, CELL_SIZE-12, CELL_SIZE-12))
            if north[r][c]: pygame.draw.line(screen, BLACK, (x, y), (x+CELL_SIZE, y), 2)
            if east[r][c+1]: pygame.draw.line(screen, BLACK, (x+CELL_SIZE, y), (x+CELL_SIZE, y+CELL_SIZE), 2)
    if cur: pygame.draw.circle(screen, BLACK, (cur[1]*CELL_SIZE+CELL_SIZE//2, cur[0]*CELL_SIZE+CELL_SIZE//2), 7)
    pygame.draw.rect(screen, PANEL, (WIDTH, 0, PANEL_WIDTH, HEIGHT))
    txt("Maze UI", WIDTH+15, 20, FONT1, TEXT); txt(f"Phase: {phase}", WIDTH+15, 55, FONT2, TEXT)
    txt(f"Stack Size: {len(path)}", WIDTH+15, 280, FONT2, TEXT); txt(f"Popped: {len(dead)}", WIDTH+15, 305, FONT2, TEXT)
    pygame.display.flip()

def generate():
    global start, end, phase
    start, end = (random.randrange(ROWS), 0), (random.randrange(ROWS), COLS-1)
    east[start[0]][0] = east[end[0]][COLS] = 0
    phase = "Generating"
    r, c = random.randrange(ROWS), random.randrange(COLS)
    stack = [(r, c)]
    visited_gen[r][c] = 1
    while stack:
        handle_events(); draw(cur=stack[-1], path=stack); pygame.time.delay(GEN_SPEED)
        r, c = stack[-1]
        n = [(r+dr, c+dc, d) for dr, dc, d in [(-1,0,'N'), (1,0,'S'), (0,1,'E'), (0,-1,'W')] if 0<=r+dr<ROWS and 0<=c+dc<COLS and not visited_gen[r+dr][c+dc]]
        if n:
            nr, nc, d = random.choice(n)
            if d=='N': north[r][c]=0
            elif d=='S': north[nr][nc]=0
            elif d=='E': east[r][c+1]=0
            else: east[r][c]=0
            visited_gen[nr][nc]=1; stack.append((nr, nc))
        else: stack.pop()

def solve():
    global phase
    phase = "Solving"
    stack, vis, dead = [start], {start}, set()
    while stack:
        handle_events(); r, c = stack[-1]; draw((r, c), stack, dead); pygame.time.delay(SOLVE_SPEED)
        if (r, c) == end: phase = "Complete"; return stack
        moved = False
        for dr, dc, d in [(-1,0,'N'), (1,0,'S'), (0,1,'E'), (0,-1,'W')]:
            nr, nc = r+dr, c+dc
            if 0<=nr<ROWS and 0<=nc<COLS and (nr, nc) not in vis:
                ok = (d=='N' and not north[r][c]) or (d=='S' and not north[nr][nc]) or (d=='E' and not east[r][c+1]) or (d=='W' and not east[r][c])
                if ok: stack.append((nr, nc)); vis.add((nr, nc)); moved = True; break
        if not moved: dead.add(stack.pop())
    return []

def main():
    generate(); final = solve()
    while True: handle_events(); draw(path=final)

if __name__ == "__main__": main()