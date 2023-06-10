#!/bin/bash
set -o allexport
source .env
set +o allexport
.venv/bin/python3 server.py
