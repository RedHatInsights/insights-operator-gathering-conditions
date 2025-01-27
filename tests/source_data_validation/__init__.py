from tests import PROJECT_ROOT

SCHEMAS = PROJECT_ROOT / "schemas"
CLUSTER_MAPPING = PROJECT_ROOT / "templates_v2" / "cluster_version_mapping.json"
CLUSTER_MAPPING_SCHEMA = SCHEMAS / "cluster_version_mapping.schema.json"
CONTAINER_LOG_REQUESTS = PROJECT_ROOT / "container_log_requests"
CONTAINER_LOG_SCHEMA = SCHEMAS / "container_log.schema.json"
GATHERING_RULES = PROJECT_ROOT / "conditional_gathering_rules"
GATHERING_RULE_SCHEMA = SCHEMAS / "gathering_rule.schema.json"
REMOTE_CONFIGURATIONS = PROJECT_ROOT / "templates_v2" / "remote_configurations"
REMOTE_CONFIGURATIONS_V1_SCHEMA = SCHEMAS / "remote_configuration_v1.schema.json"
REMOTE_CONFIGURATIONS_V2_SCHEMA = SCHEMAS / "remote_configuration_v2.schema.json"
REMOTE_CONFIGURATIONS_V2_TEMPLATE_SCHEMA = SCHEMAS / "remote_configuration_v2_template.schema.json"
