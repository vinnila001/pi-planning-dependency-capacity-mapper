# Architecture

## System overview

The planned system is a local Python application that reads planning inputs, validates and normalizes them, builds a dependency graph, calculates capacity and risk indicators, and writes graph/report artifacts. This repository currently provides the boundaries and configuration needed for that implementation.

## Package responsibilities

- `src/data`: input loading, validation, and normalization.
- `src/analysis`: dependency, capacity, cross-team, and risk analysis.
- `src/visualization`: graph construction and rendering.
- `src/reporting`: human-readable result summaries.
- `src/cli`: command-line orchestration.
- `src/config.py`: configurable thresholds and scoring weights.
- `src/logging_config.py`: reusable application logging setup.

## Domain model

The core domain consists of Teams, Features, Dependencies, and Planning Results. A Team owns capacity and features. A Feature has an identifier, name, owner, estimate, and dependency references. A Dependency connects a source feature to a target feature. A Planning Result contains validation findings, capacity indicators, graph data, and ranked risks.

## Processing flow

Inputs are loaded from local data boundaries, validated, normalized, analyzed, and then passed to visualization and reporting. Generated artifacts belong under `output/graphs` and `output/reports`; source inputs remain under `data/raw`, with normalized data under `data/processed`.

## Graph and analysis approach

Dependencies are modeled as a directed NetworkX graph. Directed-cycle detection identifies circular dependencies. Missing targets are validation findings. Team ownership on nodes/edges supports cross-team counts and hotspot analysis.

## Capacity and risk calculations

Capacity pressure is planned effort divided by available capacity. Warning and critical thresholds come from `config.py`. Risk scoring uses configured weights for dependency count, capacity pressure, cross-team impact, and unresolved references; scores at or above the high-risk threshold are prioritized.

## Storage and boundaries

The first version uses local files only. Raw and processed data are separate, and generated output is separate from both. No database, network service, or external integration is part of this design.

## Logging and error handling

Application modules should use the shared logger configured by `logging_config.py`. Validation errors should be reported with actionable context. Recoverable data-quality findings should be included in results; unrecoverable input or configuration errors should fail clearly at the CLI boundary.

## Testing strategy

Pytest is configured to discover tests in `tests`, use the project root and `src` on the Python path, enforce registered markers, and provide concise output. Future tests should cover validation, cycle detection, capacity thresholds, risk ranking, graph creation, and report content independently before adding end-to-end coverage.
