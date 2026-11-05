# Risk Scoring

Risk scoring provides a consistent way to prioritize dependency, capacity, and feature-level risks. Scores are normalized to `0.0–1.0`; higher values indicate greater planning attention. The configured high-risk threshold is `0.70`.

## Shared formula

For a risk record, calculate the available factor values, normalize each to `0.0–1.0`, and apply the configured weights:

```text
score = Σ (factor_value × factor_weight)
```

The initial weights are:

| Factor | Weight | Interpretation |
|---|---:|---|
| `dependency_count` | 0.30 | Relative number or concentration of dependencies affecting the subject. |
| `capacity_pressure` | 0.30 | Normalized pressure from planned effort versus available capacity. |
| `cross_team_impact` | 0.20 | Degree to which delivery crosses team boundaries. |
| `unresolved_reference` | 0.20 | Presence and extent of missing or unresolvable references. |

Weights must sum to `1.0`. If a factor is not applicable, the implementation should define and document whether it is treated as zero or whether the remaining weights are renormalized; the first-version default is to treat unavailable factors as zero and preserve explainability in `factors`.

## Factor guidance

### Dependency count

Use the subject's dependency count relative to the planning dataset or a documented cap. A feature with no dependencies receives `0.0`; the most connected or capped subject receives `1.0`. Circular dependencies should add a documented risk signal and normally produce at least a high-severity dependency risk.

### Capacity pressure

Calculate:

```text
capacity_pressure = planned_effort / available_capacity
```

The configured thresholds classify pressure as healthy below `0.80`, warning from `0.80` up to but excluding `1.00`, and critical at `1.00` or above. The factor is capped at `1.0` for the shared score while the raw ratio remains available in the risk description or factors.

### Cross-team impact

Use the proportion or documented count of involved teams. Same-team work is `0.0`; dependencies spanning multiple teams increase toward `1.0`. The exact normalization boundary must be consistent within a planning run.

### Unresolved references

Use `0.0` when all references resolve and `1.0` when a required reference is unresolved. Preserve the source and missing target in the shared risk record so the score can be acted upon.

## Severity mapping

Severity is derived from score and hard planning signals:

- `critical`: capacity is at or above the critical threshold, or a confirmed circular dependency materially blocks delivery.
- `high`: score is at or above `0.70`, or a warning/quality issue has material cross-team impact.
- `medium`: score is at or above `0.40` but below the high-risk threshold.
- `low`: score is below `0.40` with no critical hard signal.

Hard signals may raise severity but must not hide the numeric score or its factor breakdown.

## Prioritization and reporting

Sort open risks by descending `score`, then by severity (`critical`, `high`, `medium`, `low`), then by stable `risk_id` for deterministic output. Reports should show the subject, risk type, score, severity, contributing factors, and suggested mitigation. Re-running the same inputs and configuration must produce the same ranking.
