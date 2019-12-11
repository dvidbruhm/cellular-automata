from enum import Enum
from cellular_automata import count_neighbors_of_state

states_dict = {}
colors = {}
num_states = 64
k1 = 2
k2 = 4
g = 14

for i in range(num_states + 1):
    state_name = 'STATE_{}'.format(i)
    states_dict[state_name] = i

CellState = Enum('CellState', states_dict)

for i, state in enumerate(CellState):
    colors[state] = (i * (255 / num_states), 0, 0, 1)


def next_cell_state(cell, neighbors):
    total_sum = sum(n.state.value for n in neighbors) + cell.state.value
    nb_ill = count_neighbors_of_state(neighbors, CellState(num_states))
    nb_infected = len(neighbors) - nb_ill - count_neighbors_of_state(neighbors, CellState(0))

    if cell.state.value == 0:
        next_state = int(nb_infected/k1) + int(nb_ill/k2)

    elif cell.state.value == num_states:
        next_state = 0

    else:
        next_state = int(total_sum / (nb_infected + nb_ill + 1)) + g - 1

    if next_state > num_states:
        next_state = num_states
    return CellState(next_state)
