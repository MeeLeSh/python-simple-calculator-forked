"""Тесты командной строки."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest
from click.testing import CliRunner

from calc.cli import main


@pytest.fixture
def runner() -> CliRunner:
    """Изолированный запуск CLI без реального терминала."""
    return CliRunner()


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (["add", "2", "3"], "5"),
        (["sub", "10", "4"], "6"),
        (["mul", "6", "7"], "42"),
        (["div", "8", "2"], "4"),
        (["div", "5", "2"], "2.5"),
        (["mod", "10", "3"], "1"),
        (["pow", "2", "10"], "1024"),
        (["compute", "2", "3", "**"], "8"),
        (["add", "7,5", "2,5"], "10"),
    ],
)
def test_commands(runner: CliRunner, args: list[str], expected: str) -> None:
    result = runner.invoke(main, args)
    assert result.exit_code == 0
    assert result.output.strip() == expected


def test_division_by_zero_is_reported(runner: CliRunner) -> None:
    result = runner.invoke(main, ["div", "1", "0"])
    assert result.exit_code != 0
    assert "Деление" in result.output


def test_bad_number_is_reported(runner: CliRunner) -> None:
    result = runner.invoke(main, ["add", "два", "3"])
    assert result.exit_code != 0
    assert "Не число" in result.output


def test_unknown_operation_is_reported(runner: CliRunner) -> None:
    result = runner.invoke(main, ["compute", "2", "3", "^"])
    assert result.exit_code != 0
    assert "Неизвестная операция" in result.output


def test_help_lists_commands(runner: CliRunner) -> None:
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0
    for command in ("add", "batch", "compute", "div", "mod", "mul", "pow", "repl"):
        assert command in result.output


def test_batch_writes_results(runner: CliRunner, tmp_path: Path) -> None:
    source = tmp_path / "in.csv"
    source.write_text(
        "left,operation,right\n2,+,3\n1,/,0\n",
        encoding="utf-8",
    )
    target = tmp_path / "out.csv"

    result = runner.invoke(main, ["batch", str(source), str(target)])

    assert result.exit_code == 0
    with target.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[0]["result"] == "5"
    assert rows[0]["error"] == ""
    assert rows[1]["error"] != ""


def test_summary_counts_errors(runner: CliRunner, tmp_path: Path) -> None:
    source = tmp_path / "results.csv"
    source.write_text(
        "left,operation,right,result,error\n"
        "2,+,3,5,\n"
        "1,/,0,,Деление на 0 невозможно\n",
        encoding="utf-8",
    )
    target = tmp_path / "summary.txt"

    result = runner.invoke(main, ["summary", str(source), str(target)])

    assert result.exit_code == 0
    text = target.read_text(encoding="utf-8")
    assert "Всего выражений: 2" in text
    assert "С ошибкой: 1" in text
