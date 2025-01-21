import subprocess
from pathlib import Path

from tests import PROJECT_ROOT


class GolangRegexValidator:
    """Wrapper for running the golang tool as a subprocess

    Being it a class allows us to use it as a fixture were we can
    assert that we have the right file."""

    FILE: Path = PROJECT_ROOT / "golang_regex_validator/regexCompiler.go"

    def run(self, input: str):
        return subprocess.run(
            ["go", "run", self.FILE], input=input, capture_output=True, encoding="utf-8"
        )
