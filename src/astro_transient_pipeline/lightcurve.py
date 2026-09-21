from __future__ import annotations

import math


def arnett_flux(days_since_peak: float, nickel_mass: float = 0.6, diffusion_days: float = 18.0) -> float:
    """A normalized, positive Type-Ia-like light-curve proxy.

    This is a pedagogical approximation; do not use it for physical inference.
    """
    t = max(days_since_peak + diffusion_days, 0.01)
    return nickel_mass * math.exp(-t / 111.3) * (1 - math.exp(-t * t / diffusion_days**2))


def color_index(flux_g: float, flux_r: float) -> float:
    return -2.5 * math.log10(max(flux_g, 1e-12) / max(flux_r, 1e-12))
