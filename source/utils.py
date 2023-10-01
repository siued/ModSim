import json
import os

import numpy as np
import matplotlib.pyplot as plt
from car import Car


def get_car_positions(cars):
    return [car.position for car in cars]


def add_positions_to_plot(cars, time):
    positions = get_car_positions(cars)
    plt.plot(positions, [time for _ in positions], 'bo', markersize=1)


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
    if constants['pattern'] == 'random':
        for i in range(int(constants['initial_density'] * constants['max_distance'])):
            pos = np.random.randint(constants['max_distance'])
            while any(map(lambda car: car.position == pos, cars)):
                pos = np.random.randint(constants['max_distance'])
            cars.append(Car(pos, constants))
    elif constants['pattern'] == 'uniform':
        for i in range(int(constants['initial_density'] * constants['max_distance'])):
            pos = i * constants['max_distance'] // int(constants['initial_density'] * constants['max_distance'])
            cars.append(Car(pos, constants))
    # jammed - cars start out in a traffic jam by uniformly placing them half a safety distance apart
    elif constants['pattern'] == 'jammed':
        for i in range(int(constants['initial_density'] * constants['max_distance'])):
            pos = i * constants['safety_distance'] / 2
            cars.append(Car(pos, constants))
    # jammed_random - cars start out in a traffic jam by randomly placing them about half a safety distance apart
    elif constants['pattern'] == 'jammed_random':
        for i in range(int(constants['initial_density'] * constants['max_distance'])):
            pos = i * np.random.randint(constants['safety_distance'] // 2)
            while any(map(lambda car: car.position == pos, cars)):
                pos = i * np.random.randint(i * constants['safety_distance'] // 2)
            cars.append(Car(pos, constants))
    else:
        print('Pattern ' + constants['pattern'] + ' not implemented')
        exit()

    return cars


def save_results(name, constants):
    full_path = os.path.join('../results', f'{name}')
    os.mkdir(full_path)

    plt.savefig(os.path.join(full_path, 'fig.png'))

    with open(os.path.join(full_path, 'constants.json'), 'w') as f:
        json.dump(constants, f, indent=4)

    with open(os.path.join(full_path, 'constants.txt'), 'w') as f:
        f.write(json.dumps(constants).replace('_', ' '))
