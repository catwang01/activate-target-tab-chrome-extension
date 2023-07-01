#!/bin/bash
set -o allexport
source .env
set +o allexport
.venv/bin/python server.py
# python -m debugpy --listen 5678 --wait-for-client server.py
