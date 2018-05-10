from enum import Enum
from cellular_automata import count_neighbors_of_state

class CellState(Enum):
    DEAD = 0
    ALIVE = 1
    JUST_BORN = 2
    JUST_DEAD = 3

colors = {CellState.DEAD: (0, 0, 0, 1),
          CellState.ALIVE: (255, 255, 255, 1),
          CellState.JUST_BORN: (0, 255, 0, 1),
          CellState.JUST_DEAD: (255, 0, 0, 1)
          }

def next_cell_state(cell, neighbors):
    nb_alive_neighbors = count_neighbors_of_state(neighbors, CellState.ALIVE) + \
                         count_neighbors_of_state(neighbors, CellState.JUST_BORN)
    nb_dead_neighbors = 8 - nb_alive_neighbors
    if cell.state == CellState.ALIVE and (nb_alive_neighbors < 2 or nb_alive_neighbors > 3):
        return CellState.JUST_DEAD
    elif cell.state == CellState.DEAD and nb_alive_neighbors == 3:
        return CellState.JUST_BORN
    elif cell.state == CellState.JUST_BORN:
        return CellState.ALIVE
    elif cell.state == CellState.JUST_DEAD:
        return CellState.DEAD
    else:
        return cell.state