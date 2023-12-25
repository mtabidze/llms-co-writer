#!/usr/bin/env bash
# Copyright (c) 2023 Mikheil Tabidze
# This script performs coverage measurement.

echo -e "\nCoverage measurement has begun\n"

# Perform coverage measurement
coverage report --data-file=cover/unit-testing/unit-testing.coverage --fail-under=80
UNIT_TESTING_COVERAGE_EXIT_CODE=$?
coverage report --data-file=cover/functional-testing/functional-testing.coverage --fail-under=70
FUNCTIONAL_TESTING_COVERAGE_EXIT_CODE=$?

# Display results
echo -e "\nCoverage measurement has completed with the following results:\n" \
  "  1. Unit testing coverage exit code - ${UNIT_TESTING_COVERAGE_EXIT_CODE}\n" \
  "  2. Functional testing coverage exit code - ${FUNCTIONAL_TESTING_COVERAGE_EXIT_CODE}\n"

# Determine overall result
COVERAGE_MEASUREMENT_RESULT=$(( \
  UNIT_TESTING_COVERAGE_EXIT_CODE + \
  FUNCTIONAL_TESTING_COVERAGE_EXIT_CODE \
  ))

# Return the overall exit code
if [ $COVERAGE_MEASUREMENT_RESULT -ne 0 ];
then
  return 1
fi
