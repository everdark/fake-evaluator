import pytest
from fake_evaluator.foo import do_something


def test_do_something_right():
    assert do_something(1) == 2


def test_do_something_wrong():
    assert do_something("1") == "1"
