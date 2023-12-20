#!/usr/bin/env bash
# Copyright (c) 2023 Mikheil Tabidze
# This script performs functional testing using PyTest.

echo -e "\nFunctional testing has begun\n"

# Perform functional testing with coverage
coverage run \
  --source=app --data-file=cover/functional-testing/functional-testing.coverage --module \
  pytest --verbose --random-order tests/functional_tests
FUNCTIONAL_TESTING_EXIT_CODE=$?

# Save coverage report
coverage html \
  --data-file=cover/functional-testing/functional-testing.coverage --directory=cover/functional-testing/html

# Display results
echo -e "\nFunctional testing has completed with exit code ${FUNCTIONAL_TESTING_EXIT_CODE}\n"

# Return the exit code
if [ $FUNCTIONAL_TESTING_EXIT_CODE -ne 0 ];
then
  return 1
fi
