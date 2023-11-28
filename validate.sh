#!/bin/sh -e

# echo '>>> Cleaning cache'
# rm -rf backend/.mypy_cache
# rm -rf backend/.pytest_cache
# rm -rf backend/__pycache__

echo '>>> Skipping Pylint'
# pylint -E -v backend/*.py
# pylint -E -v backend/router
# pylint -E -v backend/sql_app

echo '>>> Running Mypy'
mypy backend

## currently no tests
# echo '>>> Running Pytest'
# pytest -vv --doctest-modules -s backend # --disable-warnings

echo '>>> Running Black'
black backend
