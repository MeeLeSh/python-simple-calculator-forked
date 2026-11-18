"""Преобразование строк в числа и результатов обратно в текст."""

from __future__ import annotations

from calc.errors import InvalidNumberError


def parse_number(raw: str) -> float:
    """Превратить строку в число.

    Запятая принимается как десятичный разделитель, чтобы ввод
    ``"7,5"`` работал так же, как ``"7.5"``.
    """
    try:
        return float(raw.strip().replace(",", "."))
    except ValueError:
        raise InvalidNumberError(raw) from None


def format_result(value: float) -> str:
    """Целое число печатать без хвоста ``.0``."""
    if value.is_integer():
        return str(int(value))
    return str(value)
