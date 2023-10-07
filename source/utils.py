import json
import os
import shutil

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from car import Car


def get_car_positions(cars, lane):
    return [car.position for car in cars if car.lane == lane]


# plot lane 0 in blue, lane 1 in red
def add_positions_to_plot(cars, time, axes):
    colormap = {0: 'b', 1: 'r', 2: 'g', 3: 'y', 4: 'm', 5: 'c'}
    for i in range(len(axes)):
        positions = get_car_positions(cars, i)
        axes[i].plot(positions, [time for _ in positions], colormap[i] + 'o', markersize=0.2, fillstyle='full')


def init_plot(constants):
    matplotlib.rcParams["figure.dpi"] = 500
    fig, axes = plt.subplots(1, constants['dimensions'])
    if constants['dimensions'] == 1:
        axes = [axes]
    for ax, i in zip(axes, range(len(axes))):
        ax.set_xlim(0, constants['max_distance'])
        ax.set_ylim(constants['max_time'], 0)
        ax.set_xlabel('Position')
        ax.set_ylabel('Time')
        # ax.xaxis.set_label_position('top')
        ax.xaxis.tick_top()
        ax.set_title(f'Lane {i}')

        if i != 0:
            ax.yaxis.set_label_position('right')
            ax.yaxis.tick_right()
    return fig, axes


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

        cars.append(Car(pos, constants, lane=np.random.randint(constants['dimensions'])))

    return cars


def save_results(name, constants):
    full_path = os.path.join('../results', f'{name}')

    if os.path.exists(full_path):
        if input('overwrite?') == 'y':
            shutil.rmtree(full_path)
        else:
            print('didn\'t save')
            return

    os.mkdir(full_path)

    plt.savefig(os.path.join(full_path, 'fig.png'), dpi=1000)

    with open(os.path.join(full_path, 'constants.json'), 'w') as f:
        json.dump(constants, f, indent=4)

    with open(os.path.join(full_path, 'constants.txt'), 'w') as f:
        f.write(json.dumps(constants).replace('_', ' '))
