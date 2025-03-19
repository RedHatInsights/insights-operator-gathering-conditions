import json

import pytest

from tests import PROJECT_ROOT
from tests.source_data_validation import remote_configurations

CONDITIONAL_GATHERING_RULES_DIR = PROJECT_ROOT / "conditional_gathering_rules"


def list_conditional_gathering_rules():
    return sorted([p for p in CONDITIONAL_GATHERING_RULES_DIR.rglob("*") if p.is_file()])


def get_conditional_gathering_rules_ids():
    return [str(p.relative_to(PROJECT_ROOT)) for p in list_conditional_gathering_rules()]


@pytest.mark.parametrize(
    "filepath",
    list_conditional_gathering_rules(),
    ids=get_conditional_gathering_rules_ids(),
)
def test_schema(schema_validator, filepath):
    schema_validator.validate(filepath, "gathering_rule.schema.json")


@pytest.fixture(scope="session")
def used_conditional_gathering_rules():
    files = set()
    for remote_config_path in remote_configurations():
        remote_config = json.loads(remote_config_path.read_text())
        for pattern in remote_config["conditional_gathering_rules"]:
            files.update(PROJECT_ROOT.glob(pattern))
    return files


@pytest.mark.parametrize(
    "filepath",
    list_conditional_gathering_rules(),
    ids=get_conditional_gathering_rules_ids(),
)
def test_no_unused_rules(used_conditional_gathering_rules, filepath):
    assert filepath in used_conditional_gathering_rules
