#!/usr/bin/env bash

rm -rf .venv

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Starting the virtual environment..."
source .venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt
