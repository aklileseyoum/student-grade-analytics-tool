"""Tests for calculations.py"""

import pytest

from student_grade_analytics_tool import calculations as calc


def test_mean_of_scores() -> None:
    assert calc.mean([80, 90, 70]) == 80.0
    assert calc.mean([100]) == 100.0


def test_mean_of_empty_list_is_none() -> None:
    assert calc.mean([]) is None


def test_all_scores_collects_and_skips_blanks(make_student) -> None:
    s1 = make_student({1: [80, None], 2: [90]}, student_id="S1")
    s2 = make_student({1: [70]}, student_id="S2")
    assert calc.all_scores([s1, s2]) == [80, 90, 70]


def test_all_scores_no_students_gives_empty_list() -> None:
    assert calc.all_scores([]) == []


@pytest.mark.parametrize(
    ("scores", "expected"),
    [([1, 2, 3], 2), ([1, 2, 3, 4], 2.5), ([3, 1, 2], 2)],
)
def test_median(scores: list[float], expected: float) -> None:
    assert calc.median(scores) == expected


def test_median_of_empty_list_is_none() -> None:
    assert calc.median([]) is None


def test_mode_most_common_score() -> None:
    assert calc.mode([1, 2, 2, 3]) == 2


def test_mode_tie_returns_first_seen() -> None:
    assert calc.mode([1, 1, 2, 2]) == 1


def test_mode_of_empty_list_is_none() -> None:
    assert calc.mode([]) is None


def test_overall_average_skips_blank_grades(make_student) -> None:
    student = make_student({1: [80, None, 70], 2: [90]})
    assert calc.overall_average(student) == 80.0


def test_overall_average_all_blank_gives_none(make_student) -> None:
    assert calc.overall_average(make_student({1: [None, None]})) is None
