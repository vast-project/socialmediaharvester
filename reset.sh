#!/bin/bash

sudo chown mapto:mapto -R db
sudo chown mapto:mapto -R data

sudo rm backend/index.html*
sudo rm -rf backend/.mypy_cache
sudo rm -rf backend/.pytest_cache
sudo rm -rf backend/__pycache__
