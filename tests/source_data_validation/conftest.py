import json

import pytest
from referencing import Registry, Resource

from tests.source_data_validation import (
    SCHEMAS,
    remote_configurations,
)


@pytest.fixture(name="remote_configurations")
def remote_configurations_fixture():
    return remote_configurations()


@pytest.fixture
def schema_registry():
    def retrieve_schema(schema_ref):
        return Resource.from_contents(json.loads((SCHEMAS / schema_ref).read_text()))

    return Registry(retrieve=retrieve_schema)
