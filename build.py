# A nasty basic implementation with no tests to preserve the ability to build data required by the
# service.

import glob
import json
import pathlib
import sys


OUTPUT = "./build"

VERSION = sys.argv[1]


def load_json_file(src_path):
    with open(str(src_path)) as fd:
        return json.load(fd)


def expand_remote_config_source(config_source, glob_list_keys):
    config = {}
    config["version"] = VERSION
    for key in glob_list_keys:
        config[key] = expand_glob_list(config_source[key])
    return config


def expand_glob_list(globs):
    results = []
    for g in globs:
        for path in glob.glob(g):
            config_part = load_json_file(path)
            results.append(config_part)
    return results


def produce_v2_config(src_path, output_dir):
    config_source = load_json_file(src_path)
    config = expand_remote_config_source(config_source, ["conditional_gathering_rules", "container_logs"])
    dst_path = output_dir / src_path.name
    dst_path.write_text(json.dumps(config))


def copy_cluster_version_mapping(output_dir):
    src_path = pathlib.Path("templates_v2/cluster_version_mapping.json")
    dst_path = output_dir / "cluster-mapping.json"
    dst_path.write_text(src_path.read_text())


def produce_v2_configs():
    build_dir = pathlib.Path(OUTPUT)
    output_dir = build_dir / "v2"
    output_dir.mkdir(parents=True, exist_ok=True)
    copy_cluster_version_mapping(build_dir)
    for src_path in glob.glob("templates_v2/remote_configurations/*.json"):
        src_path = pathlib.Path(src_path)
        produce_v2_config(src_path, output_dir)


def produce_v1_config():
    dst_path = pathlib.Path(OUTPUT) / "v1" / "rules.json"
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    config_source = load_json_file("templates_v1/rules.json")
    config = expand_remote_config_source(config_source, ["rules"])
    dst_path.write_text(json.dumps(config))


def main():
    produce_v1_config()
    produce_v2_configs()


if __name__ == "__main__":
    main()
