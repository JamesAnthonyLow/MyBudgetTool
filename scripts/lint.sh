#!/bin/bash
source "$(dirname "$0")"/functions.sh
run_command 'black . && mypy . && isort .'
