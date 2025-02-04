import json

import pytest

from tests import PROJECT_ROOT
from tests.source_data_validation import container_log_requests


def get_pod_name_regexes():
    """List all unique Pod Name regexes"""
    regexes = set()
    for file in container_log_requests():
        data = json.loads(file.read_text())
        regexes.add((file.relative_to(PROJECT_ROOT), data["pod_name_regex"]))
    return sorted(regexes)  # make a consistent order if we use xdist


def get_message_filters():
    """List all unique message filters"""
    filters = set()
    for file in container_log_requests():
        data = json.loads(file.read_text())
        for message in data["messages"]:
            filters.add((file.relative_to(PROJECT_ROOT), message))
    return sorted(filters)  # make a consistent order if we use xdist


@pytest.mark.parametrize("file_and_name", get_pod_name_regexes())
def test_pod_names_are_valid(golang_regex_validator, file_and_name):
    file, name = file_and_name
    assert golang_regex_validator.run(name).returncode == 0, f"Invalid regex {repr(name)} in {file}"


@pytest.mark.parametrize("file_and_filter", get_message_filters())
def test_message_filters(golang_regex_validator, file_and_filter):
    file, filter = file_and_filter
    assert golang_regex_validator.run(filter).returncode == 0, (
        f"Invalid regex {repr(filter)} in {file}"
    )
