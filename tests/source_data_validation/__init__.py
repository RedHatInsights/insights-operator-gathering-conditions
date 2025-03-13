from tests import PROJECT_ROOT

CLUSTER_MAPPING_PATH = PROJECT_ROOT / "blueprints_v2" / "cluster_version_mapping.json"

CONTAINER_LOG_REQUESTS_DIR = PROJECT_ROOT / "container_log_requests"

GATHERING_RULES_DIR = PROJECT_ROOT / "conditional_gathering_rules"

REMOTE_CONFIGURATIONS_V2_BLUEPRINT_DIR = PROJECT_ROOT / "blueprints_v2" / "remote_configurations"


def remote_configurations():
    return REMOTE_CONFIGURATIONS_V2_BLUEPRINT_DIR.glob("*.json")


def gathering_rules():
    return GATHERING_RULES_DIR.rglob("*.json")


def container_log_requests():
    return CONTAINER_LOG_REQUESTS_DIR.rglob("*.json")
