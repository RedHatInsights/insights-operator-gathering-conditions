import subprocess
from os import path
from pathlib import Path

import pytest


_FOLDER = Path(path.abspath(__file__)).parent
_GO_TOOL_FILE = _FOLDER.parent / "regexCompiler.go"

INVALID_REGEX = "[\\]"


def invoke(input: str) -> subprocess.CompletedProcess:
    return subprocess.run(["go", "run", _GO_TOOL_FILE], input=input, capture_output=True, encoding="utf-8")


@pytest.mark.parametrize(
    "regex,valid",
    [
        ("ab", True),
        (INVALID_REGEX, False),
    ],
)
def test_exit_status(regex, valid):
    cp = invoke(regex)
    assert cp.returncode == 0 if valid is True else cp.returncode != 0


def test_errors_are_on_stderr():
    cp = invoke(INVALID_REGEX)
    assert cp.stderr != None
