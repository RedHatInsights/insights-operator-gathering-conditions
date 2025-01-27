# Insights Operator Remote Configuration Data

[Insights Operator](https://github.com/openshift/insights-operator) is an
OpenShift cluster operator which enables Insights Advisor and other remote
health monitoring services for OpenShift. This repository manages data for
Insights Operator features that consume dynamic (remote) configuration:
[Conditional Gathering](https://github.com/openshift/insights-operator/blob/master/docs/conditional-gatherer/README.md)
and [Rapid Recommendations](https://github.com/openshift/enhancements/blob/master/enhancements/insights/rapid-recommendations.md).

The Insights Operator downloads the remote configuration from
[Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service),
a service running on the [Red Hat Hybrid Cloud Console](https://developers.redhat.com/api-catalog/api/gathering).
The service provides two API versions:

* `v1` is used by Insights Operators in OCP 4.9-4.16. This API version provides
  only remote configuration for the Conditional Gathering feature.
* `v2` is used by Insights Operators in OCP 4.17 and newer. This API version
  provides remote configuration for both Conditional Gathering and Rapid
  Recommendations features.

The [Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service)
uses data that is generated from data in this repository.


## Repository Structure

Remote configuration data is stored in a modular way that is convenient for
managing the data (see the [contributing documentation](CONTRIBUTING.md) for
details).

* `conditional_gathering_rules/*.json`
  [[schema](https://github.com/RedHatInsights/insights-operator-gathering-conditions/blob/main/schemas/gathering_rule.schema.json)]
  * A library of conditional gathering rules.
* `container_log_requests/*/*.json`
  [[schema](https://github.com/RedHatInsights/insights-operator-gathering-conditions/blob/main/schemas/container_log.schema.json)]
  * A library of container log requests, organized by their source.
* `templates_v1/rules.json`
  [[schema](https://github.com/RedHatInsights/insights-operator-gathering-conditions/blob/main/schemas/remote_configuration_v1_template.schema.json)]
  * A template for the remote configuration served by the `v1` API of the
    [[Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service)].
* `templates_v2/cluster_version_mapping.json`
  [[schema](https://github.com/RedHatInsights/insights-operator-gathering-conditions/blob/main/schemas/cluster_version_mapping.schema.json)]
  * A mapping between cluster version ranges and remote configurations used by the
    [Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service)
    for the `v2` API.
* `templates_v2/remote_configurations/*.json`
  [[schema](https://github.com/RedHatInsights/insights-operator-gathering-conditions/blob/main/schemas/remote_configuration_v2_template.schema.json)]
  * Templates for remote configurations served by the `v2` API of the
    [Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service).


## Build

The [`build.py`](./build.py) script expands templates in `templates_v1` and `templates_v2`
into files needed by the
[Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service).

Python and Go are required.
We expect this project to work on most versions of both.
To check the specific version we test and use,
see the [CI workflow configuration](.github/workflows/ci.yaml).

```shell script
# clone repo
git clone -o upstream https://github.com/RedHatInsights/insights-operator-gathering-conditions
cd insights-operator-gathering-conditions
git fetch -p upstream   # the build.py script needs version tags

# prepare runtime environment
python3 -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt

# run the build script
python build.py
```

The tool supports a few command line arguments, mostly for testing purposes. Run `python build.py --help` for details.


## Generated Files

The [`build.py`](./build.py) script generates the following files:

* `build/v1/rules.json`
  [[schema](https://github.com/RedHatInsights/insights-operator-gathering-conditions/blob/main/schemas/remote_configuration_v1.schema.json)]
  * The remote configuration returned by the `v1` API.
* `build/v2/*.json`
  [[schema](https://github.com/RedHatInsights/insights-operator-gathering-conditions/blob/main/schemas/remote_configuration_v2.schema.json)]
  * Remote configurations returned by the `v2` API.
* `build/cluster_mapping.json`
  [[schema](https://github.com/RedHatInsights/insights-operator-gathering-conditions/blob/main/schemas/cluster_version_mapping.schema.json)]
  * A file mapping cluster version ranges to specific v2 remote configurations.
* `build/v2/remote_configurations/*.json`
  [TODO: schema link]
  * Remote configurations returned by the `v2` API.
Note that the [Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service)
needs the files in a slightly different structure at the moment. The differences are handled in its
[`get_condtions.sh`](https://github.com/redhatinsights/insights-operator-gathering-conditions-service/blob/main/get_conditions.sh) script.
