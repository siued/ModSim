import matplotlib.pyplot as plt

from physics import timestep
from utils import *

np.random.seed(69)


def simulate(constants, save_plot=False):
    # we simulate traffic jams according to the equations from the 1D CA paper
    # create a road with a density of ro_0, with cars going at speed v_0
    # cars' positions are integers at the beginning
    cars = init_road(constants)

    if save_plot:
        fig, axes = init_plot(constants)

    full_speed_fraction = 0.0
    stopped_fraction = 0.0
    total_distance_covered = 0.0
    time = 0.0

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
    # save the plot
    if save_plot:
        save_results(name, constants)
        plt.show()

    return full_speed_fraction, stopped_fraction, total_distance_covered


def simulate_variable_impact(variable, min, max):
    # plot impact of acceleration on metrics
    plt.xlabel(variable)
    plt.ylabel('Metrics')

    arr1, arr2, arr3 = [], [], []

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


name = '2D_CA_model_8'

constants = {
    'initial_density': 0.10,
    'initial_velocity': 0.3,
    'max_velocity': 1.0,
    'acceleration': 0.05,
    'safety_distance': 7,
    'max_distance': 300,
    'pattern': 'random',
    'max_time': 500.0,
    'time_step': 1.0,
    'dimensions': 2,
    # maximum speed at which space-based lane change is considered as an alternative to slowing down
    'lane_change_max_speed': 0.1,
    # method used to decide when to change lanes
    # 'space-based' - change lanes when there is enough space in the other lane
    # 'speed-based' - change lanes when the speed in the other lane seems higher
    'lane_change_method': 'space-based',
    'random_slowdown_probability': 0.01
}

constants['deceleration'] = constants['acceleration'] * 2

simulate_variable_impact('random_slowdown_probability', 0.001, 0.4)
# simulate(constants, save_plot=True)
