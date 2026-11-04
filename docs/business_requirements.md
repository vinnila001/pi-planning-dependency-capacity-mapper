# Business Requirements

## Scenario

The product supports a synthetic Agile PI planning workshop. Teams plan features for an upcoming increment, identify dependencies between features, compare planned work with team capacity, and prioritize delivery risks for discussion.

Sample teams are Payments, Identity, and Notifications. Sample features include Checkout, Customer Login, and Order Confirmation. Checkout depends on Customer Login and Order Confirmation; Order Confirmation depends on Notifications. Each feature has an owning team and an estimated effort, while each team has available capacity for the increment.

## Business rules

- A dependency must reference an existing feature and should be represented in both directions for impact analysis.
- A circular dependency is a planning risk requiring explicit reporting.
- Planned effort divided by capacity indicates pressure: below 80% is healthy, 80–99% is a warning, and 100% or more is critical.
- Cross-team dependencies increase coordination risk.
- Unresolved references are retained as data-quality risks and never silently discarded.
- Risk scores combine dependency count, capacity pressure, cross-team impact, and unresolved references using configured weights.
- High-risk items meet or exceed the configured high-risk threshold.

## Expected results

The system should identify circular dependencies, unresolved references, capacity warnings/critical overloads, cross-team dependency hotspots, and a ranked risk list. It should be able to produce a dependency graph and a concise planning report.

## Acceptance criteria

- Circular dependencies are detected, identified by the involved features, and included in the report.
- Unresolved references are identified with their source feature and missing target.
- Capacity risks distinguish warning from critical pressure using configurable thresholds.
- Cross-team analysis shows the teams connected by each dependency and highlights coordination hotspots.
- Risk prioritization produces a deterministic ranking with explainable contributing factors.
- Graph output includes features as nodes and dependencies as directed edges.
- Reports summarize findings, assumptions, and high-risk items in a human-readable format.

## First-version scope

The first version defines the synthetic scenario, configuration boundaries, documentation, and project skeleton. Future implementation may read structured local files and generate graphs and reports.

Out of scope: live Jira/Azure DevOps integrations, databases, authentication, deployment, CI/CD, real-time collaboration, forecasting beyond supplied capacity, and automatic work-item updates.
