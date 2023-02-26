#!/bin/bash
# https://pypi.org/project/pip-tools/
source "$(dirname "$0")"/functions.sh
run_command pip-compile requirements.in