import pytest

from tests.source_data_validation import (
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
