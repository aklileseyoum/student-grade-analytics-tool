"""Statistics for the Student Grade Analytics Tool.

Written red-green: each function starts as a stub that raises NotImplementedError.
"""

from collections import Counter

from student_grade_analytics_tool.models import Student


def semester_averages(student: Student) -> dict[int, float]:
    """Semester number -> average, in semester order. Empty semesters are left out."""
    raise NotImplementedError


def overall_average(student: Student) -> float | None:
    """Mean of all graded courses, or None if there are none."""
    return mean(all_scores([student]))


def trend(student: Student) -> str:
    """'improving', 'declining' or 'stable', from the rolling average of semesters."""
    raise NotImplementedError


def grade_distribution(students: list[Student]) -> Counter[str]:
    """Count of letter grades across all graded courses."""
    raise NotImplementedError


def group_by_major(students: list[Student]) -> dict[str, list[Student]]:
    """Group students by major."""
    raise NotImplementedError


def top_students(students: list[Student], n: int) -> list[Student]:
    """The n students with the highest overall average."""
    raise NotImplementedError


def all_scores(students: list[Student]) -> list[float]:
    """Every graded score of every student."""
    all_grades = []
    for student in students:
        for course in student.courses:
            if course.grade is not None:
                all_grades.append(course.grade.score)
    return all_grades


def mean(scores: list[float]) -> float | None:
    """Mean of the scores, or None if there are none."""
    if len(scores) > 0:
        return sum(scores) / len(scores)
    return None


def median(scores: list[float]) -> float | None:
    """Median of the scores, or None if there are none."""
    idx = len(scores) // 2
    if len(scores) % 2 == 1:
        sorted_score = sorted(scores)
        return sorted_score[idx]
    elif len(scores) % 2 == 0 and len(scores) != 0:
        return (scores[idx] + scores[idx - 1]) / 2
    return None


def mode(scores: list[float]) -> float | None:
    """Most common score, or None if there are none."""
    counted = Counter(scores)
    score = None
    freq = 0
    for k, v in counted.items():
        if v > freq:
            score = k
            freq = v

    return score


def percentile_rank(score: float, scores: list[float]) -> float:
    """Percent of the scores that are strictly below the given score."""
    raise NotImplementedError
