"""Configurable defaults for planning analysis."""

CAPACITY_WARNING_THRESHOLD = 0.80
CAPACITY_CRITICAL_THRESHOLD = 1.00

RISK_SCORING_WEIGHTS = {
    "dependency_count": 0.30,
    "capacity_pressure": 0.30,
    "cross_team_impact": 0.20,
    "unresolved_reference": 0.20,
}

HIGH_RISK_THRESHOLD = 0.70
