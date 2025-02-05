import json

import pytest
from referencing import Registry, Resource

from tests.source_data_validation import SCHEMAS


@pytest.fixture(scope="session")
def schema_registry():
    def retrieve_schema(schema_ref):
        return Resource.from_contents(json.loads((SCHEMAS / schema_ref).read_text()))

    return Registry(retrieve=retrieve_schema)
