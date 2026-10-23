# Student Grade Analytics Tool

A command-line tool that reads student grades from a CSV file, validates them, calculates statistics with advanced Python collections, and writes a JSON report.

## Features
- Reads a CSV with `student_id, name, major, year` plus course columns named `sN_COURSE` (for example `s1_MATH101` = semester 1, course MATH101).
- Validates every row: invalid rows are skipped, logged as warnings and counted.
- Statistics: mean, median, mode, per-student average, per-semester averages, grade distribution (A-F), students grouped by major, top students, percentile rank and a performance trend (improving / declining / stable).
- Writes a timestamped JSON report to `output/`.
- Custom exception hierarchy, so every expected failure ends with a clear message instead of a traceback.

## Requirements
- Python 3.12 or newer (developed on 3.14)
- [Poetry](https://python-poetry.org/)

## Setup
```powershell
git clone https://github.com/aklileseyoum/student-grade-analytics-tool.git
cd student-grade-analytics-tool
poetry install
poetry run python scripts/generate_sample_data.py   # creates data/students.csv (40 students, seed 42)
```
Without Poetry: `pip install -r requirements.txt` (development tools only; the application uses the standard library).

## Usage
```powershell
poetry run python -m student_grade_analytics_tool.main
```
You are asked for the path to the CSV file, for example `data\students.csv`. The tool prints a short summary and writes `output/report_<timestamp>.json`.

### Sample session
```
Path to the CSV file: data\students.csv
Students analysed: 40
Rows skipped:      0
Report written to: output\report_20261023_194500.json
```

### Sample error
```
Path to the CSV file: nope.csv
Error: CSV file not found: nope.csv
```

## Project structure
| File | Responsibility |
|---|---|
| `exceptions.py` | Custom exception hierarchy (`GradeAnalyticsError` base) |
| `models.py` | Immutable dataclasses: `Grade`, `Course`, `Student` |
| `reader.py` | Reads the CSV into rows (file-level errors) |
| `parser.py` | Validates rows and builds `Student` objects (row-level errors) |
| `calculations.py` | Statistics (`Counter`, `defaultdict`, `deque`, sorting) |
| `report.py` | Builds the report and writes it as JSON |
| `main.py` | Command-line entry point |

## Design decisions
- **Frozen dataclasses** keep the data immutable; `courses` is a tuple.
- **Reader vs parser errors:** the reader raises file-level errors (not found, access, empty). The parser raises row-level errors that are skipped and counted, and only fails when no valid row remains.
- **`defaultdict` is used only to build** results; functions return plain `dict` so a missing key raises `KeyError` instead of silently creating an entry.
- **`RollingAverage`** uses `deque(maxlen=window)`, so the oldest value drops automatically.
- **Percentile rank** = (scores strictly below / total scores) x 100.
- **Calculations are plain functions** in `calculations.py`, which keeps the models pure data and easy to test.

## Testing
Calculations were built with test-driven development (red, green, refactor).
```powershell
poetry run pytest -q --cov=student_grade_analytics_tool --cov-branch
```
Current result: all tests pass, `calculations.py` at 100% line and branch coverage.

## Code quality
Black, Ruff and mypy run through pre-commit.
```powershell
poetry run mypy src
poetry run ruff check src tests
```

## Workflow
Git Flow: `feature/*` branches merged into `develop` through pull requests with merge commits and conventional commit messages (`feat:`, `test:`).

## Known limitations
- Reader, parser and `main` have limited automated test coverage.
- The CSV path is asked interactively; there is no command-line argument yet.
