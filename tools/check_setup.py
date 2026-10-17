"""Проверка окружения: Python, виртуальное окружение, pgzero, pytest и имена файлов.

Запуск: python tools/check_setup.py
Код возврата: 0 — всё в порядке, 1 — есть проблемы.
"""

import importlib
import importlib.metadata
import os
import re
import sys
from pathlib import Path

MIN_VERSION = (3, 13)
PACKAGES = ("pgzero", "pytest")
REPO_ROOT = Path(__file__).resolve().parent.parent
# Имена, которые нельзя давать своим .py: такой файл заслонит настоящий модуль и сломает импорт
TAKEN_MODULE_NAMES = set(sys.stdlib_module_names) | {"pgzero", "pgzrun", "pygame", "pytest", "test"}
SAFE_NAME = re.compile(r"[A-Za-z0-9_.\-]+")
SKIP_DIRS = {".git", ".venv", "venv", ".idea", "__pycache__", ".pytest_cache"}


def check_file_names(root: Path) -> list[str]:
    """Найти имена с пробелами/кириллицей и .py-файлы, совпадающие с модулями Python."""
    problems = []
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(part in SKIP_DIRS for part in relative.parts):
            continue
        if path.is_file() and path.suffix == ".md":
            continue
        if not SAFE_NAME.fullmatch(path.name):
            problems.append(
                f"{relative.as_posix()}: в имени пробелы, русские буквы или значки — "
                "переименуй латиницей через _"
            )
        elif path.suffix == ".py" and path.stem in TAKEN_MODULE_NAMES:
            problems.append(
                f"{relative.as_posix()}: так называется модуль Python — переименуй, "
                f"например, в my_{path.stem}.py"
            )
    return problems


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
    problems = []

    version = sys.version_info
    version_text = f"{version.major}.{version.minor}.{version.micro}"
    if version[:2] >= MIN_VERSION:
        print(f"[OK] Python {version_text}")
    else:
        print(f"[!!] Python {version_text} — нужен 3.13 или новее")
        problems.append(
            f"Python {version_text} старше 3.13. Создай .venv заново: python3.13 -m venv .venv"
        )

    if sys.prefix != sys.base_prefix:
        print(f"[OK] Виртуальное окружение: {sys.prefix}")
    else:
        print("[!!] Скрипт запущен не из виртуального окружения")
        problems.append(
            "Активируй .venv (Windows: .venv\\Scripts\\activate, macOS/Linux: source .venv/bin/activate) "
            "или выбери .venv как интерпретатор в PyCharm"
        )

    missing = []
    for package in PACKAGES:
        try:
            importlib.import_module(package)
            print(f"[OK] {package} {importlib.metadata.version(package)}")
        except Exception as error:  # noqa: BLE001 — нам важен любой сбой импорта
            print(f"[!!] {package} не импортируется: {error}")
            missing.append(package)
    if missing:
        problems.append(f"Не установлено: {', '.join(missing)}. Выполни: pip install -r requirements.txt")

    name_problems = check_file_names(REPO_ROOT)
    if name_problems:
        print(f"[!!] Имена файлов: {len(name_problems)} проблем(ы)")
        problems.extend(name_problems)
    else:
        print("[OK] Имена файлов и папок")

    print()
    if not problems:
        print("Всё готово к занятиям!")
        return 0

    print("Есть проблемы:")
    for problem in problems:
        print(f"  - {problem}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
