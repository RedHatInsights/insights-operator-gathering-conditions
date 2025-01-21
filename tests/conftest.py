import pytest

from tests import YieldFixture
from tests.golang_regex_validator import GolangRegexValidator


@pytest.fixture(scope="session")
def golang_regex_validator() -> YieldFixture[GolangRegexValidator]:
    validator = GolangRegexValidator()
    assert validator.FILE.exists()
    return validator
