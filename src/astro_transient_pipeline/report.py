from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from .pipeline import simulate_alerts
from .scheduler import rank_targets

COLORS = {
    "kilonova": "#2dd4bf",
    "SN Ia": "#60a5fa",
    "SN II": "#a78bfa",
    "AGN flare": "#fb7185",
}


def _svg_frame(title: str, body: str, subtitle: str = "") -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="560" viewBox="0 0 960 560">
<rect width="960" height="560" rx="18" fill="#07111f"/>
<text x="54" y="52" fill="#f8fafc" font-family="Segoe UI, sans-serif" font-size="25" font-weight="700">{title}</text>
<text x="54" y="78" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="14">{subtitle}</text>
{body}
</svg>'''


def _bar_chart(counts: Counter[str], total: int) -> str:
    labels = ["SN Ia", "SN II", "kilonova", "AGN flare"]
    maximum = max(counts.values(), default=1)
    bars = []
    for index, label in enumerate(labels):
        value = counts[label]
        x = 100 + index * 205
        height = 330 * value / maximum
        y = 465 - height
        bars.append(f'<rect x="{x}" y="{y:.1f}" width="120" height="{height:.1f}" rx="8" fill="{COLORS[label]}"/>')
        bars.append(f'<text x="{x + 60}" y="{y - 12:.1f}" text-anchor="middle" fill="#f8fafc" font-family="Segoe UI, sans-serif" font-size="18" font-weight="700">{value:,}</text>')
        bars.append(f'<text x="{x + 60}" y="500" text-anchor="middle" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="15">{label}</text>')
    return _svg_frame("Simulated transient population", "\n".join(bars), f"{total:,} seeded alerts • class counts from the generated CSV")


def _scatter_chart(alerts: list[dict]) -> str:
    points = []
    for alert in alerts[:700]:
        x = 75 + (alert["rise_days"] - 1) / 44 * 825
        y = 470 - (alert["color_g_minus_r"] + 0.4) / 1.2 * 350
        y = min(470, max(120, y))
        color = COLORS[alert["classification"].label]
        points.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{color}" fill-opacity="0.68"/>')
    axes = '''
<line x1="75" y1="470" x2="900" y2="470" stroke="#475569"/>
<line x1="75" y1="120" x2="75" y2="470" stroke="#475569"/>
<text x="488" y="525" text-anchor="middle" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="14">rise time (days)</text>
<text x="22" y="295" transform="rotate(-90 22 295)" text-anchor="middle" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="14">synthetic g-r color</text>'''
    return _svg_frame("Transient feature landscape", axes + "\n" + "\n".join(points), "First 700 rows from the reproducible 10,000-alert benchmark")


def build_report(output_dir: Path, alert_count: int = 10_000, seed: int = 7) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    alerts = simulate_alerts(alert_count, seed)
    ranked = rank_targets(alerts, max_targets=10)
    counts = Counter(alert["classification"].label for alert in alerts)

    with (output_dir / "alerts.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["alert_id", "rise_days", "flux_g", "flux_r", "color_g_minus_r", "class", "class_probability", "gw_overlap"])
        for alert in alerts:
            writer.writerow([
                alert["id"], f'{alert["rise_days"]:.6f}', f'{alert["flux_g"]:.8f}', f'{alert["flux_r"]:.8f}',
                f'{alert["color_g_minus_r"]:.6f}', alert["classification"].label,
                f'{alert["classification"].probability:.4f}', f'{alert["gw_overlap"]:.6f}',
            ])

    by_id = {alert["id"]: alert for alert in alerts}
    with (output_dir / "top_candidates.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["rank", "alert_id", "class", "class_probability", "gw_overlap", "priority"])
        for index, target in enumerate(ranked, start=1):
            alert = by_id[target.alert_id]
            writer.writerow([index, target.alert_id, alert["classification"].label, alert["classification"].probability, f'{alert["gw_overlap"]:.6f}', target.priority])

    summary = {
        "seed": seed,
        "alert_count": alert_count,
        "classification_counts": dict(sorted(counts.items())),
        "top_candidate": {"alert_id": ranked[0].alert_id, "priority": ranked[0].priority, "class": by_id[ranked[0].alert_id]["classification"].label},
        "displayed_queue_size": len(ranked),
    }
    (output_dir / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    (output_dir / "classification_distribution.svg").write_text(_bar_chart(counts, alert_count), encoding="utf-8")
    (output_dir / "feature_landscape.svg").write_text(_scatter_chart(alerts), encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reproducible transient benchmark data and charts.")
    parser.add_argument("--output", type=Path, default=Path("results/demo"))
    parser.add_argument("--alerts", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    print(json.dumps(build_report(args.output, args.alerts, args.seed), indent=2))


if __name__ == "__main__":
    main()
