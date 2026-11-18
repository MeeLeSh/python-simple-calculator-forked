"""Пайплайн проекта: проверки -> расчёты -> отчёт.

Единая точка входа для запуска всего проекта.

Запуск:  snakemake --cores 1
Проверить план без запуска:  snakemake --cores 1 --dry-run
"""

EXPRESSIONS = "data/expressions.csv"
RESULTS = "reports/results.csv"
SUMMARY = "reports/summary.txt"
QUALITY = "reports/quality.ok"


rule all:
    input:
        QUALITY,
        RESULTS,
        SUMMARY,


rule quality:
    # Линтеры, проверка типов и тесты.
    input:
        "pyproject.toml",
        "Snakefile",
        "src/calc/core.py",
        "src/calc/cli.py",
        "tests/test_core.py",
        "tests/test_cli.py",
    output:
        QUALITY,
    shell:
        "ruff check src tests && black --check src tests && mypy src tests && pytest -q && echo ok > {output}"


rule compute:
    # Посчитать выражения из data/expressions.csv.
    input:
        EXPRESSIONS,
        "src/calc/core.py",
    output:
        RESULTS,
    shell:
        "python -m calc batch {input[0]} {output}"


rule summary:
    # Собрать текстовый отчёт по результатам расчётов.
    input:
        RESULTS,
    output:
        SUMMARY,
    shell:
        "python -m calc summary {input} {output}"
