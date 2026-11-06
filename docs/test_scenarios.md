# Deterministic Test Scenarios

The CSV fixtures in `data/raw/` are keyed by `scenario_id`. A test must filter all four files to one scenario before validating relationships or calculating results. Identifiers are unique within a scenario and stable across runs.

## CSV contracts

| File | Required columns |
|---|---|
| `teams.csv` | `scenario_id`, `team_id`, `name`, `capacity_id`, `active` |
| `features.csv` | `scenario_id`, `feature_id`, `name`, `team_id`, `estimate`, `status`, `description` |
| `dependencies.csv` | `scenario_id`, `dependency_id`, `source_feature_id`, `target_feature_id`, `dependency_type`, `status`, `description` |
| `team_capacity.csv` | `scenario_id`, `capacity_id`, `team_id`, `increment`, `available_capacity`, `planned_effort`, `unit` |

`scenario_id` is mandatory in every file. `team_id`, `feature_id`, `dependency_id`, and `capacity_id` are unique within a scenario. Feature team references must resolve to `teams.csv`; dependency feature references should resolve to `features.csv`, except where the scenario explicitly tests an unresolved reference. Each capacity record joins to one team through `team_id` and `capacity_id`.

## Scenario catalog and expected results

| ID | Scenario | Expected result |
|---|---|---|
| `S01` | Two-feature cycle | Exactly one directed cycle containing `F-S01-A` and `F-S01-B`; no unresolved references; Payments utilization is 50%. |
| `S02` | Three-feature cycle | Exactly one directed cycle containing `F-S02-A`, `F-S02-B`, and `F-S02-C`; no unresolved references; Payments utilization is 30%. |
| `S03` | 120% utilization | Payments utilization is exactly `1.20`; capacity classification is `critical`; the feature is a capacity risk. |
| `S04` | 40% utilization | Payments utilization is exactly `0.40`; capacity classification is `healthy`; no capacity risk is created from utilization alone. |
| `S05` | Unresolved dependency | `DEP-S05-01` has target `F-S05-MISSING`; exactly one unresolved-reference finding/risk is reported; no cycle is inferred. |
| `S06` | Normal cross-team dependencies | Checkout has dependencies to Identity-owned and Payments-owned features; at least one dependency crosses team boundaries; no cycle or unresolved reference exists. |
| `S07` | Multiple predecessors | `F-S07-A` has exactly three direct predecessors (`F-S07-B`, `F-S07-C`, `F-S07-D`); no cycle or unresolved reference exists. |

## Test expectations

Tests should assert exact IDs and counts above, not only broad labels. Capacity utilization should be calculated from `planned_effort / available_capacity`. Cycle tests should use directed edges from `source_feature_id` to `target_feature_id`. Cross-team tests should compare the source feature's owning team with the target feature's owning team. Risk tests should retain the scenario and subject identifiers so findings can be traced to source rows.
