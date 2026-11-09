"""Reusable, validated CSV loading utilities for planning inputs."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
from pandas.errors import EmptyDataError, ParserError

from logging_config import configure_logging


class DataLoadError(Exception):
    """Base exception for expected input-loading failures."""


class MissingInputFileError(DataLoadError):
    """Raised when a configured input file does not exist."""


class EmptyInputFileError(DataLoadError):
    """Raised when an input file is empty or has no data rows."""


class MalformedInputFileError(DataLoadError):
    """Raised when pandas cannot parse an input file as CSV."""


class SchemaValidationError(DataLoadError):
    """Raised when a parsed CSV does not contain required columns."""


def load_csv(
    path: str | Path,
    *,
    required_columns: Iterable[str] = (),
    logger=None,
    **read_csv_kwargs,
) -> pd.DataFrame:
    """Load one CSV, validating existence, content, and required columns."""
    csv_path = Path(path)
    log = logger or configure_logging()
    log.debug("Loading CSV input: %s", csv_path)

    if not csv_path.is_file():
        raise MissingInputFileError(f"Input CSV does not exist: {csv_path}")
    if csv_path.stat().st_size == 0:
        raise EmptyInputFileError(f"Input CSV is empty: {csv_path}")

    try:
        frame = pd.read_csv(csv_path, **read_csv_kwargs)
    except EmptyDataError as exc:
        raise EmptyInputFileError(f"Input CSV contains no data: {csv_path}") from exc
    except (ParserError, UnicodeDecodeError, ValueError) as exc:
        raise MalformedInputFileError(f"Could not parse input CSV: {csv_path}") from exc

    if frame.empty:
        raise EmptyInputFileError(f"Input CSV contains no data rows: {csv_path}")

    required = set(required_columns)
    missing = sorted(required.difference(frame.columns))
    if missing:
        raise SchemaValidationError(
            f"Input CSV is missing required columns {missing}: {csv_path}"
        )

    log.info("Loaded %d rows from %s", len(frame), csv_path)
    return frame


CSV_SCHEMAS = {
    "teams": ("scenario_id", "team_id", "name", "capacity_id", "active"),
    "features": (
        "scenario_id", "feature_id", "name", "team_id", "estimate", "status", "description"
    ),
    "dependencies": (
        "scenario_id", "dependency_id", "source_feature_id", "target_feature_id",
        "dependency_type", "status", "description",
    ),
    "team_capacity": (
        "scenario_id", "capacity_id", "team_id", "increment", "available_capacity",
        "planned_effort", "unit",
    ),
}


def load_planning_data(input_dir: str | Path = "data/raw", *, logger=None) -> dict[str, pd.DataFrame]:
    """Load all canonical planning CSVs from a configurable directory."""
    directory = Path(input_dir)
    return {
        name: load_csv(
            directory / f"{name}.csv",
            required_columns=columns,
            logger=logger,
        )
        for name, columns in CSV_SCHEMAS.items()
    }
