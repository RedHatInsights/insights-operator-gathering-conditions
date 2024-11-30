# Contributing

## Development Environment

```shell script
# Python environment for pre-commit and validate.py
python3 -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt

# dependencies for bats-based build.sh tests
git submodule update --init --recursive
```

## Testing

### Linting

```shell script
pre-commit run --all-files
```

### Configuration Sources

TBD (INSIGHTOCP-1967)

```shell script
python validate.py
```

### build.sh

`build.sh` script is tested using the [Bats](https://github.com/bats-core/bats-core) framework.

```
test/test_helper/bats/bin/bats test/test.bats
```

## Conditional gathering rules

TBD (INSIGHTOCP-1967)

## Container log requests

TBD (INSIGHTOCP-1967)

## Cluster version mapping

TBD (INSIGHTOCP-1967)

## build.sh

TBD (INSIGHTOCP-1967)
