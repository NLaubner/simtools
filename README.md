# Monte Carlo simulation - Flu Spread

This project uses a Monte Carlo simulation to estimate the probability that a student becomes infected with the flu at a university campus. 


# Scenario 
The student follows a predifined route through several locations on campus, taking into account the time spent at each location and a random nummer of people present.

street -> lecture hall -> way_to_cafeteria -> cafeteria -> way_to_bib -> bib

At each location, the student spends a fixed amount of time and encounters a random number of people.

# Simulation Approach
All simulation parameters are defined in `configs/params.json`.
The simulation logic is implemented in `src/simulation.py`and executed via the notebook `notebooks/analysis.ipynb`.

The simulation outputs the overall probability of infection as well as the probability that the infection occurs at a specific location. Therefore the simulation is repeated many times to estimate infection probabilities.

--------