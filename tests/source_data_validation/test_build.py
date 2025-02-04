import json


def test_build_tool(build_tool_validator, tmp_path):
    # a test probably should not override the default build directory
    outputdir = tmp_path
    cp = build_tool_validator.run("--outputdir", outputdir)
    assert cp.returncode == 0
    assert (outputdir / "v1" / "rules.json").is_file()
    assert (outputdir / "v2" / "cluster_version_mapping.json").is_file()
    assert build_tool_validator.find_all_files(outputdir / "v2" / "remote_configurations")


def test_built_v1_remote_configurations_schema(
    build_tool_validator, tmp_path, remote_configurations_v1_validator
):
    outputdir = tmp_path
    build_tool_validator.run("--outputdir", outputdir)
    remote_config = json.loads((outputdir / "v1" / "rules.json").read_text())
    remote_configurations_v1_validator.validate(remote_config)


def test_built_v2_remote_configurations_schema(
    build_tool_validator, tmp_path, remote_configurations_v2_validator
):
    outputdir = tmp_path
    build_tool_validator.run("--outputdir", outputdir)
    for remote_config in (outputdir / "v2" / "remote_configurations").rglob("*.json"):
        rules = json.loads(remote_config.read_text())
        remote_configurations_v2_validator.validate(rules)
