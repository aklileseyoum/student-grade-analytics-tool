"""Command-line entry point: CSV in, JSON report out."""

import logging
import sys
from datetime import UTC, datetime
from pathlib import Path

from student_grade_analytics_tool.exceptions import (
    GradeAnalyticsError,
    MissingPathError,
)
from student_grade_analytics_tool.parser import parse_students
from student_grade_analytics_tool.reader import read_csv_rows
from student_grade_analytics_tool.report import build_report, write_report

stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

DEFAULT_CSV = Path("data/students.csv")
DEFAULT_OUTPUT = Path(f"output/report_{stamp}.json")

logger = logging.getLogger(__name__)


def ask_csv_path() -> Path:
    """Ask for the CSV path; an empty answer uses the default."""
    answer = input(f"Path to the CSV file [{DEFAULT_CSV}]: ").strip()
    if not answer:
        raise MissingPathError("No CSV path was given.")
    return Path(answer)


def run(csv_path: Path, output_path: Path) -> None:
    """The pipeline: read -> parse -> calculate -> write."""
    rows = read_csv_rows(csv_path)
    parsed = parse_students(rows)
    report = build_report(parsed.students, parsed.skipped)
    write_report(report, output_path)

    print(f"Students analysed: {len(parsed.students)}")
    print(f"Rows skipped:      {parsed.skipped}")
    print(f"Report written to: {output_path}")


def main() -> int:
    """Return 0 on success, 1 on a known error."""
    logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
    try:
        run(ask_csv_path(), DEFAULT_OUTPUT)
    except GradeAnalyticsError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
