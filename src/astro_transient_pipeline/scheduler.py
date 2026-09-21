from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FollowUpTarget:
    alert_id: str
    priority: float
    reason: str


def rank_targets(candidates: list[dict], max_targets: int = 10) -> list[FollowUpTarget]:
    scored = []
    for item in candidates:
        probability = item["classification"].probability
        coincidence = item["gw_overlap"]
        urgency = 1.5 if item["classification"].label == "kilonova" else 1.0
        score = urgency * (0.7 * probability + 0.3 * coincidence)
        scored.append(FollowUpTarget(item["id"], round(score, 4), f"{item['classification'].label}; GW overlap={coincidence:.2f}"))
    return sorted(scored, key=lambda target: target.priority, reverse=True)[:max_targets]
