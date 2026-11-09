from pathlib import Path

import pandas as pd
import pytest

from data.csv_loader import (
    EmptyInputFileError,
    MalformedInputFileError,
    MissingInputFileError,
    SchemaValidationError,
    load_csv,
    load_planning_data,
)


def test_load_csv_success(tmp_path: Path):
    path = tmp_path / "teams.csv"
    path.write_text("team_id,name\nTEAM-1,Payments\n", encoding="utf-8")

    result = load_csv(path, required_columns=("team_id", "name"))

    assert isinstance(result, pd.DataFrame)
    assert result.to_dict("records") == [{"team_id": "TEAM-1", "name": "Payments"}]


def test_load_planning_data_uses_configurable_directory(tmp_path: Path):
    for name, header in {
        "teams": "scenario_id,team_id,name,capacity_id,active",
        "features": "scenario_id,feature_id,name,team_id,estimate,status,description",
        "dependencies": "scenario_id,dependency_id,source_feature_id,target_feature_id,dependency_type,status,description",
        "team_capacity": "scenario_id,capacity_id,team_id,increment,available_capacity,planned_effort,unit",
    }.items():
        values = ",".join("x" for _ in header.split(","))
        (tmp_path / f"{name}.csv").write_text(f"{header}\n{values}\n", encoding="utf-8")

    result = load_planning_data(tmp_path)

    assert set(result) == {"teams", "features", "dependencies", "team_capacity"}


def test_missing_file_raises(tmp_path: Path):
    with pytest.raises(MissingInputFileError):
        load_csv(tmp_path / "missing.csv")


def test_empty_file_raises(tmp_path: Path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")

    with pytest.raises(EmptyInputFileError):
        load_csv(path)


def test_header_only_file_raises(tmp_path: Path):
    path = tmp_path / "header-only.csv"
    path.write_text("team_id,name\n", encoding="utf-8")

    with pytest.raises(EmptyInputFileError):
        load_csv(path)


def test_malformed_file_raises(tmp_path: Path):
    path = tmp_path / "malformed.csv"
    path.write_text('team_id,name\nTEAM-1,"Payments\n', encoding="utf-8")

    with pytest.raises(MalformedInputFileError):
        load_csv(path)


def test_missing_required_columns_raises(tmp_path: Path):
    path = tmp_path / "invalid-schema.csv"
    path.write_text("team_id\nTEAM-1\n", encoding="utf-8")

    with pytest.raises(SchemaValidationError):
        load_csv(path, required_columns=("team_id", "name"))
