from car import *


def consider_lane_change(cars, car, c):
    other_lane = 1 - car.lane
    # get cars ahead and behind in the other lane
    car_ahead = get_car_ahead(cars, car.position, other_lane)
    car_behind = get_car_behind(cars, car.position, other_lane)
    if car_ahead is None or distance_between_cars(car, car_ahead) > c['safety_distance']:
        if car_behind is None or distance_between_cars(car_behind, car) >= c['safety_distance']:
            car.lane = other_lane
            car.velocity += c['acceleration']
            return
    # there is no point in switching lanes, so stop in the same lane
    car.velocity = max(car.velocity - c['acceleration'], 0)


def timestep(cars, c):
    full_speed, stopped, distance = 0.0, 0.0, 0.0

    for car in cars:
        car_ahead = get_car_ahead(cars, car.position, car.lane)
        gap = distance_between_cars(car, car_ahead)

        if gap < c['safety_distance']:
            if car.velocity - c['acceleration'] <= 0 and c['dimensions'] > 1:
                consider_lane_change(cars, car, c)
            else:
                car.velocity = max(car.velocity - c['acceleration'], 0)
        else:
            car.velocity = min(car.velocity + c['acceleration'], c['max_velocity'])

        if car.velocity == c['max_velocity']:
            full_speed += 1
        if car.velocity == 0:
            stopped += 1
        distance += car.velocity * c['time_step']

        car.position = car.position + car.velocity * c['time_step']
    cars.sort(key=lambda car: car.position)

    return full_speed, stopped, distance