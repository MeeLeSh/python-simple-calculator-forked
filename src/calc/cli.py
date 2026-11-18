"""Командная строка калькулятора на click."""

from __future__ import annotations

import csv
from pathlib import Path

import click

from calc import __version__
from calc.core import evaluate
from calc.errors import CalculatorError
from calc.io import format_result, parse_number

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}
REQUIRED_COLUMNS = {"left", "operation", "right"}


def _calculate(left: str, right: str, operation: str) -> str:
    """Посчитать выражение и вернуть результат строкой."""
    try:
        value = evaluate(parse_number(left), parse_number(right), operation)
    except CalculatorError as exc:
        raise click.ClickException(str(exc)) from exc
    return format_result(value)


def _read_expressions(source: Path) -> list[dict[str, str]]:
    """Прочитать CSV с выражениями и проверить колонки."""
    with source.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        header = reader.fieldnames or []
        missing = REQUIRED_COLUMNS - set(header)
        if missing:
            columns = ", ".join(sorted(missing))
            raise click.ClickException(f"В {source.name} нет колонок: {columns}")
        return [
            {
                "left": row.get("left") or "",
                "operation": row.get("operation") or "",
                "right": row.get("right") or "",
            }
            for row in reader
        ]


def _write_csv(target: Path, rows: list[dict[str, str]], columns: list[str]) -> None:
    """Записать строки в CSV, создав каталог при необходимости."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(__version__, prog_name="calc")
def main() -> None:
    """Простой арифметический калькулятор."""


@main.command()
@click.argument("left")
@click.argument("right")
def add(left: str, right: str) -> None:
    """Сложить два числа: calc add 2 3."""
    click.echo(_calculate(left, right, "+"))


@main.command()
@click.argument("left")
@click.argument("right")
def sub(left: str, right: str) -> None:
    """Вычесть второе число из первого: calc sub 10 4."""
    click.echo(_calculate(left, right, "-"))


@main.command()
@click.argument("left")
@click.argument("right")
def mul(left: str, right: str) -> None:
    """Умножить два числа: calc mul 6 7."""
    click.echo(_calculate(left, right, "*"))


@main.command()
@click.argument("left")
@click.argument("right")
def div(left: str, right: str) -> None:
    """Разделить первое число на второе: calc div 8 2."""
    click.echo(_calculate(left, right, "/"))


@main.command()
@click.argument("left")
@click.argument("right")
def mod(left: str, right: str) -> None:
    """Остаток от деления: calc mod 10 3."""
    click.echo(_calculate(left, right, "%"))


@main.command(name="pow")
@click.argument("left")
@click.argument("right")
def power(left: str, right: str) -> None:
    """Возвести первое число в степень: calc pow 2 10."""
    click.echo(_calculate(left, right, "**"))


@main.command()
@click.argument("left")
@click.argument("right")
@click.argument("operation")
def compute(left: str, right: str, operation: str) -> None:
    """Посчитать произвольную операцию: calc compute 2 3 "**"."""
    click.echo(_calculate(left, right, operation))


@main.command()
def repl() -> None:
    """Интерактивный режим — как в первой версии калькулятора."""
    click.echo("Welcome to our Arithmetic Calculator")
    click.echo("Операции: + - * / % **, выход — q")
    while True:
        operation = click.prompt("Оператор", default="q", show_default=False)
        if operation.strip().lower() in {"q", "quit", "exit"}:
            break
        try:
            left = parse_number(click.prompt("Первое число"))
            right = parse_number(click.prompt("Второе число"))
            value = evaluate(left, right, operation.strip())
        except CalculatorError as exc:
            click.echo(f"Ошибка: {exc}", err=True)
            continue
        click.echo(f"Result: {format_result(value)}")
    click.echo("Thanks for using this simple arithmetic calculator")


@main.command()
@click.argument("source", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("target", type=click.Path(dir_okay=False, path_type=Path))
def batch(source: Path, target: Path) -> None:
    """Посчитать все выражения из CSV-файла.

    Вход — колонки ``left, operation, right``, выход — они же плюс
    ``result`` и ``error``.
    """
    results: list[dict[str, str]] = []
    for row in _read_expressions(source):
        record = {**row, "result": "", "error": ""}
        try:
            value = evaluate(
                parse_number(row["left"]),
                parse_number(row["right"]),
                row["operation"],
            )
        except CalculatorError as exc:
            record["error"] = str(exc)
        else:
            record["result"] = format_result(value)
        results.append(record)

    columns = ["left", "operation", "right", "result", "error"]
    _write_csv(target, results, columns)
    failed = sum(1 for record in results if record["error"])
    click.echo(f"Посчитано выражений: {len(results)}, ошибок: {failed}")


@main.command()
@click.argument("results", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("target", type=click.Path(dir_okay=False, path_type=Path))
def summary(results: Path, target: Path) -> None:
    """Собрать короткий отчёт по файлу результатов."""
    with results.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    failed = [row for row in rows if row.get("error")]
    lines = [
        f"Всего выражений: {len(rows)}",
        f"Успешно: {len(rows) - len(failed)}",
        f"С ошибкой: {len(failed)}",
    ]
    for row in failed:
        expression = f"{row.get('left')} {row.get('operation')} {row.get('right')}"
        lines.append(f"  {expression}: {row['error']}")

    target.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(lines) + "\n"
    target.write_text(text, encoding="utf-8")
    click.echo(text, nl=False)


if __name__ == "__main__":
    main()
