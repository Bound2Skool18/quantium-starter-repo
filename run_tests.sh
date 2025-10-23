#!/usr/bin/env bash
set -u -o pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${REPO_DIR}/.venv"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Virtual environment not found at: $VENV_DIR"
  exit 1
fi

# Ensure chromedriver is available (required by dash[testing]/selenium)
if ! command -v chromedriver >/dev/null 2>&1; then
  echo "chromedriver not found in PATH. Install it (e.g., 'brew install chromedriver') and re-run."
  exit 1
fi

# Activate venv
# shellcheck disable=SC1090
source "${VENV_DIR}/bin/activate"

# Run tests headlessly
pytest -q --maxfail=1 --disable-warnings --headless --webdriver=Chrome
STATUS=$?

deactivate || true

if [[ $STATUS -eq 0 ]]; then
  echo "All tests passed."
  exit 0
else
  echo "Tests failed."
  exit 1
fi