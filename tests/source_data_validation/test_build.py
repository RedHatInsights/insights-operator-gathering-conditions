import json

from jsonschema import validate


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
        schema_registry.get_or_retrieve("remote_configuration_v1.schema.json").value.contents,
        registry=schema_registry,
    )


def test_built_v2_remote_configurations_schema(build_tool_validator, tmp_path, schema_registry):
    outputdir = tmp_path
    build_tool_validator.run("--outputdir", outputdir)
    for remote_config_path in (outputdir / "v2" / "remote_configurations").rglob("*.json"):
        remote_config = json.loads(remote_config_path.read_text())
        validate(
            remote_config,
            schema_registry.get_or_retrieve("remote_configuration_v2.schema.json").value.contents,
            registry=schema_registry,
        )
