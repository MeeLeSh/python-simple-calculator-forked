"""Исключения калькулятора.

Все ошибки, которые можно показать пользователю, наследуются от
:class:`CalculatorError` — командная строка ловит только их.
"""

from __future__ import annotations


class CalculatorError(Exception):
    """Базовая ошибка калькулятора."""


class DivisionByZeroError(CalculatorError):
    """Деление на ноль невозможно."""

    def __init__(self, message: str = "Деление на 0 невозможно") -> None:
        super().__init__(message)


class UnknownOperationError(CalculatorError):
    """Оператор не поддерживается."""

    def __init__(self, operation: str) -> None:
        self.operation = operation
        super().__init__(f"Неизвестная операция: {operation!r}")


class InvalidNumberError(CalculatorError):
    """Строку не удалось превратить в число."""

    def __init__(self, raw: str) -> None:
        self.raw = raw
        super().__init__(f"Не число: {raw!r}")
