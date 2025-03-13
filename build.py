# A nasty basic implementation with no tests to preserve the ability to build data required by the
# service.

import argparse
import json
import logging
import logging.config
import pathlib
import shutil
import subprocess

import git
import jsonschema
import semver
from referencing import Registry, Resource

logger = logging.getLogger(__name__)

logging_config = {
    "version": 1,
    "incremental": False,
    "formatters": {
        "console": {"format": "[%(asctime)s] %(levelname)s: %(message)s"},
    },
    "handlers": {
        "console": {
            "formatter": "console",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "__main__": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


class ClusterVersionMappingError(RuntimeError):
    """An exception used to report cluster version mapping validation errors."""


class RegexValidationError(RuntimeError):
    """An exception used to report invalid regular expressions."""


class GolangRegexValidator:
    """Wrapper for running a golang validation tool as a subprocess."""

    def __init__(self, file):
        self._file = str(file)

    def validate(self, regex):
        return subprocess.run(
            ["go", "run", self._file], input=regex, capture_output=True, encoding="utf-8"
        )


class RemoteConfigurations:
    def __init__(self, sourcedir, version, schemadir):
        logger.info(f"Current working directory: {pathlib.Path().absolute()}")

        self.schemadir = pathlib.Path(schemadir).absolute()
        logger.info(f"Schema directory: {self.schemadir}")

        self.sourcedir = pathlib.Path(sourcedir).absolute()
        logger.info(f"Source directory: {self.sourcedir}")

        self.version = version if version else self.get_version_from_git()
        logger.info(f"Remote configuration version: {self.version}")

        regex_validator_path = pathlib.Path() / "golang_regex_validator" / "regexCompiler.go"
        self.regex_validator = GolangRegexValidator(regex_validator_path)
        logger.info(f"Golang regex validator: {regex_validator_path}")

        self.registry = Registry(retrieve=self._retrieve_schema)
        self.configs_v1 = {}
        self.cluster_version_mapping = None
        self.configs_v2 = {}

        self._load_v1_config()
        self._load_v2_configs()

    def _retrieve_schema(self, schema_ref):
        schema_path = self.schemadir / schema_ref
        return Resource.from_contents(json.loads(schema_path.read_text()))

    def get_version_from_git(self):
        logger.info(f"Determining remote configuration version from Git repo: {self.sourcedir}")
        repo = git.Repo(self.sourcedir)
        raw_version = repo.git.describe("--tags", "--long")
        return self.parse_version_from_git(raw_version)

    def _load_v1_config(self):
        blueprint_name = "rules.json"
        blueprint_file = self.sourcedir / "blueprints_v1" / blueprint_name
        logger.info(f"Building config from v1 blueprint: {blueprint_file}")
        blueprint = self._load_json(blueprint_file)
        self.configs_v1[blueprint_name] = {
            "rules": self._expand_glob_list(blueprint["rules"]),
            "version": self.version,
        }

    def _load_v2_configs(self):
        blueprints_v2 = self.sourcedir / "blueprints_v2"
        self._load_v2_cluster_version_mapping(blueprints_v2)
        self._load_v2_remote_configurations(blueprints_v2)

    def _load_v2_cluster_version_mapping(self, blueprints_v2):
        filepath = self._get_v2_cluster_version_mapping_path(blueprints_v2)
        logger.info(f"Loading cluster version mapping blueprint: {filepath}")
        self.cluster_version_mapping = self._load_json(filepath)
        self._assert_json_schema(
            filepath, self.cluster_version_mapping, "cluster_version_mapping.schema.json"
        )
        self._assert_cluster_version_mapping_first_interval(filepath, self.cluster_version_mapping)
        self._assert_cluster_version_mapping_order(filepath, self.cluster_version_mapping)

    def _load_v2_remote_configurations(self, blueprints_v2):
        for i, (_, filename) in enumerate(self.cluster_version_mapping):
            # The same remote configuration file can be used for multiple version ranges.
            if filename in self.configs_v2:
                continue

            blueprint_path = self._get_v2_remote_configuration_blueprint_path(
                blueprints_v2, i, filename
            )

            logger.info(f"Building config from v2 blueprint: {blueprint_path}")
            blueprint = self._load_json(blueprint_path)
            self.configs_v2[filename] = {
                "conditional_gathering_rules": self._expand_glob_list(
                    blueprint["conditional_gathering_rules"]
                ),
                "container_logs": self._expand_glob_list(blueprint["container_logs"]),
                "version": self.version,
            }

    @staticmethod
    def _get_v2_cluster_version_mapping_path(root_v2):
        return root_v2 / "cluster_version_mapping.json"

    @staticmethod
    def _get_v2_remote_configuration_path(root_v2, filename):
        return root_v2 / "remote_configurations" / filename

    def _get_v2_remote_configuration_blueprint_path(self, blueprints_v2, idx, filename):
        blueprint_path = self._get_v2_remote_configuration_path(blueprints_v2, filename)

        if not blueprint_path.is_file():
            cluster_version_mapping_path = self._get_v2_cluster_version_mapping_path(blueprints_v2)
            e = ClusterVersionMappingError(
                f"'{filename}' does not reference a valid config at index {idx}: "
                f"{cluster_version_mapping_path}; "
                f"expected remote configuration blueprint path: {blueprint_path}"
            )
            logger.critical(f"❌ {e.__class__.__name__}: {e}")
            raise (e)

        return blueprint_path

    def _expand_glob_list(self, globs):
        loaded_paths = set()
        results = []
        for g in globs:
            for path in sorted(self.sourcedir.glob(g)):
                if path not in loaded_paths:
                    loaded_paths.add(path)
                    data = self._load_json(path)
                    results.append(data)
        return results

    def write(self, outputdir):
        outputdir = pathlib.Path(outputdir).absolute()
        logger.info(f"Output directory: {outputdir}")
        self._write_v1(outputdir / "v1")
        self._write_v2(outputdir / "v2")

    def _write_v1(self, outputdir_v1):
        logger.info("Writing v1 configs")
        outputdir_v1.mkdir(parents=True, exist_ok=True)
        for filename, config in self.configs_v1.items():
            filepath = outputdir_v1 / filename
            self._write_config(filepath, config)
            self._assert_json_schema(filepath, config, "remote_configuration_v1.schema.json")

    def _write_v2(self, outputdir_v2):
        logger.info("Writing v2 configs")
        remote_config_dir = outputdir_v2 / "remote_configurations"
        remote_config_dir.mkdir(parents=True, exist_ok=True)
        self._write_v2_cluster_version_mapping(outputdir_v2)
        self._write_v2_remote_configurations(remote_config_dir)

    def _write_v2_cluster_version_mapping(self, outputdir_v2):
        srcpath = self.sourcedir / "blueprints_v2" / "cluster_version_mapping.json"
        dstpath = outputdir_v2 / "cluster_version_mapping.json"
        logger.info(f"Writing cluster_version_mapping.json: {dstpath}")
        # preserve non-standard formatting of the file
        shutil.copy(srcpath, dstpath)

    def _write_v2_remote_configurations(self, remote_config_dir):
        for filename, config in self.configs_v2.items():
            filepath = remote_config_dir / filename
            self._write_config(filepath, config)
            self._assert_json_schema(filepath, config, "remote_configuration_v2.schema.json")
            self._assert_valid_pod_name_regexes(filepath, config)
            self._assert_valid_message_filters(filepath, config)

    def _assert_cluster_version_mapping_first_interval(self, filepath, content):
        first_version = content[0][0]
        if semver.Version.parse(first_version) > semver.Version(4, 17, 0, prerelease=0):
            e = ClusterVersionMappingError(
                f"Invalid first interval: '{first_version}' is greater than '4.17.0-0': {filepath}"
            )
            e.add_note(
                "\nThe cluster_version_mapping.json file has to cover all OCP versions "
                "with the Rapid Recommendations feature (OCP 4.17.0-0 and greater)."
            )
            logger.critical(f"❌ {e.__class__.__name__}: {e}")
            raise (e)

    def _assert_cluster_version_mapping_order(self, filepath, content):
        v1 = None
        for i, (raw_version, _) in enumerate(content):
            v2 = semver.Version.parse(raw_version)
            if v1 is None or v1 < v2:
                v1 = v2
            else:
                e = ClusterVersionMappingError(
                    f"'{v1}' is NOT smaller than '{v2}' in semantic versioning "
                    f"at index {i}: {filepath}"
                )
                e.add_note(
                    "\nPairs in the cluster_version_mapping.json file "
                    "must have strictly increasing semantic versions."
                )
                logger.critical(f"❌ {e.__class__.__name__}: {e}")
                raise (e)

    def _assert_valid_pod_name_regexes(self, filepath, config):
        for i, request in enumerate(config["container_logs"]):
            regex = request["pod_name_regex"]
            validation = self.regex_validator.validate(regex)
            if validation.returncode != 0:
                e = RegexValidationError(
                    f"Invalid golang regular expression in '.container_logs[{i}].pod_name_regex': {filepath}"
                )
                e.add_note(validation.stderr)
                logger.critical(f"❌ {e.__class__.__name__}: {e}")
                raise (e)

    def _assert_valid_message_filters(self, filepath, config):
        filters = []
        for request in config["container_logs"]:
            filters.extend(request["messages"])
        # This is an over-approximation - we are trying to compile the biggest regular expression
        # that the Insights Operator could use based on the given config. This would occur for a pod
        # name that would match the pod name regexes in all requests, which is unlikely. If this
        # over-approximation starts producing false positives (each individual filter is valid but
        # the combined expression is not), we will need to consider other measures against message
        # filters that would exceed limits of golang regular expressions.
        regex = "|".join(filters)
        validation = self.regex_validator.validate(regex)
        if validation.returncode != 0:
            e = RegexValidationError(
                f"Message filters do not comprise a valid golang regular expression: {filepath}"
            )
            e.add_note(validation.stderr)
            logger.critical(f"❌ {e.__class__.__name__}: {e}")
            raise (e)

    @staticmethod
    def _load_json(path):
        logger.debug(f"Loading file: {path}")
        return json.loads(path.read_text())

    @staticmethod
    def _write_config(filepath, config):
        logger.info(f"Writing config: {filepath}")
        filepath.write_text(json.dumps(config))
        return filepath

    def _assert_json_schema(self, filepath, content, schema_ref):
        logger.info(f"Validating file against {schema_ref}: {filepath}")

        try:
            schema = self.registry.get_or_retrieve(schema_ref).value.contents
            jsonschema.validate(content, schema, registry=self.registry)

        except (jsonschema.ValidationError, jsonschema.SchemaError) as e:
            e.add_note(f"\nValidated file: {filepath}")
            e.add_note(f"Schema directory: {self.schemadir}")
            e.add_note(f"Schema: {schema_ref}")
            logger.critical(f"❌ JSON validation error: {e.__class__.__name__}: {e.message}")
            raise (e)

    @staticmethod
    def parse_version_from_git(raw_version):
        version = semver.Version.parse(raw_version)
        distance, commit = version.prerelease.split("-", 1)
        version_args = [version.major, version.minor, version.patch]
        if distance != "0":
            version_args.extend([distance, commit])
        return str(semver.Version(*version_args))


def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="build.py",
        description="Build tool for Insights Operator Gathering Conditions Service configuration.",
    )
    parser.add_argument(
        "--sourcedir",
        action="store",
        default=".",
        help="Path to a directory that stores configuration sources.",
    )
    parser.add_argument(
        "--outputdir",
        action="store",
        default="./build",
        help="Path to a directory where the produced configuration will be written. "
        "Existing files will be overwritten.",
    )
    parser.add_argument(
        "--schemadir",
        action="store",
        default="./schemas",
        help="Path to a directory with required JSON schemas.",
    )
    parser.add_argument(
        "--version",
        action="store",
        default=None,
        help="Configuration version. Defaults to the setuptools_scm version.",
    )
    return parser.parse_args()


def main():
    args = parse_arguments()
    remote_configs = RemoteConfigurations(args.sourcedir, args.version, args.schemadir)
    remote_configs.write(args.outputdir)
    logger.info("Done.")


if __name__ == "__main__":
    logging.config.dictConfig(logging_config)
    main()
