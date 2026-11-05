# Data Dictionary

This dictionary defines the canonical records used by the PI planning dependency and capacity mapper. Identifiers are stable, non-empty strings and must be unique within their entity type. Dates and timestamps use ISO 8601 when introduced; the first version does not require them.

## Relationship overview

```text
Team 1 ─── owns ─── * Feature
Team 1 ─── has ─── 1 Capacity
Feature 1 ─── source ─── * Dependency * ─── target ─── 1 Feature
Feature / Team / Dependency ─── may produce ─── * RiskRecord
```

## Team schema

| Field | Type | Required | Constraints / meaning |
|---|---|---:|---|
| `team_id` | string | yes | Unique stable identifier, recommended format `TEAM-001`. |
| `name` | string | yes | Human-readable team name; unique within the planning dataset. |
| `capacity_id` | string | yes | References exactly one `Capacity.capacity_id`. |
| `active` | boolean | no | Defaults to `true`; indicates whether the team participates in the increment. |

## Feature schema

| Field | Type | Required | Constraints / meaning |
|---|---|---:|---|
| `feature_id` | string | yes | Unique stable identifier, recommended format `FEAT-001`. |
| `name` | string | yes | Human-readable feature name. |
| `team_id` | string | yes | References exactly one owning `Team.team_id`. |
| `estimate` | number | yes | Non-negative planned effort in the dataset's effort unit. |
| `status` | string | yes | One of `planned`, `in_progress`, `done`, or `blocked`. |
| `description` | string | no | Context for planning and reporting. |

## Dependency schema

| Field | Type | Required | Constraints / meaning |
|---|---|---:|---|
| `dependency_id` | string | yes | Unique stable identifier, recommended format `DEP-001`. |
| `source_feature_id` | string | yes | References the feature that requires another feature. |
| `target_feature_id` | string | yes | References the feature required by the source; must not equal `source_feature_id`. |
| `dependency_type` | string | yes | One of `blocks`, `enables`, or `coordinates`. |
| `status` | string | yes | One of `unresolved`, `acknowledged`, `in_progress`, or `resolved`. |
| `description` | string | no | Explanation of the dependency or handoff. |

Both feature references are mandatory. A missing target is retained as an unresolved-reference finding rather than dropped. A dependency is directed from `source_feature_id` to `target_feature_id`; reverse traversal may be derived for impact analysis and is not stored as a second record.

## Capacity schema

| Field | Type | Required | Constraints / meaning |
|---|---|---:|---|
| `capacity_id` | string | yes | Unique stable identifier, recommended format `CAP-001`. |
| `team_id` | string | yes | References exactly one `Team.team_id`; one capacity record per team and increment. |
| `increment` | string | yes | Planning increment identifier, such as `PI-2026-Q1`. |
| `available_capacity` | number | yes | Positive available effort for the increment. |
| `planned_effort` | number | yes | Non-negative sum of assigned feature estimates. |
| `unit` | string | yes | Effort unit, such as `story_points` or `person_days`. |

Derived `capacity_pressure` is `planned_effort / available_capacity`. It is not required in source input and must not replace the two source measures.

## Shared risk record schema

All dependency, capacity, and feature-level risks use one `RiskRecord` shape. `subject_type` and `subject_id` identify the item at risk; `risk_type` explains the category.

| Field | Type | Required | Constraints / meaning |
|---|---|---:|---|
| `risk_id` | string | yes | Unique stable identifier, recommended format `RISK-001`. |
| `risk_type` | string | yes | One of `dependency`, `capacity`, `feature`, or `data_quality`. |
| `subject_type` | string | yes | One of `dependency`, `capacity`, `feature`, or `team`. |
| `subject_id` | string | yes | Identifier of the subject; must resolve for normal risks. |
| `title` | string | yes | Short human-readable risk statement. |
| `description` | string | yes | Explainable context and evidence. |
| `severity` | string | yes | One of `low`, `medium`, `high`, or `critical`. |
| `score` | number | yes | Normalized score from `0.0` through `1.0`. |
| `status` | string | yes | One of `open`, `accepted`, `mitigating`, or `closed`. |
| `factors` | object/map | yes | Named normalized inputs contributing to `score`. |
| `related_ids` | list[string] | no | Related feature, team, dependency, or capacity identifiers. |
| `mitigation` | string | no | Proposed response or planning action. |

`data_quality` risks may use a missing or unresolved reference in `related_ids`, but must preserve the original reference in `description`.
