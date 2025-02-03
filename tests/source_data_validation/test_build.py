import json
import os
import shutil
from pathlib import Path

import pytest
from jsonschema import RefResolver, validate

from tests.source_data_validation import (
    remote_configurations_v1_schema,
    remote_configurations_v2_schema,
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


def test_built_v1_remote_configurations_schema(build_tool_validator, tmp_path, remote_configurations_v1_schema):
    outputdir = tmp_path
    cp = build_tool_validator.run("--outputdir", outputdir)
    remote_config = json.loads((outputdir / "v1" / "rules.json").read_text())
    resolver = RefResolver(f"file://{SCHEMAS}/", remote_configurations_v1_schema)
    validate(remote_config, remote_configurations_v1_schema, resolver=resolver)


def test_built_v2_remote_configurations_schema(build_tool_validator, tmp_path, remote_configurations_v2_schema):
    outputdir = tmp_path
    cp = build_tool_validator.run("--outputdir", outputdir)
    resolver = RefResolver(f"file://{SCHEMAS}/", remote_configurations_v2_schema)
    for remote_config in (outputdir / "v2" / "remote_configurations").rglob("*.json"):
        rules = json.loads(remote_config.read_text())
        validate(rules, remote_configurations_v2_schema, resolver=resolver)
