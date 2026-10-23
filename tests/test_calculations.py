"""Tests for calculations.py"""

from student_grade_analytics_tool import calculations as calc


def test_mean_of_scores() -> None:
    assert calc.mean([80, 90, 70]) == 80.0
    assert calc.mean([100]) == 100.0


def test_mean_of_empty_list_is_none() -> None:
    assert calc.mean([]) is None
