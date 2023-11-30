#!/usr/bin/env bash
# Copyright (c) 2023 Mikheil Tabidze
# This script performs all testing using testing scripts.

echo -e "\nTesting has begun\n"

# Perform testing
source ./bin/run_unit_testing.sh "$*"
UNIT_TESTING_EXIT_CODE=$?
source ./bin/run_functional_testing.sh "$*"
FUNCTIONAL_TESTING_EXIT_CODE=$?
source ./bin/run_coverage_measurement.sh "$*"
COVERAGE_MEASUREMENT_EXIT_CODE=$?
source ./bin/run_static_code_analysis.sh "$*"
STATIC_CODE_ANALYSIS_EXIT_CODE=$?

# Display results
echo -e "\nTesting has completed with the following results:\n" \
  "  1. Unit testing exit code - ${UNIT_TESTING_EXIT_CODE}\n" \
  "  2. Functional testing exit code - ${FUNCTIONAL_TESTING_EXIT_CODE}\n" \
  "  3. Coverage measurement exit code - ${COVERAGE_MEASUREMENT_EXIT_CODE}\n" \
  "  4. Static code analysis exit code - ${STATIC_CODE_ANALYSIS_EXIT_CODE}\n"

# Determine overall result
TESTS_RESULT=$(( \
  UNIT_TESTING_EXIT_CODE + \
  FUNCTIONAL_TESTING_EXIT_CODE + \
  COVERAGE_MEASUREMENT_EXIT_CODE + \
  STATIC_CODE_ANALYSIS_EXIT_CODE \
  ))

# Return the overall exit code
if [ $TESTS_RESULT -ne 0 ];
then
  exit 1
fi
