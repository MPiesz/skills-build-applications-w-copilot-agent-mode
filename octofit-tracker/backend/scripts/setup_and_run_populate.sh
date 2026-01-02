#!/usr/bin/env bash
set -euo pipefail

# Paths (absolute workspace path)
ROOT="/workspaces/skills-build-applications-w-copilot-agent-mode"
BACKEND="$ROOT/octofit-tracker/backend"
VENV="$BACKEND/venv"

echo "Creating virtualenv at $VENV..."
python3 -m venv "$VENV"

echo "Activating virtualenv and installing requirements..."
# shellcheck source=/dev/null
source "$VENV/bin/activate"
pip install --upgrade pip
pip install -r "$BACKEND/requirements.txt"

echo "Running migrations and populate_db..."
python "$BACKEND/manage.py" migrate --noinput
python "$BACKEND/manage.py" populate_db

echo "Done."
