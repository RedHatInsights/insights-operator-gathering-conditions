import subprocess

import pytest

from tests import PROJECT_ROOT


@pytest.fixture(scope="session")
def repository_root():
    return PROJECT_ROOT


class GolangRegexValidator:
    """Wrapper for running the golang tool as a subprocess

    Being it a class allows us to use it as a fixture were we can
    assert that we have the right file."""

    def __init__(self, file):
        self._file = file

    def run(self, input):
        return subprocess.run(
            ["go", "run", self._file], input=input, capture_output=True, encoding="utf-8"
        )


@pytest.fixture(scope="session")
def golang_regex_validator(repository_root):
    tool_file = repository_root / "golang_regex_validator/regexCompiler.go"
    assert tool_file.exists()
    validator = GolangRegexValidator(tool_file)
    return validator
