import pytest

from tests.source_data_validation import (
    CLUSTER_MAPPING_PATH,
    container_log_requests,
    remote_configurations,
)


def files_and_schemas_to_validate():
    files_and_schemas = []
    files_and_schemas += [(CLUSTER_MAPPING_PATH, "cluster_version_mapping.schema.json")]
    files_and_schemas += [
        (log_file, "container_log.schema.json") for log_file in container_log_requests()
    ]
    files_and_schemas += [
        (config_file, "remote_configuration_v2_blueprint.schema.json")
        for config_file in remote_configurations()
    ]
    return files_and_schemas


@pytest.mark.parametrize("filepath,schema", files_and_schemas_to_validate())
def test_schema(schema_validator, filepath, schema):
    schema_validator.validate(filepath, schema)
