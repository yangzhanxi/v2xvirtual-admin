#!/bin/bash

# Run unit tests
python -m pytest \
    --pycodestyle \
    --isort \
    --flakes \
    --mypy \
    --cache-clear \
    --cov=. \
    -k "./venv"