#!/usr/bin/env bash

rm -rf .venv

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Starting the virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
python3 -m pip install --upgrade -r requirements.txt

echo "Ignore the following error if you are not on NixOS: "
fix-python --venv .venv --libs assets/nix/libs.nix
