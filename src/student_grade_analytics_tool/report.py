"""Build the analytics report, format a console chart and write the JSON file."""

import json
from collections import OrderedDict
from pathlib import Path
from typing import TypedDict

from student_grade_analytics_tool import calculations as calc
from student_grade_analytics_tool.exceptions import ReportWriteError
from student_grade_analytics_tool.models import Student

TOP_N = 5
GRADE_ORDER = ("A", "B", "C", "D", "F")


class SummaryStats(TypedDict):
    """Overall numbers for the whole file."""

    students: int
    skipped_rows: int
    mean: float | None
    median: float | None
    mode: float | None


class MajorStats(TypedDict):
    """Numbers for one major."""

    students: int
    average: float | None


class StudentSummary(TypedDict):
    """One student in the top performers list."""

    student_id: str
    name: str
    major: str
    year: int
    overall_average: float | None
    percentile: float | None
    trend: str
    semester_averages: dict[str, float]


class Report(TypedDict):
    """The structure of the JSON report."""

    summary: SummaryStats
    grade_distribution: OrderedDict[str, int]
    by_major: OrderedDict[str, MajorStats]
    top_students: list[StudentSummary]


def _round(value: float | None) -> float | None:
    """Round to 2 decimals, keeping None as None."""
    return None if value is None else round(value, 2)


def _student_summary(student: Student, all_averages: list[float]) -> StudentSummary:
    """Pick the report values for one student."""
    average = calc.overall_average(student)
    percentile = (
        None if average is None else calc.percentile_rank(average, all_averages)
    )
    return StudentSummary(
        student_id=student.student_id,
        name=student.name,
        major=student.major,
        year=student.year,
        overall_average=_round(average),
        percentile=_round(percentile),
        trend=calc.trend(student),
        semester_averages={
            str(semester): round(avg, 2)
            for semester, avg in calc.semester_averages(student).items()
        },
    )


def build_report(students: list[Student], skipped: int, top_n: int = TOP_N) -> Report:
    """Run the calculations and pick the values that go into the report."""
    scores = calc.all_scores(students)
    averages = [
        average
        for student in students
        if (average := calc.overall_average(student)) is not None
    ]
    distribution = calc.grade_distribution(students)
    majors = calc.group_by_major(students)

    return Report(
        summary=SummaryStats(
            students=len(students),
            skipped_rows=skipped,
            mean=_round(calc.mean(scores)),
            median=_round(calc.median(scores)),
            mode=_round(calc.mode(scores)),
        ),
        grade_distribution=OrderedDict(
            (grade, distribution.get(grade, 0)) for grade in GRADE_ORDER
        ),
        by_major=OrderedDict(
            (
                major,
                MajorStats(
                    students=len(majors[major]),
                    average=_round(calc.mean(calc.all_scores(majors[major]))),
                ),
            )
            for major in sorted(majors)
        ),
        top_students=[
            _student_summary(student, averages)
            for student in calc.top_students(students, top_n)
        ],
    )


def format_distribution_chart(distribution: dict[str, int], width: int = 30) -> str:
    """Return a text bar chart of the grade distribution."""
    peak = max(distribution.values(), default=0)
    lines = []
    for grade, count in distribution.items():
        bar = "#" * (round(count / peak * width) if peak else 0)
        lines.append(f"{grade} | {bar} {count}")
    return "\n".join(lines)


def write_report(report: Report, path: Path) -> None:
    """Write the report as JSON.

    Raises:
        ReportWriteError: the file cannot be written.
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
    except OSError as err:
        raise ReportWriteError(f"Cannot write report to {path}") from err
