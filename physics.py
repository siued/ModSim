def timestep(road, step):
    for car in road:
        if car is not None:
            car.position = car.position + car.speed * step
    road.sort(key=lambda car: car.position)