#!/bin/bash
set -euxo pipefail

poetry run cruft check
poetry run mypy --ignore-missing-imports preconvert/
poetry run isort --check --diff preconvert/ tests/
poetry run black --check preconvert/ tests/
poetry run flake8 preconvert/ tests/
poetry run safety check
poetry run bandit -r preconvert/
