#!/usr/bin/env bash

set -e

cd "$(dirname "$0")"

VENV_DIR=".venv"
REQ_FILE="requirements.txt"

if ! command -v python >/dev/null 2>&1; then
    echo "python not found in PATH" >&2
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtualenv..."
    python -m venv "$VENV_DIR"
fi

. "$VENV_DIR/bin/activate"

if [ -f "$REQ_FILE" ]; then
    STAMP="$VENV_DIR/.requirements.stamp"
    if [ ! -f "$STAMP" ] || [ "$REQ_FILE" -nt "$STAMP" ]; then
        echo "Installing dependencies..."
        pip install -r "$REQ_FILE"
        touch "$STAMP"
    fi
fi

exec python ./main.py
