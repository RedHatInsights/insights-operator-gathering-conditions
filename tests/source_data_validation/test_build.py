import json

from jsonschema import validate

from tests.source_data_validation import (
    REMOTE_CONFIGURATIONS_V1_SCHEMA_PATH,
    REMOTE_CONFIGURATIONS_V2_SCHEMA_PATH,
)


def test_build_tool(build_tool_validator, tmp_path):
    # a test probably should not override the default build directory
    outputdir = tmp_path
    cp = build_tool_validator.run("--outputdir", outputdir)
    assert cp.returncode == 0
    assert (outputdir / "v1" / "rules.json").is_file()
    assert (outputdir / "v2" / "cluster_version_mapping.json").is_file()
    assert build_tool_validator.find_all_files(outputdir / "v2" / "remote_configurations")


def test_built_v1_remote_configurations_schema(build_tool_validator, tmp_path, schema_registry):
    outputdir = tmp_path
    build_tool_validator.run("--outputdir", outputdir)
    rules = json.loads((outputdir / "v1" / "rules.json").read_text())
    validate(
        rules,
        schema_registry.get_or_retrieve(str(REMOTE_CONFIGURATIONS_V1_SCHEMA_PATH)).value.contents,
        registry=schema_registry,
    )


def test_built_v2_remote_configurations_schema(build_tool_validator, tmp_path, schema_registry):
    outputdir = tmp_path
    build_tool_validator.run("--outputdir", outputdir)
    for remote_config_path in (outputdir / "v2" / "remote_configurations").rglob("*.json"):
        remote_config = json.loads(remote_config_path.read_text())
        validate(
            remote_config,
            schema_registry.get_or_retrieve(
                str(REMOTE_CONFIGURATIONS_V2_SCHEMA_PATH)
            ).value.contents,
            registry=schema_registry,
        )
