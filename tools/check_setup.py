"""Проверка окружения: версия Python, виртуальное окружение, pgzero и pytest.

Запуск: python tools/check_setup.py
Код возврата: 0 — всё в порядке, 1 — есть проблемы.
"""

import importlib
import importlib.metadata
import os
import sys

MIN_VERSION = (3, 13)
PACKAGES = ("pgzero", "pytest")


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
