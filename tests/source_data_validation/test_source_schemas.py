import json

import pytest

from tests.source_data_validation import (
    CLUSTER_MAPPING_PATH,
    cluster_mapping_validator,
    container_log_requests,
    container_log_validator,
    gathering_rule_validator,
    gathering_rules,
    remote_configurations,
    remote_configurations_v2_template_validator,
)


def files_and_schemas_to_validate():
    files_and_schemas = []
    files_and_schemas += [(CLUSTER_MAPPING_PATH, cluster_mapping_validator())]
    files_and_schemas += [
        (log_file, container_log_validator()) for log_file in container_log_requests()
    ]
    files_and_schemas += [
        (rules_file, gathering_rule_validator()) for rules_file in gathering_rules()
    ]
    files_and_schemas += [
        (config_file, remote_configurations_v2_template_validator())
        for config_file in remote_configurations()
    ]
    return files_and_schemas


@pytest.mark.parametrize("content_file,validator", files_and_schemas_to_validate())
def test_schema(content_file, validator):
    content = json.loads(content_file.read_text())
    validator.validate(content)
