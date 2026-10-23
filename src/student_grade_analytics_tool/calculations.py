"""Statistics for the Student Grade Analytics Tool.

Written red-green: each function starts as a stub that raises NotImplementedError.
"""

from collections import Counter, defaultdict

from student_grade_analytics_tool.models import Student


def semester_averages(student: Student) -> dict[int, float]:
    """Semester number -> average, in semester order. Empty semesters are left out."""
    scores = defaultdict(list)
    for course in student.courses:
        if course.grade is not None:
            scores[course.semester].append(course.grade.score)

    avg_score = defaultdict(float)
    for k, v in sorted(scores.items()):
        avg_score[k] = sum(v) / len(v)
    return avg_score


def overall_average(student: Student) -> float | None:
    """Mean of all graded courses, or None if there are none."""
    return mean(all_scores([student]))


def trend(student: Student) -> str:
    """'improving', 'declining' or 'stable', from the rolling average of semesters."""
    raise NotImplementedError


def grade_distribution(students: list[Student]) -> Counter[str]:
    """Count of letter grades across all graded courses."""
    grade_counts: Counter[str] = Counter()
    for student in students:
        for course in student.courses:
            if course.grade is not None:
                grade_counts[course.grade.letter] += 1

    return grade_counts


def group_by_major(students: list[Student]) -> dict[str, list[Student]]:
    """Group students by major."""
    by_major: defaultdict[str, list[Student]] = defaultdict(list)
    for student in students:
        by_major[student.major].append(student)

    return dict(by_major)


def top_students(students: list[Student], n: int) -> list[Student]:
    """The n students with the highest overall average."""
    avg_all = {}
    for student in students:
        summ: float = 0.0
        count = 0
        for course in student.courses:
            if course.grade is not None:
                summ += course.grade.score
                count += 1
        if summ != 0:
            avg = summ / count
            avg_all[student] = avg

    students_ranked = list(
        dict(sorted(avg_all.items(), key=lambda item: item[1], reverse=True))
    )

    if n < len(students_ranked):
        return students_ranked[:n]

    return students_ranked


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
    idx = 0
    for each in sorted(scores):
        if each < score:
            idx += 1
        else:
            return (idx / len(scores)) * 100
    if idx != 0:
        return 100

    return 0.0
