import pathlib
import shutil

import pytest

import build


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
    assert str(success_test_case) in cp.stdout
    assert str(outputdir) in cp.stdout
    # generated files
    build_tool_validator.assert_same_config_dirs(outputdir, success_test_case / "expected")


def test_idempotency(build_tool_validator, tmp_path, test_case_dir):
    sample_test_case = test_case_dir / "valid_comprehensive"
    outputdir = tmp_path / "output"

    args = ["--sourcedir", sample_test_case / "src", "--outputdir", outputdir, "--version", "0.0.1"]

    cp = build_tool_validator.run(*args)
    cp = build_tool_validator.run(*args)
    assert cp.returncode == 0
    build_tool_validator.assert_same_config_dirs(outputdir, sample_test_case / "expected")


def test_failure(build_tool_validator, tmp_path, fail_test_case):
    outputdir = tmp_path / "output"
    custom_schemadir = fail_test_case / "schemas"
    schemadir = (
        custom_schemadir if custom_schemadir.exists() else pathlib.Path("schemas").absolute()
    )
    expected_stdout = (fail_test_case / "expected_stdout.txt").read_text().split("\n")
    expected_stderr = (fail_test_case / "expected_stderr.txt").read_text().split("\n")

    cp = build_tool_validator.run(
        "--sourcedir",
        fail_test_case / "src",
        "--schemadir",
        schemadir,
        "--outputdir",
        outputdir,
        "--version",
        "0.0.1",
    )

    assert cp.returncode != 0

    assert all(line in cp.stdout for line in expected_stdout)
    assert all(line in cp.stderr for line in expected_stderr)


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
