#!/usr/bin/env bash

set -o errexit

print "Python version: "
python3 --version
print "\n"

echo "Installing & Building Dependencies... "
pip install -r requirements.txt

echo "Collecting static files... "
python3 manage.py collectstatic --no-input
