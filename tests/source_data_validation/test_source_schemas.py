import json
import pytest

from jsonschema import validate

from tests.source_data_validation import (
    CLUSTER_MAPPING_PATH,
    cluster_mapping_schema,
    container_log_requests,
    container_log_schema,
    gathering_rules,
    gathering_rule_schema,
    remote_configurations,
    remote_configurations_v2_template_schema,
)


def files_and_schemas_to_validate():
    files_and_schemas = []
    files_and_schemas += [(CLUSTER_MAPPING_PATH, cluster_mapping_schema())]
    files_and_schemas += [(log_file, container_log_schema()) for log_file in container_log_requests()]
    files_and_schemas += [(rules_file, gathering_rule_schema()) for rules_file in gathering_rules()]
    files_and_schemas += [(config_file, remote_configurations_v2_template_schema()) for config_file in remote_configurations()]
    return files_and_schemas


@pytest.mark.parametrize("content_file,schema", files_and_schemas_to_validate())
def test_schema(content_file, schema):
    content = json.loads(content_file.read_text())
    validate(content, schema)
