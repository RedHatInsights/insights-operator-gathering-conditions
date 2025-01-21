import pytest

from tests.golang_regex_validator import GolangRegexValidator


@pytest.fixture(scope="session")
def golang_regex_validator():
    validator = GolangRegexValidator()
    assert validator.FILE.exists()
    return validator
