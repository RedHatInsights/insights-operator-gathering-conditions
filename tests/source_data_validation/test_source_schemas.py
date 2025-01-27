import json

from jsonschema import validate

from tests.source_data_validation import (
    CLUSTER_MAPPING,
    CLUSTER_MAPPING_SCHEMA,
    CONTAINER_LOG_REQUESTS,
    CONTAINER_LOG_SCHEMA,
    GATHERING_RULE_SCHEMA,
    GATHERING_RULES,
    REMOTE_CONFIGURATIONS,
    REMOTE_CONFIGURATIONS_V2_TEMPLATE_SCHEMA,
)


def test_cluster_mapping_schema():
    schema = json.loads(CLUSTER_MAPPING_SCHEMA.read_text())
    mapping = json.loads(CLUSTER_MAPPING.read_text())
    validate(mapping, schema)


def test_container_log_schema():
    schema = json.loads(CONTAINER_LOG_SCHEMA.read_text())
    for log_file in CONTAINER_LOG_REQUESTS.rglob("*.json"):
        container_log = json.loads(log_file.read_text())
        validate(container_log, schema)


def test_gathering_rules_schema():
    schema = json.loads(GATHERING_RULE_SCHEMA.read_text())
    for rules_file in GATHERING_RULES.rglob("*.json"):
        gathering_rules = json.loads(rules_file.read_text())
        validate(gathering_rules, schema)


def test_remote_configuration_v2_templates_schema():
    schema = json.loads(REMOTE_CONFIGURATIONS_V2_TEMPLATE_SCHEMA.read_text())
    for remote_config_file in REMOTE_CONFIGURATIONS.rglob("*.json"):
        remote_config = json.loads(remote_config_file.read_text())
        validate(remote_config, schema)
