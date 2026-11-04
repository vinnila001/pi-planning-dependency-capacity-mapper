# PI Planning Dependency Capacity Mapper

This project provides the foundation for analyzing dependencies, team capacity, and delivery risk during Agile Program Increment (PI) planning. The first version contains project configuration and documentation only; application business logic will be added in later work.

## Setup

Create a virtual environment:

```powershell
py -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run tests with `pytest`. Coverage can be added with `pytest --cov=src`.

## Layout

- `data/` contains raw and processed inputs.
- `src/` contains configuration and future data, analysis, visualization, reporting, and CLI modules.
- `tests/` contains automated tests.
- `docs/` contains business and architecture documentation.
- `output/` stores generated graphs and reports.

See `docs/business_requirements.md` and `docs/architecture.md` for the initial scope and design.
