from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Classification:
    label: str
    probability: float
    rationale: str


def classify(peak_flux: float, rise_days: float, color_g_minus_r: float) -> Classification:
    """Transparent baseline taxonomy for simulated alerts."""
    if rise_days < 3 and color_g_minus_r < 0.15:
        return Classification("kilonova", 0.72, "fast, blue evolution")
    if 12 <= rise_days <= 25 and -0.2 <= color_g_minus_r <= 0.8:
        return Classification("SN Ia", 0.91, "Ia-like cadence and color")
    if peak_flux > 4 and rise_days > 30:
        return Classification("AGN flare", 0.67, "bright, slowly evolving source")
    return Classification("SN II", 0.58, "default slow transient class")
