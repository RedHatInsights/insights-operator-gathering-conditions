import json
import shutil

import pytest
from jsonschema import validate

import build

"""
def test_success(build_tool_validator, tmp_path, success_test_case):
    outputdir = tmp_path / "output"
    cp = build_tool_validator.run(
        "--sourcedir",
        success_test_case / "src",
        "--outputdir",
        outputdir,
        # each test case could define its own version in a dedicated file if needed.
        "--version",
        "0.0.1",
    )

    # exit status
    assert cp.returncode == 0

    # logging
    assert "Remote configuration version: 0.0.1" in cp.stdout
    assert str(success_test_case) in cp.stdout
    assert str(outputdir) in cp.stdout

    # generated files
    build_tool_validator.assert_same_config_dirs(outputdir, success_test_case / "expected")
"""


def test_idempotency(build_tool_validator, tmp_path, test_case_dir):
    sample_test_case = test_case_dir / "valid_comprehensive"
    outputdir = tmp_path / "output"

    args = ["--sourcedir", sample_test_case / "src", "--outputdir", outputdir, "--version", "0.0.1"]

    cp = build_tool_validator.run(*args)
    cp = build_tool_validator.run(*args)
    assert cp.returncode == 0
    build_tool_validator.assert_same_config_dirs(outputdir, sample_test_case / "expected")


def test_v1_output_validated_correctly(build_tool_validator, tmp_path, schema_registry):
    outputdir = tmp_path
    cp = build_tool_validator.run("--outputdir", outputdir)
    if cp.stderr == "":
        try:
            rules = json.loads((outputdir / "v1" / "rules.json").read_text())
            validate(
                rules,
                schema_registry.get_or_retrieve(
                    "remote_configuration_v1.schema.json"
                ).value.contents,
                registry=schema_registry,
            )
        except Exception:
            pytest.fail(
                "There are discrapenties between build tool validation and direct validation of schema"
            )


def test_get_version_without_git_repo(build_tool_validator, tmp_path, test_case_dir):
    """Test that --version can supply a version when the source directory isn't in a Git repo."""
    sample_test_case = test_case_dir / "valid_comprehensive"
    sourcedir = tmp_path / "src"
    outputdir = tmp_path / "build"

    # copy a sample source dir to a directory outside of any Git repo
    shutil.copytree(sample_test_case / "src", sourcedir)

    cp = build_tool_validator.run(
        "--sourcedir", sourcedir, "--outputdir", outputdir, "--version", "0.0.1"
    )

    assert cp.returncode == 0
    build_tool_validator.assert_same_config_dirs(outputdir, sample_test_case / "expected")


@pytest.mark.parametrize(
    "raw_version,expected_result",
    [
        ("1.1.3-0-g5305978", "1.1.3"),
        ("1.1.3-0.1-g5305978", "1.1.3-0.1+g5305978"),
        ("1.1.3-30-g5305978", "1.1.3-30+g5305978"),
    ],
)
def test_parse_version_from_git_valid(raw_version, expected_result):
    parsed_version = build.RemoteConfigurations.parse_version_from_git(raw_version)
    assert parsed_version == expected_result


@pytest.mark.parametrize("raw_version", ["sometag-0-abcdefgh", "1.2.3.4-0-abcdefgh"])
def test_parse_version_from_git_invalid(raw_version):
    with pytest.raises(ValueError):
        build.RemoteConfigurations.parse_version_from_git(raw_version)
