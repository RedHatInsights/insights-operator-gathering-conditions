def test_run_build_tool(build_tool_validator, tmp_path):
    """Check that the build tool succeeds on the source data. The build tool fails if it cannot
    generate valid configuration."""
    # a test probably should not override the default build directory
    outputdir = tmp_path
    cp = build_tool_validator.run("--outputdir", outputdir)
    assert cp.returncode == 0
