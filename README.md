#Monte Carlo simulation - Flu Spread

This project uses a Monte Carlo simulation to estimate the probability that a student becomes infected with the flu at a university campus. 
The student visits several locations on campus, taking into account the time spent at each location and a random nummer of people present.

All simulation parameters are defined in `configs/params.json`.
The simulation logic is implemented in `src/simulation.py`and executed via the notebook `notebooks/analysis.ipynb`.

The simulation outputs the overall probability of infection as well as the probability that the infection occurs at a specific location.

--------

