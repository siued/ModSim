class car:
    def __init__(self, speed, position):
        self.speed = speed
        self.position = position

    # loop position around the road
    def __setattr__(self, name, value):
        if name == 'position':
            if value > 100:
                value = value - 100
        super().__setattr__(name, value)