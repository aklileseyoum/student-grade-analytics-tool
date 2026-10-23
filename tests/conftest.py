from collections.abc import Callable

import pytest

from student_grade_analytics_tool.models import Course, Grade, Student


@pytest.fixture
def make_student() -> Callable[..., Student]:
    """Build a Student from {semester: [scores]}. Use None for a blank score."""

    def _make(
        scores: dict[int, list[float | None]],
        *,
        student_id: str = "S001",
        major: str = "CS",
        year: int = 1,
    ) -> Student:
        courses = tuple(
            Course(
                code=f"C{semester}{index}",
                semester=semester,
                grade=None if score is None else Grade(score),
            )
            for semester, semester_scores in scores.items()
            for index, score in enumerate(semester_scores, start=1)
        )
        return Student(student_id, f"Name {student_id}", major, year, courses)

    return _make
