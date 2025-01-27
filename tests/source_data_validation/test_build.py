import json
import os
import shutil
from pathlib import Path

import pytest
from jsonschema import RefResolver, validate

from tests.source_data_validation import (
    REMOTE_CONFIGURATIONS_V1_SCHEMA,
    REMOTE_CONFIGURATIONS_V2_SCHEMA,
    SCHEMAS,
)


def test_build_tool(build_tool_validator, tmp_path):
    # a test probably should not override the default build directory
    outputdir = tmp_path
    cp = build_tool_validator.run("--outputdir", outputdir)
    assert cp.returncode == 0
    assert (outputdir / "v1" / "rules.json").is_file()
    assert (outputdir / "v2" / "cluster_version_mapping.json").is_file()
    assert build_tool_validator.find_all_files(outputdir / "v2" / "remote_configurations")


def test_built_v1_remote_configurations_schema(build_tool_validator, tmp_path):
    outputdir = tmp_path
    cp = build_tool_validator.run("--outputdir", outputdir)
    schema = json.loads(REMOTE_CONFIGURATIONS_V1_SCHEMA.read_text())
    remote_config = json.loads((outputdir / "v1" / "rules.json").read_text())
    resolver = RefResolver(f"file://{SCHEMAS}/", schema)
    validate(remote_config, schema, resolver=resolver)


def test_built_v2_remote_configurations_schema(build_tool_validator, tmp_path):
    outputdir = tmp_path
    cp = build_tool_validator.run("--outputdir", outputdir)
    schema = json.loads(REMOTE_CONFIGURATIONS_V2_SCHEMA.read_text())
    resolver = RefResolver(f"file://{SCHEMAS}/", schema)
    for remote_config in (outputdir / "v2" / "remote_configurations").rglob("*.json"):
        rules = json.loads(remote_config.read_text())
        validate(rules, schema, resolver=resolver)
