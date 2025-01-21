
# Golang Regex Validator

This tool reads a Golang regular expression from the standard input and checks whether it can be compiled.
The result is indicated by the exit status.

To use it:

```go run regexCompiler.go```

## Tests

Tests validating the tool itself are implemented using `pytest` and located in `tests/golang_regex_validator`. Other `pytest` tests then use the tool to validate data contained in this repository.
