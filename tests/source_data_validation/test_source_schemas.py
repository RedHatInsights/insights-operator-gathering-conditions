import json

import pytest
from jsonschema import validate

from tests.source_data_validation import (
    CLUSTER_MAPPING_PATH,
    CLUSTER_MAPPING_SCHEMA_PATH,
    CONTAINER_LOG_SCHEMA_PATH,
    GATHERING_RULE_SCHEMA_PATH,
    REMOTE_CONFIGURATIONS_V2_TEMPLATE_SCHEMA_PATH,
    container_log_requests,
    gathering_rules,
    remote_configurations,
)


def files_and_schemas_to_validate():
    files_and_schemas = []
    files_and_schemas += [(CLUSTER_MAPPING_PATH, CLUSTER_MAPPING_SCHEMA_PATH)]
    files_and_schemas += [
        (log_file, CONTAINER_LOG_SCHEMA_PATH) for log_file in container_log_requests()
    ]
    files_and_schemas += [
        (rules_file, GATHERING_RULE_SCHEMA_PATH) for rules_file in gathering_rules()
    ]
    files_and_schemas += [
        (config_file, REMOTE_CONFIGURATIONS_V2_TEMPLATE_SCHEMA_PATH)
        for config_file in remote_configurations()
    ]
    return files_and_schemas


@pytest.mark.parametrize("content_file,schema", files_and_schemas_to_validate())
def test_schema(content_file, schema, schema_registry):
    content = json.loads(content_file.read_text())
    validate(
        content,
        schema_registry.get_or_retrieve(str(schema)).value.contents,
        registry=schema_registry,
    )
