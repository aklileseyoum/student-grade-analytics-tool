import csv
from pathlib import Path

from student_grade_analytics_tool.exceptions import (
    CSVAccessError,
    CSVNotFoundError,
    EmptyCSVError,
)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    """Read a CSV file and return its rows as dictionaries keyed by header.

    Raises:
        CSVNotFoundError: the file does not exist.
        CSVAccessError: the file cannot be opened (permissions, or a folder).
        EmptyCSVError: the file has no header or no data rows.
    """
    try:
        with open(path, newline="", encoding="utf-8") as f:
            dict_reader = csv.DictReader(f)
            if not dict_reader.fieldnames:
                raise EmptyCSVError(f"CSV file has no header: {path}")
            rows = list(dict_reader)
    except FileNotFoundError as err:
        raise CSVNotFoundError(f"CSV file not found: {path}") from err
    except (PermissionError, IsADirectoryError) as err:
        raise CSVAccessError(f"Cannot read CSV file: {path}") from err

    if not rows:
        raise EmptyCSVError(f"CSV file has a header but no data rows: {path}")
    return rows
