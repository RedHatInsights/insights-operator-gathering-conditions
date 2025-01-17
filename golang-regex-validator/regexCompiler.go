package main

import (
	"io"
	"os"
	"regexp"
)

func main() {
	bytes, err := io.ReadAll(os.Stdin)
	if err != nil {
		panic(err)
	}
	regex := string(bytes)

	regexp.MustCompile(regex)
}
