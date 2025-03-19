import json

import pytest

from tests.source_data_validation import (
    BLUEPRINTS_V2_DIR,
    remote_configurations,
)

CLUSTER_VERSION_MAPPING_PATH = BLUEPRINTS_V2_DIR / "cluster_version_mapping.json"


def test_cluster_version_mapping_schema(schema_validator):
    schema_validator.validate(CLUSTER_VERSION_MAPPING_PATH, "cluster_version_mapping.schema.json")


@pytest.mark.parametrize("filepath", remote_configurations())
def test_remote_configuration_blueprint_schema(schema_validator, filepath):
    schema_validator.validate(filepath, "remote_configuration_v2_blueprint.schema.json")


@pytest.fixture(scope="session")
def used_blueprints_v2():
    mapping = json.loads(CLUSTER_VERSION_MAPPING_PATH.read_text())
    return [relpath for _, relpath in mapping]


@pytest.mark.parametrize("filepath", remote_configurations())
def test_no_unused_blueprint(used_blueprints_v2, filepath):
    mapping_path = str(filepath.relative_to(BLUEPRINTS_V2_DIR))
    assert mapping_path in used_blueprints_v2
