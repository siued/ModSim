import json

import numpy as np
import matplotlib.pyplot as plt
from car import car


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
            cars.append(car(pos, constants))
    else:
        print('Pattern ' + constants['pattern'] + ' not implemented')

    return cars


def save_plot(name):
    plt.savefig(f'{name}.png')
