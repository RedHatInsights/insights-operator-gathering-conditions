# A nasty basic implementation with no tests to preserve the ability to build data required by the
# service.

import argparse
import json
import pathlib
import shutil

import git
import semver


class RemoteConfigurations:
    def __init__(self, sourcedir, version):
        self.sourcedir = pathlib.Path(sourcedir)
        self.version = version if version else self.get_version_from_git()
        self.configs_v1 = {}
        self.configs_v2 = {}

        self._load_v1_config()
        self._load_v2_configs()

    def get_version_from_git(self):
        repo = git.Repo(self.sourcedir)
        raw_version = repo.git.describe("--tags", "--long")
        return self.parse_version_from_git(raw_version)

    def _load_v1_config(self):
        template_name = "rules.json"
        template_file = self.sourcedir / "templates_v1" / template_name
        template = self._load_json(template_file)
        self.configs_v1[template_name] = {
            "rules": self._expand_glob_list(template["rules"]),
            "version": self.version,
        }

    def _load_v2_configs(self):
        templates_dir = self.sourcedir / "templates_v2" / "remote_configurations"
        for template_file in templates_dir.glob("*.json"):
            template = self._load_json(template_file)
            self.configs_v2[template_file.name] = {
                "conditional_gathering_rules": self._expand_glob_list(
                    template["conditional_gathering_rules"]
                ),
                "container_logs": self._expand_glob_list(template["container_logs"]),
                "version": self.version,
            }

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
        outputdir = pathlib.Path(outputdir)
        self._write_v1(outputdir / "v1")
        self._write_v2(outputdir / "v2")

    def _write_v1(self, outputdir):
        outputdir.mkdir(parents=True, exist_ok=True)
        self._write_configs(outputdir, self.configs_v1)

    def _write_v2(self, outputdir):
        (outputdir / "remote_configurations").mkdir(parents=True, exist_ok=True)
        self._write_cluster_version_mapping(outputdir)
        self._write_configs(outputdir / "remote_configurations", self.configs_v2)

    def _write_cluster_version_mapping(self, outputdir):
        # preserve non-standard formatting of the file
        srcpath = self.sourcedir / "templates_v2" / "cluster_version_mapping.json"
        dstpath = outputdir / "cluster_version_mapping.json"
        shutil.copy(srcpath, dstpath)

    @staticmethod
    def _load_json(path):
        return json.loads(path.read_text())

    @staticmethod
    def _write_configs(outputdir, configs):
        for filename in configs:
            filepath = outputdir / filename
            filepath.write_text(json.dumps(configs[filename]))

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
    remote_configs = RemoteConfigurations(args.sourcedir, args.version)
    remote_configs.write(args.outputdir)


if __name__ == "__main__":
    main()
