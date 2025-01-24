import json

import pytest

from tests.source_data_validation import CONTAINER_LOG_REQUESTS


def get_pod_name_regexes():
    """List all unique Pod Name regexes"""
    regexes = set()
    for file in CONTAINER_LOG_REQUESTS.glob("**/*.json"):
        data = json.loads(file.read_text())
        regexes.add(data["pod_name_regex"])
    return sorted(regexes)  # make a consistent order if we use xdist


def get_message_filters():
    """List all unique message filters"""
    filters = set()
    for file in CONTAINER_LOG_REQUESTS.glob("**/*.json"):
        data = json.loads(file.read_text())
        filters.update(data["messages"])
    return sorted(filters)  # make a consistent order if we use xdist


@pytest.mark.parametrize("name", get_pod_name_regexes())
def test_pod_names_are_valid(golang_regex_validator, name):
    assert golang_regex_validator.run(name).returncode == 0, f"Invalid regex {repr(name)}"


@pytest.mark.parametrize("filter", get_message_filters())
def test_message_filters(golang_regex_validator, filter):
    assert golang_regex_validator.run(filter).returncode == 0, f"Invalid regex {repr(filter)}"
