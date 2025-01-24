import pytest

INVALID_REGEX = "[\\]"


@pytest.mark.parametrize(
    "regex,valid",
    [
        ("ab", True),
        (INVALID_REGEX, False),
    ],
)
def test_exit_status(golang_regex_validator, regex, valid):
    cp = golang_regex_validator.run(regex)
    assert cp.returncode == 0 if valid is True else cp.returncode != 0


def test_errors_are_on_stderr(golang_regex_validator):
    cp = golang_regex_validator.run(INVALID_REGEX)
    assert "panic: regexp" in cp.stderr
