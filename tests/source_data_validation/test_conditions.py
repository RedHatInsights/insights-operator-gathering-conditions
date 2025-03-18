import json

import pytest

from tests.source_data_validation import (
    BLUEPRINTS_V2_DIR,
    CLUSTER_MAPPING_PATH,
    remote_configurations,
)


@pytest.mark.parametrize("remote_config_path", remote_configurations())
def test_all_remote_configurations_used(remote_config_path):
    mapping = json.loads(CLUSTER_MAPPING_PATH.read_text())
    mapping_configs = [relpath for _, relpath in mapping]

    relative_config_path = str(remote_config_path.relative_to(BLUEPRINTS_V2_DIR))
    assert relative_config_path in mapping_configs
