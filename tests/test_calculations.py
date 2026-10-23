"""Tests for calculations.py"""

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
