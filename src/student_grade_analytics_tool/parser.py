"""Turn raw CSV rows into Student objects."""

import logging
import re
from collections.abc import Iterable
from dataclasses import dataclass

from student_grade_analytics_tool.exceptions import (
    InvalidHeaderError,
    InvalidRecordError,
    NoValidRecordsError,
)
from student_grade_analytics_tool.models import Course, Grade, Student

logger = logging.getLogger(__name__)

COLUMN_PATTERN = re.compile(r"s(?P<semester>\d+)_(?P<code>\w+)")
REQUIRED_COLUMNS = ("student_id", "name", "major", "year")


@dataclass(frozen=True)
class ParseResult:
    """The students that were parsed and how many rows were skipped."""

    students: list[Student]
    skipped: int


def parse_header(fieldnames: Iterable[str]) -> dict[str, tuple[int, str]]:
    """Map each sN_COURSE column to (semester, course code).

    Raises:
        InvalidHeaderError: a required column is missing, or there are no
            course columns.
    """
    names = list(fieldnames)
    missing = [column for column in REQUIRED_COLUMNS if column not in names]
    if missing:
        raise InvalidHeaderError(f"Missing required columns: {', '.join(missing)}")

    columns: dict[str, tuple[int, str]] = {}
    for name in names:
        match = COLUMN_PATTERN.fullmatch(name)
        if match:
            columns[name] = (int(match["semester"]), match["code"])
    if not columns:
        raise InvalidHeaderError(
            "No course columns found. Expected names like 's1_MATH101'."
        )
    return columns


def parse_grade(cell: str) -> Grade | None:
    """Turn one score cell into a Grade. A blank cell gives None.

    Raises:
        ValueError: the cell is not a number, or is outside 0-100.
    """
    cell = cell.strip()
    if not cell:
        return None
    try:
        score = float(cell)
    except ValueError as err:
        raise ValueError(f"score {cell!r} is not a number") from err
    if not 0 <= score <= 100:
        raise ValueError(f"score {cell!r} is outside 0-100")
    return Grade(score=score)


def _cell(row: dict[str, str], key: str) -> str:
    """Return a cell as stripped text. A missing cell counts as empty."""
    return (row.get(key) or "").strip()


def _required(row: dict[str, str], key: str) -> str:
    value = _cell(row, key)
    if not value:
        raise ValueError(f"{key!r} is empty")
    return value


def _year(row: dict[str, str]) -> int:
    value = _cell(row, "year")
    try:
        return int(value)
    except ValueError as err:
        raise ValueError(f"'year' is not a whole number: {value!r}") from err


def parse_row(
    row: dict[str, str], columns: dict[str, tuple[int, str]], row_number: int
) -> Student:
    """Build one Student from one row.

    Raises:
        InvalidRecordError: any field in the row is invalid.
    """
    try:
        courses = tuple(
            Course(code=code, semester=semester, grade=parse_grade(_cell(row, column)))
            for column, (semester, code) in columns.items()
        )
        return Student(
            student_id=_required(row, "student_id"),
            name=_required(row, "name"),
            major=_required(row, "major"),
            year=_year(row),
            courses=courses,
        )
    except ValueError as err:
        raise InvalidRecordError(row_number, str(err)) from err


def parse_students(rows: list[dict[str, str]]) -> ParseResult:
    """Parse every row. Invalid rows are skipped, logged and counted.

    Raises:
        InvalidHeaderError: the header is wrong.
        NoValidRecordsError: there are no rows, or every row was invalid.
    """
    if not rows:
        raise NoValidRecordsError("There are no rows to parse.")

    columns = parse_header(rows[0].keys())
    students: list[Student] = []
    skipped = 0
    for row_number, row in enumerate(rows, start=2):
        try:
            students.append(parse_row(row, columns, row_number))
        except InvalidRecordError as err:
            logger.warning("Skipping invalid row: %s", err)
            skipped += 1

    if not students:
        raise NoValidRecordsError("Every row in the CSV file was invalid.")
    return ParseResult(students=students, skipped=skipped)
