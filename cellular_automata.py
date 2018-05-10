import pygame
import sys
from enum import Enum
import random
import copy
import argparse

from os import listdir
from os.path import isfile
import importlib

#from highlife import *

cellular_automata = None


class Grid():
    def __init__(self, num_cells_x, num_cells_y, cell_size):
        global cellular_automata
        self.size = num_cells_x
        self.cells = [[Cell(i, j, cell_size, cellular_automata.CellState(0)) for j in range(num_cells_y)] for i in range(num_cells_x)]
        
    def draw(self, screen):
        for cell_row in self.cells:
            for cell in cell_row:
                cell.draw(screen)
        
        pygame.display.flip()
                
    def update(self):
        global cellular_automata
        new_cells = copy.deepcopy(self.cells)
        for cell_row in self.cells:
            for cell in cell_row:
                # next state of each cell depending of cellular automata we want
                new_cells[cell.x][cell.y].state = cellular_automata.next_cell_state(cell, cell.get_neighbors(self))

        self.cells = new_cells
                
class Cell():
    def __init__(self, x, y, size, state):
        self.x = x
        self.y = y
        self.size = size
        self.state = state
        
    def draw(self, screen):
        global cellular_automata
        rect_border = pygame.Rect(self.x * self.size, self.y * self.size, self.size, self.size)
        rect_fill = pygame.Rect(self.x * self.size + 1, self.y * self.size + 1, self.size - 2, self.size - 2)
        
        pygame.draw.rect(screen, pygame.Color(255,255,255,1), rect_border)
        pygame.draw.rect(screen, cellular_automata.colors[self.state], rect_fill)

    def get_neighbors(self, grid):
        neighbors = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                neighbor_x = i + self.x
                neighbor_y = j + self.y
                if ((i, j) != (0, 0) and
                    neighbor_x >= 0 and neighbor_x < grid.size and 
                    neighbor_y >= 0 and neighbor_y < grid.size):
                    
                    neighbors.append(grid.cells[neighbor_x][neighbor_y])

        return neighbors
        
def count_neighbors_of_state(neighbors, state):
    count = 0
    for neighbor in neighbors:
        if neighbor.state == state:
            count += 1
    return count

"""
    for i in range(-1, 2):
        for j in range(-1, 2):
            neighbor_x = i + cell.x
            neighbor_y = j + cell.y
            if ((i, j) != (0, 0) and
                neighbor_x >= 0 and neighbor_x < grid.size and 
                neighbor_y >= 0 and neighbor_y < grid.size and
                grid.cells[neighbor_x][neighbor_y].state == state):

                count += 1
"""            


def main():
    global cellular_automata

    parser = argparse.ArgumentParser(description='Application that simulates different cellular automaton')
    parser.add_argument('-c', '--cellular-automaton', help='Which cellular automaton to launch', required=False, default="gameoflife")
    parser.add_argument('-s', '--grid-size', help='Size of the grid to use', required=False, default=30, type=int)
    args = parser.parse_args()

    if args.cellular_automaton + ".py" in [f for f in listdir() if isfile(f)]:
        cellular_automata = importlib.import_module(args.cellular_automaton)
    else:
        print("Cannot find " + args.cellular_automaton + ".py file.")
        sys.exit()
    
    running = False
    grid_size = args.grid_size

    pygame.init()
    
    win_size = width, height = 600, 600
    
    screen = pygame.display.set_mode(win_size)

    cell_size = width / grid_size
    grid = Grid(grid_size, grid_size, cell_size)
    
    grid.draw(screen)

    while True:
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    running = not running

        if running:
            grid.update()
            grid.draw(screen)

            pygame.time.delay(200)
        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and (pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]):
                    if pygame.mouse.get_pressed()[0]: increment = 1
                    else: increment = -1
                
                    mouse_pos = pygame.mouse.get_pos()
                    clicked_cell_coord = (int(mouse_pos[0] / cell_size), int(mouse_pos[1] / cell_size))
                    grid.cells[clicked_cell_coord[0]][clicked_cell_coord[1]].state = \
                        cellular_automata.CellState((grid.cells[clicked_cell_coord[0]][clicked_cell_coord[1]].state.value + increment) % len(cellular_automata.CellState))
                    grid.draw(screen)

if __name__ == "__main__":
    main()