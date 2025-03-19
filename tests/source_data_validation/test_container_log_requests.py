import json

import pytest

from tests import PROJECT_ROOT
from tests.source_data_validation import remote_configurations

CONTAINER_LOG_REQUESTS_DIR = PROJECT_ROOT / "container_log_requests"


def list_container_log_requests():
    # make a consistent order if we use xdist
    return sorted([p for p in CONTAINER_LOG_REQUESTS_DIR.rglob("*") if p.is_file()])


def get_container_log_requests_ids():
    return [str(p.relative_to(PROJECT_ROOT)) for p in list_container_log_requests()]


@pytest.mark.parametrize(
    "filepath",
    list_container_log_requests(),
    ids=get_container_log_requests_ids(),
)
def test_schema(schema_validator, filepath):
    schema_validator.validate(filepath, "container_log.schema.json")


@pytest.fixture(scope="session")
def used_container_log_requests():
    files = set()
    for remote_config_path in remote_configurations():
        remote_config = json.loads(remote_config_path.read_text())
        for pattern in remote_config["container_logs"]:
            files.update(PROJECT_ROOT.glob(pattern))
    return files


@pytest.mark.parametrize(
    "filepath",
    list_container_log_requests(),
    ids=get_container_log_requests_ids(),
)
def test_no_unused_requests(used_container_log_requests, filepath):
    assert filepath in used_container_log_requests


@pytest.mark.parametrize(
    "filepath",
    list_container_log_requests(),
    ids=get_container_log_requests_ids(),
)
def test_pod_name_regex(golang_regex_validator, filepath):
    request = json.loads(filepath.read_text())
    pod_name_regex = request["pod_name_regex"]
    assert golang_regex_validator.run(pod_name_regex).returncode == 0, (
        f"Invalid regex {repr(pod_name_regex)} in {filepath}"
    )


def get_message_filters():
    """List all unique message filters"""
    filters = []
    for file in list_container_log_requests():
        data = json.loads(file.read_text())
        for message_filter in data["messages"]:
            filters.append((file.relative_to(PROJECT_ROOT), message_filter))
    # The list order is consistent. The list_container_log_requests() function returns a sorted list
    # of files and the message filters order in individual files is fixed.
    return filters


def get_message_filters_ids():
    return [f"{filepath},filter{i}" for i, (filepath, _) in enumerate(get_message_filters())]


@pytest.mark.parametrize(
    "file_and_filter",
    get_message_filters(),
    ids=get_message_filters_ids(),
)
def test_message_filter_regex(golang_regex_validator, file_and_filter):
    filepath, message_filter = file_and_filter
    assert golang_regex_validator.run(message_filter).returncode == 0, (
        f"Invalid regex {repr(message_filter)} in {filepath}"
    )
