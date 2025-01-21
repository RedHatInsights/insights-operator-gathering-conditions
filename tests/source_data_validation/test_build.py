import pathlib


def test_build_tool(build_tool_validator, tmpdir):
    # a test probably should not override the default build directory
    outputdir = pathlib.Path(tmpdir)
    cp = build_tool_validator.run("--outputdir", outputdir)
    assert cp.returncode == 0
    assert (outputdir / "v1" / "rules.json").is_file()
    assert (outputdir / "v2" / "cluster_version_mapping.json").is_file()
    assert build_tool_validator.find_all_files(outputdir / "v2" / "remote_configurations")
