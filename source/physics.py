from car import *


def consider_line_change(cars, i, c):
    other_lane = 1 - cars[i].lane
    car_ahead = get_car_ahead(cars, cars[i].position, other_lane)
    car_behind = get_car_behind(cars, cars[i].position, other_lane)
    if car_ahead is None or car_ahead.position - cars[i].position > c['safety_distance']:
        if car_behind is None or cars[i].position - car_behind.position >= c['safety_distance']:
            cars[i].lane = other_lane
            # undo deceleration and accelerate because there is now space in front.
            cars[i].velocity += c['acceleration'] * 2
    # there is no point in switching lanes, so stop in the same lane
    cars[i].velocity = 0


def timestep(cars, c):
    full_speed, stopped, distance = 0.0, 0.0, 0.0

    for i in range(len(cars)):
        car_ahead = get_car_ahead(cars, cars[i].position, cars[i].lane)
        gap = car_ahead.position - cars[i].position
        if gap < 0:
            gap += c['max_distance']

        if gap < c['safety_distance']:
            cars[i].velocity -= c['acceleration']
            if cars[i].velocity <= 0:
                consider_line_change(cars, i, c)
                # cars[i].velocity = 0
        else:
            cars[i].velocity += c['acceleration']
            if cars[i].velocity > c['max_velocity']:
                cars[i].velocity = c['max_velocity']
        if cars[i].velocity == c['max_velocity']:
            full_speed += 1
        if cars[i].velocity == 0:
            stopped += 1
        distance += cars[i].velocity * c['time_step']
        cars[i].position = cars[i].position + cars[i].velocity * c['time_step']
    cars.sort(key=lambda car: car.position)

    return full_speed, stopped, distance