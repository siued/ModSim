Here we model and simulate. Or simulate and model, depending on what we feel like.

## To do list:
- [x] make the cars start evenly spread across the road
- [x] try out car distributions
- [x] add logic to the movement of the cars
- [x] implement physics from paper
- [x] implement a measure of the traffic-jamness of the simulation, try to find relationships between variables and the amount of traffic jam generated
- [ ] mention limitations of our sim - cars don't move in parallel but one at a time
- [x] push the zip file with older code to github @Andreea
- [ ] make a random slowdown parameter?
- [ ] make more lane change algorithms?
- [ ] make the road start with unbalanced densities
- [ ] mention that we are using no memory for the drivers
- [ ] talk about the acceleration to max speed ratio
- [ ] talk about random slowdown making graphs look chaotic, maybe more realistic
- [ ] try making random slowdown depend on something cause stochastic models and shit
- [ ] try making safety distance depend on speed - this sucks, maybe talk about it?

### Meeting 1 notes
We discussed how to implement two-lane simulation using the existing code. We discussed potential ways to simulate lane switching, like:
- Switch based on relative lane speed
- Switch based on space in other lane if stopped (or set some speed cutoff)
- Switch based on lane density <br>

We decided to save the code state as it is right now so that we have the simulation which was used to generate the 1D CA graphs. <br>
We decided to not yet look at the other 2-lane CA implementation we found on github so that we can first try to implement our own without influence. <br>
We decided to implement traffic jam metrics to be able to measure and graph the impact of changing constants on the outcome 
- A measure of the fraction of time spent at 0 speed
- The fraction of time spent at max speed
- The fraction of maximum possible distance covered (hence taking into account not just stopping jams but also ones that slow the car down)