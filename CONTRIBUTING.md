# Contributing

## Development Environment

The development environment is the same as the build environment.
See the [Build](README.md#build) section in [README.md](./README.md).

## Linters

```shell script
pre-commit run --all-files
```

## Tests

All tests are implemented using `pytest`. The tests cover:

* Source data validation and enforcement of conventions
* Tests for the [build tool](./build.py)
* Tests for [golang_regex_validator](./golang_regex_validator),
  a tool used by the build tool and other tests

All test can be executed in one go:

```shell script
pytest --cov . --cov-report term-missing
```

## Remote Configuration Data Management

### Conditional Gathering Rules

TBD

### Container Log Requests

TBD

### Cluster Version Mapping

TBD
