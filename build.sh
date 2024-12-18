#!/bin/bash

VERSION=$(git describe --tags --abbrev=0)
python build.py $VERSION
