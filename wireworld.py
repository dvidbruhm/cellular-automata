from enum import Enum
from cellular_automata import count_neighbors_of_state

class CellState(Enum):
    EMPTY = 0
    ELECTRON_HEAD = 1
    ELECTRON_TAIL = 2
    CONDUCTOR = 3

colors = {CellState.EMPTY: (0,0,0,255),
          CellState.ELECTRON_HEAD: (0,0,255,255),
          CellState.ELECTRON_TAIL: (255,0,0,255),
          CellState.CONDUCTOR: (255,255,0,255)}

def next_cell_state(cell, neighbors):
    if cell.state == CellState.ELECTRON_HEAD:
        return CellState.ELECTRON_TAIL
    elif cell.state == CellState.ELECTRON_TAIL:
        return CellState.CONDUCTOR
    elif cell.state == CellState.CONDUCTOR and count_neighbors_of_state(neighbors, CellState.ELECTRON_HEAD) in [1, 2]:
        return CellState.ELECTRON_HEAD
    else:
        return cell.state