from tests import PROJECT_ROOT

BLUEPRINTS_V2_DIR = PROJECT_ROOT / "blueprints_v2"


def remote_configurations():
    return BLUEPRINTS_V2_DIR.glob("remote_configurations/*.json")
