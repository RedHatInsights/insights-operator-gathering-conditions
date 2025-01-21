import subprocess
from os import path
from pathlib import Path

_FOLDER = Path(path.abspath(__file__)).parent
_PROJECT_ROOT = _FOLDER.parent.parent


class GolangRegexValidator:
    """Wrapper for running the golang tool as a subprocess

    Being it a class allows us to use it as a fixture were we can
    assert that we have the right file."""

    FILE: Path = _PROJECT_ROOT / "golang_regex_validator/regexCompiler.go"

    def run(self, input: str):
        return subprocess.run(
            ["go", "run", self.FILE], input=input, capture_output=True, encoding="utf-8"
        )
