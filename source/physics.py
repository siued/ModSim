import numpy as np

from car import *


def update_speed(car, gap, c):
    if gap < c['safety_distance']:
        car.velocity = max(car.velocity - c['deceleration'], 0)
    else:
        car.velocity = min(car.velocity + c['acceleration'], c['max_velocity'])

    if car.velocity * c['time_step'] >= gap:
        # can occur if parameters are set such that cars can't decelerate fast enough
        # relative to the safety distance and max velocity
        print('crash')


def consider_lane_change_space_based(cars, car, c, gap):
    if gap > c['safety_distance'] or car.velocity - c['deceleration'] > c['lane_change_max_speed']:
        update_speed(car, gap, c)
        return

    other_lane = 1 - car.lane
    # get cars ahead and behind in the other lane
    car_ahead = get_car_ahead(cars, car.position, other_lane)
    car_behind = get_car_behind(cars, car.position, other_lane)

    if car_ahead is None or distance_between_cars(car, car_ahead) > c['safety_distance']:
        if car_behind is None or distance_between_cars(car_behind, car) >= c['safety_distance']:
            car.lane = other_lane
            car.velocity = min(car.velocity + c['acceleration'], c['max_velocity'])
            return
    # there is no point in switching lanes, so slow down in current lane
    car.velocity = max(car.velocity - c['deceleration'], 0)


def consider_lane_change_speed_based(cars, car, c, gap):
    other_lane = 1 - car.lane
    # get cars ahead and behind in the other lane
    car_ahead = get_car_ahead(cars, car.position, other_lane)
    car_behind = get_car_behind(cars, car.position, other_lane)

    if car_ahead is None:
        # other lane is empty, use maximum speed
        other_lane_speed = c['max_velocity']
    else:
        other_lane_speed = (car_ahead.velocity + car_behind.velocity) / 2

    if gap < c['safety_distance']:
        this_lane_speed = max(car.velocity - c['deceleration'], 0)
    else:
        this_lane_speed = min(car.velocity + c['acceleration'], c['max_velocity'])

    # if other lane is empty and this lane isn't at max speed, switch lanes
    if car_ahead is None and this_lane_speed < c['max_velocity']:
        car.lane = other_lane
        car.velocity = min(car.velocity + c['acceleration'], c['max_velocity'])
        return

    # consider speed difference vs acceleration?
    # maybe add a driver politeness parameter?
    if (other_lane_speed > this_lane_speed
            and distance_between_cars(car_behind, car) > c['safety_distance']
            and distance_between_cars(car, car_ahead) >= c['safety_distance']):
        car.lane = other_lane
        gap = distance_between_cars(car, car_ahead)
        update_speed(car, gap, c)
    else:
        update_speed(car, gap, c)


def update_speed_and_lane(car, cars, c, gap):
    # one-lane road
    if c['dimensions'] == 1:
        update_speed(car, gap, c)
        return

    if c['lane_change_method'] == 'space-based':
        consider_lane_change_space_based(cars, car, c, gap)
        return

    if c['lane_change_method'] == 'speed-based':
        consider_lane_change_speed_based(cars, car, c, gap)
        return

    print('Error: invalid lane change method')
    exit()


def timestep(cars, c):
    full_speed, stopped, distance = 0.0, 0.0, 0.0

    for car in cars:
        car_ahead = get_car_ahead(cars, car.position, car.lane)
        gap = distance_between_cars(car, car_ahead)

        update_speed_and_lane(car, cars, c, gap)

        if car.velocity == c['max_velocity']:
            full_speed += 1
        if car.velocity == 0:
            stopped += 1

        if np.random.rand() < c['random_slowdown_probability']:
            # just some constant, just using deceleration is too little
            car.velocity = max(car.velocity - 2 * c['deceleration'], 0)

        distance += car.velocity * c['time_step']

        car.position = car.position + car.velocity * c['time_step']
    cars.sort(key=lambda car: car.position)

    return full_speed, stopped, distance