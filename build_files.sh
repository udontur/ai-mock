#!/usr/bin/env bash

echo "Installing & Building Dependencies... "
python3 -m pip instgall -r requirements.txt

echo "Collecting static files... "
python3 manage.py collectstatic --noinput
