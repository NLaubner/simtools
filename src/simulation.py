"""
Monte Carlo simulation of influenza infection risk at a university campus.

A student visits several campus locations ("spots). For each spot, the number 
of people present is sampled randomly and the probability of infection is 
computed based on duration, crowd size and infection parameters.
"""

import json
import math
import numpy as np
import pandas as pd


def load_config(path="configs/params.json"):
    """Load simulation parameters from a JSON file.
    Parameters
    
    path : str
        Path to JSON config file.

    Returns

    dict
        Simulation parameters.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    

def p_infection(duration_min, infectious_people, beta_per_minute, multiplier=1.0):
    """Return infection probability for a single spot visit.
    Parameters

    duration_min : int
        Time spent at spot in minutes.
    infectious_people : int
        Number of infectious individuals.
    beta_per_minute : float
        Transmission rate per minute. 
    multiplier : float
        Spot-specific risk factor

    Returns

    float
        Infection probability.
    """
    if infectious_people <= 0:
        return 0.0
    lam= beta_per_minute * multiplier * duration_min * infectious_people
    return 1.0 - math.exp(-lam)


def run_monte_carlo(cfg, return_details=True):
    """Run Monte Carlo Simulation and return results and summary
    
    Parameters

    cfg : dict
        Simulation configuration.
    return_details : bool
        Return per-run details if True

    Returns

    pandas.DataFrame
        Simulation results.
    pandas.DataFrame
        Summary statistics.
    """
    rng = np.random.default_rng(cfg["seed"])
    n = cfg["n_simulations"]

    route = cfg["route"]
    spots = cfg["spots"]
    p_inf_people = cfg["p_infectious"]
    beta = cfg["beta_per_minute"]

    infection_spots = []
    rows = []

    # Each iteration represents one simulated day of the student
    for i in range(n):
        infected = False
        infected_at = None
        row = {"run": i}
       
        # Student visits campus locations sequentially, infection stops the process
        for spot_name in route:
            s = spots[spot_name]
            duration = s["duration_min"]
            n_people = int(rng.integers(s["people_min"], s["people_max"]+ 1))
            n_infectious = int(rng.binomial(n_people, p_inf_people))
            mult = s.get("multiplier", 1.0)

            p = p_infection(duration, n_infectious, beta, mult)

            if return_details:
                row[f"{spot_name}_people"] = n_people
                row[f"{spot_name}_infectious"] = n_infectious

            if (not infected) and (rng.random() < p):
                infected = True
                infected_at = spot_name

        infection_spots.append(infected_at)
        if return_details:
            row["infected"] = infected_at is not None
            row["infection_spot"] = infected_at
            rows.append(row)

    overall = sum(s is not None for s in infection_spots) / n
    per_spot = {spot: sum(s == spot for s in infection_spots) / n for spot in route}

    summary = pd.DataFrame(
        [{"metric": "overall_infection_probability", "value": overall}]
        + [{"metric": f"p_infection_happens_at_{spot}", "value": per_spot[spot]} for spot in route]

    )

    results = pd.DataFrame(rows) if return_details else pd.DataFrame(
        {"infection_spot": infection_spots}

    )

    return results, summary
