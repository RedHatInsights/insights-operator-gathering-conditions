import json
import pathlib

import pytest
from referencing import Registry, Resource

from tests.source_data_validation import SCHEMAS

TEST_CASE_DIR = pathlib.Path(__file__).parent.absolute()


@pytest.fixture(scope="session")
def schema_registry():
    def retrieve_schema(schema_ref):
        return Resource.from_contents(json.loads((SCHEMAS / schema_ref).read_text()))

    return Registry(retrieve=retrieve_schema)


@pytest.fixture
def test_case_dir():
    return TEST_CASE_DIR


def get_success_test_cases():
    return TEST_CASE_DIR.glob("valid_*")


@pytest.fixture(params=get_success_test_cases())
def success_test_case(request):
    # fixture parametrization: a data directory that defines a happy day test case
    return request.param
