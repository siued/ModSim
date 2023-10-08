# find the closest car in front of the given position in the given lane
# returns None if there are no cars in the lane
def get_car_ahead(cars, position, lane):
    # check if there are cars in the lane
    if not any(map(lambda c: c.lane == lane, cars)):
        return None
    for car in cars:
        if car.position > position and car.lane == lane:
            return car
    # if we are here, then we need to loop around
    return next(filter(lambda c: c.lane == lane, cars))


# find the closest car behind the given position in the given lane
# returns None if there are no cars in the lane
def get_car_behind(cars, position, lane):
    # check if there are cars in the lane
    if not any(map(lambda c: c.lane == lane, cars)):
        return None
    for car in reversed(cars):
        if car.position <= position and car.lane == lane:
            return car
    # if we are here, then we need to loop around
    return next(filter(lambda c: c.lane == lane, reversed(cars)))


# get distance between two cars assuming they are in the same lane
# wrap around if needed
def distance_between_cars(car1, car2):
    if car1.position > car2.position:
        return car2.position - car1.position + car1.constants['max_distance']
    return car2.position - car1.position


class Car:
    def __init__(self, position, constants, lane=0):
        self.velocity = constants['initial_velocity']
        self.constants = constants
        self.lane = lane
        self.position = position

    # loop position around the road
    def __setattr__(self, name, value):
        if name == 'position':
            if value > self.constants['max_distance']:
                value = value - self.constants['max_distance']
        super().__setattr__(name, value)
