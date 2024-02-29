#!/bin/bash
set -euo pipefail

# Run unit tests
python -m pytest \
    --pycodestyle \
    --isort \
    --flakes \
    --mypy \
    --cache-clear \
    --cov=. \
    --junitxml=build/pytest.xml\
    "$@"
