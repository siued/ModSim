import json
from physics import timestep
from utils import *

np.random.seed(69)

time = 0.0

name = 'results/1D_CA_model_2'

constants = {
    'initial_density': 0.15,
    'initial_velocity': 0.3,
    'max_velocity': 1.0,
    'acceleration': 0.2,
    'safety_distance': 7,
    'max_distance': 300,
    'pattern': 'random',
    'max_time': 500.0,
    'time_step': 1.0
}

# just in case
with open(f'{name}.json', 'w') as f:
    json.dump(constants, f, indent=4)

with open(f'{name}.txt', 'w') as f:
    f.write(json.dumps(constants).replace('_', ' '))

# we simulate traffic jams according to the equations from the 1D CA paper
# create a road with a density of ro_0, with cars going at speed v_0
# cars' positions are in steps of 1 at the beginning
cars = init_road(constants)

init_plot(constants)

while time <= constants['max_time']:
    timestep(cars, constants)
    add_positions_to_plot(cars, time)
    time += constants['time_step']

# save the plot
save_plot(name)
plt.show()
