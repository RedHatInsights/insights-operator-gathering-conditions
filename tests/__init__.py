from collections.abc import Generator
from typing import TypeVar

# source: https://github.com/pytest-dev/pytest/discussions/7809
T = TypeVar("T")

YieldFixture = Generator[T, None, None]
