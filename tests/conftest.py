import json
import os
import pathlib
import subprocess
import sys

import deepdiff
import jsonschema
import pytest
from referencing import Registry, Resource

from tests import PROJECT_ROOT, SCHEMAS


@pytest.fixture(scope="session")
def repository_root():
    return PROJECT_ROOT


@pytest.fixture(scope="session")
def build_tool():
    return PROJECT_ROOT / "build.py"


class GolangRegexValidator:
    """Wrapper for running the golang tool as a subprocess

    Being it a class allows us to use it as a fixture were we can
    assert that we have the right file."""

    def __init__(self, file):
        self._file = file

    def run(self, input):
        return subprocess.run(
            ["go", "run", self._file], input=input, capture_output=True, encoding="utf-8"
        )


@pytest.fixture(scope="session")
def golang_regex_validator(repository_root):
    tool_file = repository_root / "golang_regex_validator/regexCompiler.go"
    assert tool_file.exists()
    validator = GolangRegexValidator(tool_file)
    return validator


class BuildToolValidator:
    def __init__(self, build_tool):
        self.build_tool = pathlib.Path(build_tool).absolute()

    def run(self, *args):
        cp = subprocess.run(
            ["python", self.build_tool, *args], capture_output=True, encoding="utf-8"
        )
        # have pytest print it out when a test fails
        print(cp.stdout)
        print(cp.stderr, file=sys.stderr)
        return cp

    def assert_same_config_dirs(self, dir1, dir2):
        dir1 = pathlib.Path(dir1)
        dir2 = pathlib.Path(dir2)

        files_in_dir1 = self.find_all_files(dir1)
        files_in_dir2 = self.find_all_files(dir2)

        difference1 = [str(dir1 / path) for path in files_in_dir1 - files_in_dir2]
        difference2 = [str(dir2 / path) for path in files_in_dir2 - files_in_dir1]

        assert files_in_dir1 == files_in_dir2, "\n".join(
            ["directories do not contain same files; file paths found in only one directory:"]
            + sorted(difference1 + difference2)
        )

        for relpath in sorted(files_in_dir1):
            file1 = dir1 / relpath
            file2 = dir2 / relpath
            self.assert_same_json_files(file1, file2)

    @staticmethod
    def assert_same_json_files(file1, file2):
        obj1 = json.loads(file1.read_text())
        obj2 = json.loads(file2.read_text())
        diff = deepdiff.DeepDiff(obj1, obj2)
        assert not diff, f"JSON objects differ:\n{json.dumps(diff, indent=4)}"

    @staticmethod
    def find_all_files(path):
        """Returns a set of relative paths of all files under a directory (recursively)."""
        files = set()
        # pathlib.Path.walk() has been added only in Python 3.12
        for dirpath, _, filenames in os.walk(str(path)):
            for filename in filenames:
                files.add(pathlib.Path(dirpath).relative_to(path) / filename)
        return files


@pytest.fixture()
def build_tool_validator(build_tool):
    return BuildToolValidator(build_tool)


class SchemaValidator:
    def __init__(self, schema_registry):
        self.schema_registry = schema_registry

    def validate(self, filepath, schemaref):
        content = json.loads(filepath.read_text())
        jsonschema.validate(
            content,
            self.schema_registry.get_or_retrieve(str(schemaref)).value.contents,
            registry=self.schema_registry,
        )


@pytest.fixture(scope="session")
def schema_validator():
    def retrieve_schema(schema_ref):
        return Resource.from_contents(json.loads((SCHEMAS / schema_ref).read_text()))

    schema_registry = Registry(retrieve=retrieve_schema)

    return SchemaValidator(schema_registry)
