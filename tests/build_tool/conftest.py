import pathlib

import pytest

TEST_CASE_DIR = pathlib.Path(__file__).parent.absolute()


@pytest.fixture
def test_case_dir():
    return TEST_CASE_DIR


def get_success_test_cases():
    return sorted(TEST_CASE_DIR.glob("valid_*"))


def get_fail_test_cases():
    return sorted(TEST_CASE_DIR.glob("invalid_*"))


def paths_to_ids(paths):
    return [p.name for p in paths]


@pytest.fixture(params=get_success_test_cases(), ids=paths_to_ids(get_success_test_cases()))
def success_test_case(request):
    # fixture parametrization: a data directory that defines a happy day test case
    return request.param


@pytest.fixture(params=get_fail_test_cases(), ids=paths_to_ids(get_fail_test_cases()))
def fail_test_case(request):
    # fixture parametrization: a data directory that defines a sad day test case
    return request.param
