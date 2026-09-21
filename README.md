# astro-transient-pipeline

A dependency-light, simulated multi-messenger transient triage pipeline inspired by ZTF/GROWTH workflows. It is intentionally an MVP: it generates alerts, evaluates a physics-shaped light curve, assigns a transparent taxonomy, cross-matches a mock GW localization, and produces a follow-up queue.

## Quick start

```bash
python -m astro_transient_pipeline.pipeline --alerts 100 --seed 7
pytest
```

## MVP snapshot

| Metric | Verified demo result |
| --- | ---: |
| Simulated alert stream | 100 alerts |
| Follow-up queue | top 10 targets |
| Highest-ranked candidate | `SIM00093` (priority 1.132) |
| Kilonovae in the displayed queue | 2 |
| Reproducibility | deterministic with `--seed 7` |

These values come from `python -m astro_transient_pipeline.pipeline --alerts 100 --seed 7`. The demonstration exercises the full MVP sequence: simulated photometry, transparent classification, mock GW-overlap scoring, and follow-up ranking.

The full research plan is represented by package boundaries for ingest, light curves, classification, multi-messenger correlation, and scheduling. Production integrations (Kafka, Avro, HEALPix, Bokeh, and PostgreSQL) are deliberately optional next steps, not hard requirements for the first runnable demo.

## Layout

- `src/astro_transient_pipeline/`: runnable simulation and domain modules
- `models/`, `data/`, `notebooks/`, `dashboard/`: reserved asset and interface locations
- `tests/`: deterministic MVP tests
