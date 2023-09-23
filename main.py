import numpy as np
from car import car
from physics import timestep
from utils import *

np.random.seed(69)

ro_0 = 0.3
v_0 = 0.3
v_max = 1.0

d_max = 100
# we simulate traffic jams according to the equations from the 1D CA paper
# create a road with a density of ro_0, with cars going at speed v_0
# cars' positions are in steps of 1 at the beginning
road = [car(v_0, i) for i in range(int(d_max * ro_0))]

t = 0.0
t_max = 10.0
t_step = 0.05

plot = plt.plot([], [])
plt.xlim(0, d_max)
plt.ylim(t_max, 0)
plt.xlabel('Position')
plt.ylabel('Time')
plt.gca().xaxis.set_label_position('top')
plt.gca().xaxis.tick_top()

while t <= t_max:
    timestep(road, t_step)
    plot_road(road_to_float(road), t, plt)
    t += t_step

plt.show()