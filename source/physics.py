def timestep(cars, c):
    for i in range(len(cars)):
        if (i + 1) % len(cars) == 0:
            gap = cars[0].position - cars[i].position + c['max_distance']
        else:
            gap = cars[i + 1].position - cars[i].position

        if gap < c['safety_distance']:
            cars[i].velocity -= c['acceleration']
            if cars[i].velocity < 0:
                cars[i].velocity = 0
        else:
            cars[i].velocity += c['acceleration']
            if cars[i].velocity > c['max_velocity']:
                cars[i].velocity = c['max_velocity']
        cars[i].position = cars[i].position + cars[i].velocity * c['time_step']
    cars.sort(key=lambda car: car.position)
