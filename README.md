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

* `conditional_gathering_rules/*.json` -
  A library of conditional gathering rules.
  TODO: schema reference
* `container_log_requests/*/*.json` -
  A library of container log requests, organized by their source.
  TODO: schema reference
* `templates_v1/rules.json` -
  A template for the remote configuration served by the `v1` API of the
  [Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service).
  TODO: schema reference
* `templates_v2/cluster_version_mapping.json` -
  A mapping between cluster version ranges and remote configurations used by the
  [Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service)
  for the `v2` API.
  TODO: schema reference
* `templates_v2/remote_configurations/*.json` -
  Templates for remote configurations served by the `v2` API of the
  [Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service).
  TODO: schema reference


## Build

The [`build.sh`](./build.sh) script expands templates in `templates_v1` and `templates_v2`
into files expected by the
[Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service).

```shell script
git clone -o upstream https://github.com/RedHatInsights/insights-operator-gathering-conditions
cd insights-operator-gathering-conditions
# the build.sh script needs version tags
git fetch -p origin
/bin/bash build.sh
```


## Generated Files

The [Insights Operator Gathering Conditions Service](https://github.com/redhatinsights/insights-operator-gathering-conditions-service)
requires the following files to operate:

* `build/v1/rules.json` -
  The remote configuration returned by the `v1` API.
  TODO: schema reference
* `build/v2/*.json` -
  Remote configurations returned by the `v2` API.
  TODO: schema reference
* `build/cluster_mapping.json` -
  A file mapping cluster version ranges to specific v2 remote configurations.
  TODO: schema reference
