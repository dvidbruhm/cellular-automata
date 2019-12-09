from enum import Enum
from cellular_automata import count_neighbors_of_state

states_dict = {}
colors = {}
num_states = 8

for i in range(num_states):
    state_name = 'STEP_{}'.format(i)
    states_dict[state_name] = i

CellState = Enum('CellState', states_dict)

for i, state in enumerate(CellState):
    colors[state] = (i*(256/num_states), 0, 0, 1)

print(colors)

def next_cell_state(cell, neighbors):
    total_sum = sum(n.state.value for n in neighbors) + cell.state.value

    if cell.state.value * 9 + 2 >= total_sum:
        if cell.state.value >= 1:
            return CellState(cell.state.value - 1)
        else:
            return CellState(num_states - 1)
    else:
        return CellState(cell.state.value + 1)
