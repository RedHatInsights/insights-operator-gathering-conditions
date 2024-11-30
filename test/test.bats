#!/usr/bin/env bash

TEST_OUTPUT=./test/build
TEST_CONDITIONS=./test/conditions
TEST_CONFIGURATIONS=./test/remote_configurations

setup() {
    load 'test_helper/bats-support/load'
    load 'test_helper/bats-assert/load'
}

@test "test v1 config conditions" {
    ./build.sh --conditions $TEST_CONDITIONS --output $TEST_OUTPUT --configs $TEST_CONFIGURATIONS
    # check the config for v1 has been created
    assert [ -f ${TEST_OUTPUT}/v1/rules.json ]
    # check number of conditions in resulting config
    assert [ $(jq '.rules | length' ${TEST_OUTPUT}/v1/rules.json) -eq 3 ]
    # check all conditions in resulting config
    run cat ${TEST_OUTPUT}/v1/rules.json
    assert_line --partial 'TestCondition1'
    assert_line --partial 'TestCondition2'
    assert_line --partial 'TestCondition3'
}

@test "test v2 configs conditions" {
    ./build.sh --conditions $TEST_CONDITIONS --output $TEST_OUTPUT --configs $TEST_CONFIGURATIONS
    # check that configurations have been created
    assert [ -f ${TEST_OUTPUT}/v2/config1.json ]
    assert [ -f ${TEST_OUTPUT}/v2/config2.json ]
    # check number of conditions in resulting configs
    assert [ $(jq '.conditional_gathering_rules | length' ${TEST_OUTPUT}/v2/config1.json) -eq 2 ]
    assert [ $(jq '.conditional_gathering_rules | length' ${TEST_OUTPUT}/v2/config2.json) -eq 2 ]
    # check conditions in the first config
    run cat ${TEST_OUTPUT}/v2/config1.json
    assert_line --partial 'TestCondition1'
    assert_line --partial 'TestCondition2'
    refute_line --partial 'TestCondition3'
    # check conditions in the second config
    run cat ${TEST_OUTPUT}/v2/config2.json
    assert_line --partial 'TestCondition1'
    refute_line --partial 'TestCondition2'
    assert_line --partial 'TestCondition3'
}

@test "test v2 configs container_logs field" {
    ./build.sh --conditions $TEST_CONDITIONS --output $TEST_OUTPUT --configs $TEST_CONFIGURATIONS
    # check that configurations have been created
    assert [ -f ${TEST_OUTPUT}/v2/config1.json ]
    assert [ -f ${TEST_OUTPUT}/v2/config2.json ]
    # check container_logs in the first config is empty
    run jq '.container_logs' ${TEST_OUTPUT}/v2/config1.json
    assert_output '[]'
    # check container_logs in the second config
    run jq '.container_logs' ${TEST_OUTPUT}/v2/config2.json
    assert_line --partial 'namespace1'
    assert_line --partial 'test message'

}

@test "test cluster-mapping.json included" {
    ./build.sh --conditions $TEST_CONDITIONS --output $TEST_OUTPUT --configs $TEST_CONFIGURATIONS
    # check that cluster-mapping.json has been created
    assert [ -f ${TEST_OUTPUT}/cluster-mapping.json ]

}

teardown() {
    rm -r $TEST_OUTPUT
}
