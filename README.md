# astro-transient-pipeline

A dependency-light, simulated multi-messenger transient triage pipeline inspired by ZTF/GROWTH workflows. It is intentionally an MVP: it generates alerts, evaluates a physics-shaped light curve, assigns a transparent taxonomy, cross-matches a mock GW localization, and produces a follow-up queue.

## Why this project exists

Modern time-domain surveys can generate far more alerts than a follow-up network can observe. This repository demonstrates the core decision path in a compact, inspectable form: turn a synthetic alert stream into astrophysical classifications, combine those classifications with a multi-messenger coincidence score, and rank the most useful targets for follow-up.

The current code is small enough to audit line by line while preserving clean boundaries for production components such as Kafka, Avro, HEALPix, trained classifiers, sky catalogs, and telescope scheduling.

## Architecture

```mermaid
flowchart LR
    A[Seeded alert simulator] --> B[Arnett-shaped flux model]
    B --> C[Color and rise-time features]
    C --> D[Transparent transient classifier]
    D --> E[Mock GW spatial overlap]
    E --> F[Priority scoring]
    F --> G[Ranked top-10 follow-up queue]
```

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m astro_transient_pipeline.pipeline --alerts 100 --seed 7
pytest
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

### Command-line options

| Option | Default | Purpose |
| --- | ---: | --- |
| `--alerts` | `100` | Number of simulated alert packets to process |
| `--seed` | `0` | Seed controlling light-curve parameters and GW overlap |

Example output from the verified run:

```text
SIM00093  priority=1.132  kilonova; GW overlap=0.84
SIM00095  priority=0.997  kilonova; GW overlap=0.54
SIM00097  priority=0.930  SN Ia; GW overlap=0.98
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

## How the ranking works

Each alert receives an interpretable class label and probability from its peak flux, rise time, and synthetic `g-r` color. The scheduler then combines the class confidence with the mock gravitational-wave overlap:

```text
priority = urgency × (0.7 × class_probability + 0.3 × gw_overlap)
```

Kilonova candidates receive an urgency multiplier of `1.5`; all other classes use `1.0`. This intentionally simple formula creates a clear baseline for later expected-information-gain or ILP scheduling experiments.

## Module guide

| Module | Responsibility |
| --- | --- |
| `lightcurve.py` | Arnett-shaped flux proxy and astronomical color index |
| `classifier.py` | Rule-based taxonomy for kilonovae, SN Ia, SN II, and AGN flares |
| `scheduler.py` | Multi-messenger priority score and bounded follow-up queue |
| `pipeline.py` | Alert simulation, orchestration, CLI parsing, and formatted results |
| `tests/test_pipeline.py` | Determinism, queue length, and descending-priority checks |

## Validation and reproducibility

```bash
python -m astro_transient_pipeline.pipeline --alerts 100 --seed 7
python -m compileall -q src
pytest
```

`tests/test_pipeline.py` verifies that a seeded 20-alert run produces a deterministic, descending top-10 priority queue. GitHub Actions repeats the test after installing the optional development dependency set.

## Current limitations

- Alerts are generated in memory rather than consumed from Kafka or Avro packets.
- The light-curve equation is a normalized teaching proxy, not a radiative-transfer model.
- Classification thresholds are illustrative and are not trained on survey data.
- GW overlap is a seeded scalar rather than an integral over a HEALPix probability map.
- The scheduler ranks candidates but does not yet model visibility, telescope slew, weather, or exposure constraints.

## Roadmap

1. Add typed alert schemas and an Avro/Kafka adapter.
2. Introduce HEALPix sky-map correlation and catalog cross-matching.
3. Replace the rule baseline with calibrated probabilistic classifiers.
4. Add airmass-aware scheduling and telescope constraints.
5. Stream results into an interactive Bokeh sky dashboard.

The full research plan is represented by package boundaries for ingest, light curves, classification, multi-messenger correlation, and scheduling. Production integrations (Kafka, Avro, HEALPix, Bokeh, and PostgreSQL) are deliberately optional next steps, not hard requirements for the first runnable demo.

## Layout

- `src/astro_transient_pipeline/`: runnable simulation and domain modules
- `models/`, `data/`, `notebooks/`, `dashboard/`: reserved asset and interface locations
- `tests/`: deterministic MVP tests
