#!/usr/bin/env bash
# Copyright (c) 2023 Mikheil Tabidze
# This script performs static code analysis using various tools.

echo -e "\nStatic code analysis has begun\n"

# Perform static code analysis
bandit --severity-level all --confidence-level all --recursive ./app
BANDIT_EXIT_CODE=$?
pip-audit
PIP_AUDIT_EXIT_CODE=$?
pip-licenses --order=license --fail-on="GPL;GPLv2;GPLv3;LGPL;LGPLv2.1;LGPLv3"
PIP_LICENSES_EXIT_CODE=$?
flake8 --count app
FLAKE8_EXIT_CODE=$?
pylama app
PYLAMA_EXIT_CODE=$?
ruff check app
RUFF_EXIT_CODE=$?
black --check app
BLACK_EXIT_CODE=$?
isort --check app
ISORT_EXIT_CODE=$?

# Display results
echo -e "\nStatic code analysis has completed with the following results:\n" \
  "  1. bandit exit code - ${BANDIT_EXIT_CODE}\n" \
  "  2. pip-audit exit code - ${PIP_AUDIT_EXIT_CODE}\n" \
  "  3. pip-licenses exit code - ${PIP_LICENSES_EXIT_CODE}\n" \
  "  4. flake8 exit code - ${FLAKE8_EXIT_CODE}\n" \
  "  5. pylama exit code - ${PYLAMA_EXIT_CODE}\n" \
  "  6. ruff exit code - ${RUFF_EXIT_CODE}\n" \
  "  7. black exit code - ${BLACK_EXIT_CODE}\n" \
  "  8. isort exit code - ${ISORT_EXIT_CODE}\n"

# Determine overall result
STATIC_CODE_ANALYSIS_RESULT=$(( \
  BANDIT_EXIT_CODE + \
  PIP_AUDIT_EXIT_CODE + \
  PIP_LICENSES_EXIT_CODE + \
  FLAKE8_EXIT_CODE + \
  PYLAMA_EXIT_CODE + \
  RUFF_EXIT_CODE + \
  BLACK_EXIT_CODE + \
  ISORT_EXIT_CODE \
  ))

# Return the overall exit code
if [ $STATIC_CODE_ANALYSIS_RESULT -ne 0 ];
then
  return 1
fi
