import pygame

pygame.init()

info = pygame.display.Info()

WIDTH = info.current_w
HEIGHT = info.current_h
CELL_SIZE = 20
FPS = 10

# Grid
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Direções
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Controles jogador 1 (WASD)
P1_KEYS = {
    pygame.K_w: UP,
    pygame.K_s: DOWN,
    pygame.K_a: LEFT,
    pygame.K_d: RIGHT
}

# Controles jogador 2 (Setas)
P2_KEYS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT
}

# Controles jogador 3 (IJKL)
P3_KEYS = {
    pygame.K_i: UP,
    pygame.K_k: DOWN,
    pygame.K_j: LEFT,
    pygame.K_l: RIGHT
}

# Controles jogador 4 (TFGH)
P4_KEYS = {
    pygame.K_t: UP,
    pygame.K_g: DOWN,
    pygame.K_f: LEFT,
    pygame.K_h: RIGHT
}