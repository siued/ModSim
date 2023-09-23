import numpy as np
import matplotlib.pyplot as plt


def show_road(road):
    for car in road:
        if car is None:
            print('.', end='')
        else:
            print('o', end='')
    print()


def road_to_float(road):
    return [car.position for car in road]


def plot_road(road_floats, time, plot):
    plot.plot(road_floats, [time for _ in road_floats], 'bo', markersize=1)