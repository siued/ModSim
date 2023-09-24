import json


class car:
    def __init__(self, position, constants):
        self.velocity = constants['initial_velocity']
        self.constants = constants
        self.position = position
        self.acceleration = 0.0

    # loop position around the road
    def __setattr__(self, name, value):
        if name == 'position':
            if value > self.constants['max_distance']:
                value = value - self.constants['max_distance']
        super().__setattr__(name, value)