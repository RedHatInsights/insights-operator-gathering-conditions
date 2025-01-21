# Contributing

## Development Environment

Python and Go are required.
Although we expect this project to work on most versions of both,
to check the specific version we support see the ones used in the CI workflow
(see `.github/workflows/ci.yaml`).

```shell script
# Python environment for pre-commit and validate.py
python3 -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt
```

## Testing

```shell script
pytest
```

### Linting

```shell script
pre-commit run --all-files
```

## Remote Configuration Data Management

### Conditional Gathering Rules

TBD

### Container Log Requests

TBD

### Cluster Version Mapping

TBD
