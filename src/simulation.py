import numpy as np
import pandas as pd


def simulate_one_day(rng, params):
    infected = False
    infected_at = None
    total_contacts = 0

    for place in params["route"]:
        if infected or total_contacts >= params["max_contacts"]:
            break

        low, high = params["contacts_range"][place]
        contacts_here = rng.integers(low, high + 1)

        contacts_here = min(contacts_here,
                            params["max_contacts"] - total_contacts)

        for _ in range(contacts_here):
            if rng.random() < params["prevalence"]:
                if rng.random() < params["beta"][place]:
                    infected = True
                    infected_at = place
                    break

        total_contacts += contacts_here

    return infected, infected_at, total_contacts


def run_monte_carlo(params):
    rng = np.random.default_rng(params["seed"])

    records = []

    for run in range(params.get["runs", 0]):
        infected, place, contacts = simulate_one_day(rng, params)

        records.append({
            "run": run,
            "infected": infected,
            "infected_at": place,
            "total_contacts": contacts
        })

    df = pd.DataFrame(records)

    return df
