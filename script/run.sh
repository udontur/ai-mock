#!/usr/bin/env bash

python -m gunicorn api.asgi:application -k uvicorn.workers.UvicornWorker
