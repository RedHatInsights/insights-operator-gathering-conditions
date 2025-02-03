from tests import PROJECT_ROOT
import pytest
import json

SCHEMAS = PROJECT_ROOT / "schemas"

CLUSTER_MAPPING_PATH = PROJECT_ROOT / "templates_v2" / "cluster_version_mapping.json"
CLUSTER_MAPPING_SCHEMA_PATH = SCHEMAS / "cluster_version_mapping.schema.json"

CONTAINER_LOG_REQUESTS_DIR = PROJECT_ROOT / "container_log_requests"
CONTAINER_LOG_SCHEMA_PATH = SCHEMAS / "container_log.schema.json"

GATHERING_RULES_DIR = PROJECT_ROOT / "conditional_gathering_rules"
GATHERING_RULE_SCHEMA_PATH = SCHEMAS / "gathering_rule.schema.json"

REMOTE_CONFIGURATIONS_V2_TEMPLATE_DIR = PROJECT_ROOT / "templates_v2" / "remote_configurations"
REMOTE_CONFIGURATIONS_V2_TEMPLATE_SCHEMA_PATH = SCHEMAS / "remote_configuration_v2_template.schema.json"

REMOTE_CONFIGURATIONS_V1_SCHEMA_PATH = SCHEMAS / "remote_configuration_v1.schema.json"
REMOTE_CONFIGURATIONS_V2_SCHEMA_PATH = SCHEMAS / "remote_configuration_v2.schema.json"


def remote_configurations():
    return REMOTE_CONFIGURATIONS_V2_TEMPLATE_DIR.glob("*.json")


@pytest.fixture(name="remote_configurations")
def remote_configurations_fixture():
    return remote_configurations()


def gathering_rules():
    return GATHERING_RULES_DIR.rglob("*.json")


def container_log_requests():
    return CONTAINER_LOG_REQUESTS_DIR.rglob("*.json")


def cluster_mapping_schema():
    return json.loads(CLUSTER_MAPPING_SCHEMA_PATH.read_text())


def gathering_rule_schema():
    return json.loads(GATHERING_RULE_SCHEMA_PATH.read_text())


def container_log_schema():
    return json.loads(CONTAINER_LOG_SCHEMA_PATH.read_text())


def remote_configurations_v2_template_schema():
    return json.loads(REMOTE_CONFIGURATIONS_V2_TEMPLATE_SCHEMA_PATH.read_text())


@pytest.fixture
def remote_configurations_v1_schema():
    return json.loads(REMOTE_CONFIGURATIONS_V1_SCHEMA_PATH.read_text())


@pytest.fixture
def remote_configurations_v2_schema():
    return json.loads(REMOTE_CONFIGURATIONS_V2_SCHEMA_PATH.read_text())

