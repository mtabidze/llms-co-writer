#!/usr/bin/env bash
# Copyright (c) 2023 Mikheil Tabidze
# This script performs unit testing using PyTest.

echo -e "\nUnit testing has begun\n"

# Perform unit testing with coverage
coverage run \
  --source=app --data-file=cover/unit-testing/unit-testing.coverage --module \
  pytest --verbose --random-order tests/unit_tests
UNIT_TESTING_EXIT_CODE=$?

# Save coverage report
coverage html \
  --data-file=cover/unit-testing/unit-testing.coverage --directory=cover/unit-testing/html

# Display results
echo -e "\nUnit testing has completed with exit code ${UNIT_TESTING_EXIT_CODE}\n"

# Return the exit code
if [ $UNIT_TESTING_EXIT_CODE -ne 0 ];
then
  return 1
fi
