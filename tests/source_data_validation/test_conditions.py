import json
import pathlib

from tests.source_data_validation import (
    CLUSTER_MAPPING,
    CONTAINER_LOG_REQUESTS,
    GATHERING_RULES,
    PROJECT_ROOT,
    REMOTE_CONFIGURATIONS,
)


def test_all_remote_configurations_used():
    mapping = json.loads(CLUSTER_MAPPING.read_text())
    mapping_configs = set([pair[1] for pair in mapping])
    available_configs = set()

    for remote_config_path in REMOTE_CONFIGURATIONS.rglob("*.json"):
        available_configs.add(str(remote_config_path.relative_to(REMOTE_CONFIGURATIONS)))

    assert mapping_configs == available_configs


def test_all_container_logs_used():
    available_logs = set(
        [log.relative_to(PROJECT_ROOT) for log in CONTAINER_LOG_REQUESTS.rglob("*.json")]
    )
    logs_in_configs = set()

    for remote_config_path in REMOTE_CONFIGURATIONS.rglob("*.json"):
        remote_config = json.loads(remote_config_path.read_text())
        for pattern in remote_config["container_logs"]:
            logs_in_configs.update(pathlib.Path().glob(pattern))

    assert available_logs == logs_in_configs


def test_all_gathering_rules_used():
    available_rules = set(
        [rule.relative_to(PROJECT_ROOT) for rule in GATHERING_RULES.rglob("*.json")]
    )
    rules_in_configs = set()

    for remote_config_path in REMOTE_CONFIGURATIONS.rglob("*.json"):
        remote_config = json.loads(remote_config_path.read_text())
        for pattern in remote_config["conditional_gathering_rules"]:
            rules_in_configs.update(pathlib.Path().glob(pattern))

    assert available_rules == rules_in_configs
