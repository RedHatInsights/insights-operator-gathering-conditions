import json
import pytest
import pathlib

from tests.source_data_validation import (
    CLUSTER_MAPPING_PATH,
    REMOTE_CONFIGURATIONS_V2_TEMPLATE_DIR,
    PROJECT_ROOT,
    gathering_rules,
    remote_configurations,
    remote_configurations_fixture,
    container_log_requests,
)


@pytest.mark.parametrize("remote_config_path", remote_configurations())
def test_all_remote_configurations_used(remote_config_path):
    mapping = json.loads(CLUSTER_MAPPING_PATH.read_text())
    mapping_configs = [pair[1] for pair in mapping]

    relative_config_path = str(remote_config_path.relative_to(REMOTE_CONFIGURATIONS_V2_TEMPLATE_DIR))
    assert relative_config_path in mapping_configs


@pytest.mark.parametrize("log_path", container_log_requests())
def test_all_container_logs_used(log_path, remote_configurations):
    relative_log_path = log_path.relative_to(PROJECT_ROOT)

    for remote_config_path in remote_configurations:
        remote_config = json.loads(remote_config_path.read_text())
        for pattern in remote_config["container_logs"]:
            if relative_log_path in pathlib.Path().glob(pattern):
                return

    assert False


@pytest.mark.parametrize("rule", gathering_rules())
def test_gathering_rule_used(rule, remote_configurations):
    relative_rule = rule.relative_to(PROJECT_ROOT)
    rules_in_configs = set()

    for remote_config_path in remote_configurations:
        remote_config = json.loads(remote_config_path.read_text())
        for pattern in remote_config["conditional_gathering_rules"]:
            if relative_rule in pathlib.Path().glob(pattern):
                return

    assert False
