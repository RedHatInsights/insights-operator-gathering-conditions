#!/bin/bash

mkdir -p ./build
mkdir -p ./build/v1
mkdir -p ./build/v2

# Build the conditions for v1 endpoint
VERSION=$(git describe --tags --abbrev=0)
jq --arg VERSION $VERSION \
    -s '{ version: $VERSION, rules: map(.) }' ./conditions/*.json > ./build/v1/rules.json

# Build remote configurations
for config_template in ./remote_configurations/*; do
    # build JSON array with contents of all required conditions
    contents='['
    while read -r condition; do 
	contents+=$(cat conditions/${condition}.json)
	contents+=','
    done < <(jq -r '.conditional_gathering_rules[]' $config_template)
    # remove last comma from the array
    contents=${contents%?}
    contents+=']'
    # build entire config with contents and the version
    jq --argjson contents "${contents}" --arg VERSION $VERSION '.version=$VERSION | .conditional_gathering_rules=$contents' $config_template > ./build/v2/$(basename $config_template)
done
