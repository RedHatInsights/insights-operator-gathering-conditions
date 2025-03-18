from tests import PROJECT_ROOT

CLUSTER_MAPPING_PATH = PROJECT_ROOT / "blueprints_v2" / "cluster_version_mapping.json"

BLUEPRINTS_V2_DIR = PROJECT_ROOT / "blueprints_v2"


def remote_configurations():
    return BLUEPRINTS_V2_DIR.glob("remote_configurations/*.json")
