import json
import os
import shutil

import numpy as np
import matplotlib.pyplot as plt
from car import Car


def get_car_positions(cars, lane):
    return [car.position for car in cars if car.lane == lane]


# plot lane 0 in blue, lane 1 in red
def add_positions_to_plot(cars, time):
    lane0_positions = get_car_positions(cars, 0)
    lane1_positions = get_car_positions(cars, 1)
    plt.plot(lane0_positions, [time for _ in lane0_positions], 'bo', markersize=1)
    # plt.plot(lane1_positions, [time for _ in lane1_positions], 'ro', markersize=1)


def init_plot(constants):
    plot = plt.plot([], [])
    plt.xlim(0, constants['max_distance'])
    plt.ylim(constants['max_time'], 0)
    plt.xlabel('Position')
    plt.ylabel('Time')
    plt.gca().xaxis.set_label_position('top')
    plt.gca().xaxis.tick_top()
    return plot


def init_road(constants):
    cars = []

    for i in range(int(constants['initial_density'] * constants['max_distance'] * constants['dimensions'])):
        if constants['pattern'] == 'random':
            pos = np.random.randint(constants['max_distance'])
            while any(map(lambda car: car.position == pos, cars)):
                pos = np.random.randint(constants['max_distance'])

        elif constants['pattern'] == 'uniform':
            pos = i * constants['max_distance'] // int(constants['initial_density'] * constants['max_distance'])

        # jammed - cars start out in a traffic jam by uniformly placing them half a safety distance apart
        elif constants['pattern'] == 'jammed':
            pos = i * constants['safety_distance'] / 2

        # jammed_random - cars start out in a traffic jam by randomly placing them about half a safety distance apart
        elif constants['pattern'] == 'jammed_random':
            pos = i * np.random.randint(constants['safety_distance'] // 2)
            while any(map(lambda car: car.position == pos, cars)):
                pos = i * np.random.randint(i * constants['safety_distance'] // 2)

        else:
            print('Pattern ' + constants['pattern'] + ' not implemented')
            exit()

        cars.append(Car(pos, constants))

    return cars


def save_results(name, constants):
    full_path = os.path.join('../results', f'{name}')

    if os.path.exists(full_path) and input('delete?') == 'y':
        shutil.rmtree(full_path)
    else:
        print('didn\'t save')
        return

    os.mkdir(full_path)

    plt.savefig(os.path.join(full_path, 'fig.png'))

    with open(os.path.join(full_path, 'constants.json'), 'w') as f:
        json.dump(constants, f, indent=4)

    with open(os.path.join(full_path, 'constants.txt'), 'w') as f:
        f.write(json.dumps(constants).replace('_', ' '))
