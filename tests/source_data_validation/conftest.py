import json

import pytest
from jsonschema import Draft202012Validator

from tests.source_data_validation import (
    REMOTE_CONFIGURATIONS_V1_SCHEMA_PATH,
    REMOTE_CONFIGURATIONS_V2_SCHEMA_PATH,
    container_log_requests,
    remote_configurations,
    schema_registry,
)


@pytest.fixture(name="container_log_requests")
def container_log_requests_fixture():
    return container_log_requests()


@pytest.fixture(name="remote_configurations")
def remote_configurations_fixture():
    return remote_configurations()


@pytest.fixture(name="schema_registry")
def schema_registry_fixture():
    return schema_registry()


@pytest.fixture
def remote_configurations_v1_validator(schema_registry):
    schema = json.loads(REMOTE_CONFIGURATIONS_V1_SCHEMA_PATH.read_text())
    return Draft202012Validator(schema, registry=schema_registry)


@pytest.fixture
def remote_configurations_v2_validator(schema_registry):
    schema = json.loads(REMOTE_CONFIGURATIONS_V2_SCHEMA_PATH.read_text())
    return Draft202012Validator(schema, registry=schema_registry)
