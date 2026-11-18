"""Тесты чистой логики калькулятора."""

from __future__ import annotations

import pytest

from calc.core import OPERATIONS, evaluate
from calc.errors import DivisionByZeroError, UnknownOperationError


@pytest.mark.parametrize(
    ("left", "right", "operation", "expected"),
    [
        (2, 3, "+", 5),
        (10, 4, "-", 6),
        (6, 7, "*", 42),
        (8, 2, "/", 4),
        (10, 3, "%", 1),
        (2, 10, "**", 1024),
        (7.5, 2.5, "+", 10),
        (-5, 3, "*", -15),
    ],
)
def test_evaluate(left: float, right: float, operation: str, expected: float) -> None:
    assert evaluate(left, right, operation) == pytest.approx(expected)


def test_all_operations_are_available() -> None:
    assert set(OPERATIONS) == {"+", "-", "*", "/", "%", "**"}


@pytest.mark.parametrize("operation", ["/", "%"])
def test_zero_division_raises(operation: str) -> None:
    with pytest.raises(DivisionByZeroError):
        evaluate(1, 0, operation)


@pytest.mark.parametrize("operation", [":", "", "^", "plus"])
def test_unknown_operation_raises(operation: str) -> None:
    with pytest.raises(UnknownOperationError) as exc_info:
        evaluate(1, 2, operation)
    assert operation in str(exc_info.value)
