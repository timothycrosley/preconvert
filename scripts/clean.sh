#!/bin/bash
set -euxo pipefail

poetry run isort preconvert/ tests/
poetry run black preconvert/ tests/
