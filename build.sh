#!/bin/bash


# The following code is necessary to make CLI arguments work (with long flag names). 
# These arguments are necessary to make the script configurable and testable.
TEMP=$(getopt -o o: --long configs:,conditions:,output: \
              -n 'build' -- "$@")

if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi

OUTPUT=./build
CONDITIONS=./conditions
CONFIGS=./remote_configurations
CLUSTER_MAPPING=cluster-mapping.json

while true; do
  case "$1" in
    --configs ) CONFIGS=$2 ; shift 2 ;;
    --conditions ) CONDITIONS=$2 ; shift 2 ;;
    -o | --output ) OUTPUT=$2 ; shift 2 ;;
    -- ) shift; break ;;
    * ) break ;;
  esac
done

mkdir -p ${OUTPUT}/v1
mkdir -p ${OUTPUT}/v2

# Determine version
NUMBER_OF_HEAD_TAGS=$(git tag --points-at HEAD | wc -l)
if [ $NUMBER_OF_HEAD_TAGS -gt 1 ]; then
    echo "ERROR: Cannot determine version. HEAD has more than one tag."
    exit 1
fi
VERSION=$(git describe --tags | sed 's/\(.*\)-\(.*\)/\1+\2/')
# Outputs:
# 1.1.1 if HEAD has the 1.1.1 tag
# 1.1.1-4+g3615c20 if HEAD is g3615c20, 4 commits ahead of the 1.1.1 tag

# Build the conditions for v1 endpoint
jq --arg VERSION $VERSION \
    -s '{ version: $VERSION, rules: map(.) }' ${CONDITIONS}/*.json > ${OUTPUT}/v1/rules.json

# Build remote configurations for v2 endpoint
for config_template in ${CONFIGS}/*; do
    # build JSON array with contents of all required conditions
    contents='['
    while read -r condition; do 
	contents+=$(cat ${CONDITIONS}/${condition}.json)
	contents+=','
    done < <(jq -r '.conditional_gathering_rules[]' $config_template)
    # remove last comma from the array
    contents=${contents%?}
    contents+=']'
    # build entire config with contents and the version
    jq --argjson contents "${contents}" --arg VERSION $VERSION '.version=$VERSION | .conditional_gathering_rules=$contents' $config_template > ${OUTPUT}/v2/$(basename $config_template)
done

cp ${CLUSTER_MAPPING} ${OUTPUT}/ 
