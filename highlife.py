from enum import Enum
from cellular_automata import count_neighbors_of_state

class CellState(Enum):
    DEAD = 0
    ALIVE = 1

colors = {CellState.DEAD: (0, 0, 0, 1),
          CellState.ALIVE: (255, 255, 255, 1)}

def next_cell_state(cell, neighbors):
    nb_alive_neighbors = count_neighbors_of_state(neighbors, CellState.ALIVE)
    nb_dead_neighbors = 8 - nb_alive_neighbors
    if cell.state == CellState.ALIVE and (nb_alive_neighbors < 2 or nb_alive_neighbors > 3):
        return CellState.DEAD
    elif cell.state == CellState.DEAD and nb_alive_neighbors in [3, 6]: # Only difference with game of life
        return CellState.ALIVE
    else:
        return cell.state