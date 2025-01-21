import pathlib

import pytest

TEST_CASE_DIR = pathlib.Path(__file__).parent.absolute()


@pytest.fixture
def test_case_dir():
    return TEST_CASE_DIR


def get_success_test_cases():
    return TEST_CASE_DIR.glob("valid_*")


@pytest.fixture(params=get_success_test_cases())
def success_test_case(request):
    # fixture parametrization: a data directory that defines a happy day test case
    return request.param
