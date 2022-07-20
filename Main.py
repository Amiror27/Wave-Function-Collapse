import pygame
from Grid import Grid

pygame.init()

#grid information
GR_X_SIZE, GR_Y_SIZE = 3,3
CELL_SIZE = 143
SC_WIDTH, SC_HEIGHT = GR_X_SIZE * (CELL_SIZE+1)+1, GR_Y_SIZE * (CELL_SIZE+1)+1
CONNECTIONS = {0: (0,1), 1: (0,1,2), 2: (1,2,3), 3: (2,3)}
MAP_GRID = Grid(GR_X_SIZE, GR_Y_SIZE, 4, CONNECTIONS)

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WATER = (17, 66, 130)
SAND = (217, 192, 93)
GRASS = (147, 219, 53)
FOREST = (20, 69, 17)
TILE_COLORS = (WATER, SAND, GRASS, FOREST)


SCREEN = pygame.display.set_mode((SC_WIDTH, SC_HEIGHT), pygame.RESIZABLE, pygame.FULLSCREEN)
pygame.display.set_caption("testTEST")


def draw_BG():
    SCREEN.fill(WHITE)

    for i in range(0, SC_WIDTH, CELL_SIZE+1):
        pygame.draw.rect(SCREEN, BLACK, [i, 0, 1, SC_HEIGHT])

    for j in range(0, SC_HEIGHT, CELL_SIZE+1):
        pygame.draw.rect(SCREEN, BLACK, [0, j, SC_WIDTH, 1])


def draw_tiles():
    for i in MAP_GRID.collapsed:
        pygame.draw.rect(SCREEN, TILE_COLORS[i.possibilities[0]], [i.x*(CELL_SIZE+1)+1, i.y*(CELL_SIZE+1)+1, CELL_SIZE, CELL_SIZE])


def main():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if len(MAP_GRID.collapsed) < MAP_GRID.x_size * MAP_GRID.y_size:
            MAP_GRID.single_iteration()

        print(f'collapsed: {MAP_GRID.collapsed}')
        draw_BG()
        draw_tiles()
        pygame.display.update()
    pygame.quit()


main()
