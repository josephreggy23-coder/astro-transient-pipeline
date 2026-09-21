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

## What is implemented today

| Stage | MVP implementation | Next research integration |
| --- | --- | --- |
| Light curves | normalized Arnett-shaped flux proxy | radiative-transfer / kilonova grids |
| Classification | four-rule transparent taxonomy | trained hierarchical Bayesian model |
| Multi-messenger context | per-alert mock GW-overlap score | HEALPix FITS and neutrino localizations |
| Scheduling | priority-ranked top-10 queue | airmass-aware ILP allocation |

The compact implementation is designed to make every ranking decision inspectable before adding Kafka, Avro, GPU models, or external sky catalogs.

## Validation and reproducibility

```bash
python -m astro_transient_pipeline.pipeline --alerts 100 --seed 7
python -m compileall -q src
pytest
```

`tests/test_pipeline.py` verifies that a seeded 20-alert run produces a deterministic, descending top-10 priority queue. GitHub Actions repeats the test after installing the optional development dependency set.

The full research plan is represented by package boundaries for ingest, light curves, classification, multi-messenger correlation, and scheduling. Production integrations (Kafka, Avro, HEALPix, Bokeh, and PostgreSQL) are deliberately optional next steps, not hard requirements for the first runnable demo.

## Layout

- `src/astro_transient_pipeline/`: runnable simulation and domain modules
- `models/`, `data/`, `notebooks/`, `dashboard/`: reserved asset and interface locations
- `tests/`: deterministic MVP tests
