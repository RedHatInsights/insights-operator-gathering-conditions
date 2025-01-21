from collections.abc import Generator
from os import path
from pathlib import Path
from typing import TypeVar

# source: https://github.com/pytest-dev/pytest/discussions/7809
T = TypeVar("T")

YieldFixture = Generator[T, None, None]

_FOLDER = Path(path.abspath(__file__)).parent
PROJECT_ROOT = _FOLDER.parent
