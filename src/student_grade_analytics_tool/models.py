"""Data models for the Student Grade Analytics Tool."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Grade:
    """A numeric score (0-100) with its letter grade."""

    score: float

    @property
    def letter(self) -> str:
        """Letter grade for this score."""
        if self.score >= 90:
            return "A"
        if self.score >= 80:
            return "B"
        if self.score >= 70:
            return "C"
        if self.score >= 60:
            return "D"
        return "F"


@dataclass(frozen=True)
class Course:
    """One student's result in one course during one semester."""

    code: str
    semester: int
    grade: Grade | None  # None when the score is missing


@dataclass(frozen=True)
class Student:
    """A student and their courses across all semesters."""

    student_id: str
    name: str
    major: str
    year: int
    courses: tuple[Course, ...]
