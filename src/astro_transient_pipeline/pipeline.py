from __future__ import annotations

import argparse
import random

from .classifier import classify
from .lightcurve import arnett_flux, color_index
from .scheduler import rank_targets


def simulate_alerts(count: int, seed: int = 0) -> list[dict]:
    rng = random.Random(seed)
    alerts = []
    for index in range(count):
        rise_days = rng.uniform(1, 45)
        g = arnett_flux(rise_days - 18, nickel_mass=rng.uniform(0.25, 1.0)) * rng.uniform(3, 12)
        r = g * rng.uniform(0.7, 1.4)
        color = color_index(g, r)
        classification = classify(max(g, r), rise_days, color)
        alerts.append(
            {
                "id": f"SIM{index:05d}",
                "rise_days": rise_days,
                "flux_g": g,
                "flux_r": r,
                "color_g_minus_r": color,
                "classification": classification,
                "gw_overlap": rng.random(),
            }
        )
    return alerts


def run(count: int, seed: int = 0) -> list:
    return rank_targets(simulate_alerts(count, seed))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a simulated transient triage shift.")
    parser.add_argument("--alerts", type=int, default=100)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    for target in run(args.alerts, args.seed):
        print(f"{target.alert_id}  priority={target.priority:.3f}  {target.reason}")


if __name__ == "__main__":
    main()
