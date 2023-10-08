import matplotlib.pyplot as plt

from physics import timestep
from utils import *

np.random.seed(69)


# run the simulation once with the given constants
# save_plot: a plot will be created and saved if this is True
# returns the fraction of time spent at full speed, stopped and
# the fraction of the total possible distance covered
def simulate(constants, save_plot=False):
    cars = init_road(constants)

    if save_plot:
        fig, axes = init_plot(constants)

    full_speed_fraction = 0.0
    stopped_fraction = 0.0
    total_distance_covered = 0.0
    time = 0.0

    # run the simulation
    while time <= constants['max_time']:
        full_speed, stopped, distance = timestep(cars, constants)

        if save_plot:
            add_positions_to_plot(cars, time, axes)

        time += constants['time_step']

        full_speed_fraction += full_speed
        stopped_fraction += stopped
        total_distance_covered += distance

    # calculate the fractions of time spent at full speed and stopped
    full_speed_fraction = (full_speed_fraction * constants['time_step']) / (len(cars) * (time))
    stopped_fraction = (stopped_fraction * constants['time_step']) / (len(cars) * (time))

    # calculate the fraction of the total possible distance covered
    total_distance_covered = total_distance_covered / (len(cars) * constants['max_time'] * constants['max_velocity'])

    if save_plot:
        save_results(name, constants)
        plt.show()

    return full_speed_fraction, stopped_fraction, total_distance_covered


# run the simulation multiple times, varying one constant
# and plot the impact of that constant on the metrics
def simulate_variable_impact(variable, min, max):

    plt.xlabel(variable)
    plt.ylabel('Metrics')

    arr1, arr2, arr3 = [], [], []

    # range of the variable
    values = np.linspace(min, max)

    for value in values:
        constants[variable] = value

        full_speed_fraction, stopped_fraction, total_distance_covered = simulate(constants)

        arr1.append(full_speed_fraction)
        arr2.append(stopped_fraction)
        arr3.append(total_distance_covered)

    plt.plot(values, arr1, 'b')
    plt.plot(values, arr2, 'r')
    plt.plot(values, arr3, 'g')

    plt.legend(['Full speed fraction', 'Stopped fraction', 'Total distance covered'])

    name = '2D_CA_model_' + variable + '_impact'
    save_results(name, constants)
    plt.show()


# name of the simulation run
# results will be saved under 'results/name/' as a png, json and txt files
name = '2D_CA_model_10'

# the constants for the simulation
constants = {
    'initial_density': 0.12,
    'initial_velocity': 0.3,
    'max_velocity': 1.0,
    'acceleration': 0.2,
    'safety_distance': 7,
    'max_distance': 300,
    # initial car distribution pattern
    'pattern': 'random',
    'max_time': 500.0,
    'time_step': 1.0,
    # number of lanes. currently only 1 or 2 are supported
    'dimensions': 2,
    # maximum speed at which space-based lane change is considered as an alternative to slowing down
    'lane_change_max_speed': 0.1,
    # method used to decide when to change lanes
    # 'space-based' - change lanes when there is enough space in the other lane
    # 'speed-based' - change lanes when the speed in the other lane seems higher
    'lane_change_method': 'space-based',
    'random_slowdown_probability': 0.0
}

# braking is assumed to be twice the acceleration
# if braking is too low relative to max_velocity and safety-distance, cars will crash into each other
constants['deceleration'] = constants['acceleration'] * 2

# simulate_variable_impact('acceleration', 0.04, 1.0)
simulate(constants, save_plot=True)
