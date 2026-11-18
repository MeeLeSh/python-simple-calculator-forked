"""Чистая логика калькулятора: без ``input()`` и ``print()``.

Модуль ничего не знает про командную строку, поэтому его легко
тестировать и переиспользовать в пайплайне.
"""

from __future__ import annotations

import operator
from collections.abc import Callable

from calc.errors import DivisionByZeroError, UnknownOperationError

BinaryOperation = Callable[[float, float], float]

#: Поддерживаемые операции: символ -> функция из модуля operator.
OPERATIONS: dict[str, BinaryOperation] = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "%": operator.mod,
    "**": operator.pow,
}

ZERO_DIVISION_OPERATIONS = frozenset({"/", "%"})


def evaluate(left: float, right: float, operation: str) -> float:
    """Посчитать выражение ``left operation right``.

    >>> evaluate(2, 3, "+")
    5.0
    """
    try:
        func = OPERATIONS[operation]
    except KeyError:
        raise UnknownOperationError(operation) from None

    if operation in ZERO_DIVISION_OPERATIONS and right == 0:
        raise DivisionByZeroError()

    return float(func(left, right))
