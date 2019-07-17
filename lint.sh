#!/bin/bash

mypy --ignore-missing-imports preconvert/
isort --check --diff --recursive preconvert/
black --check -l 100 preconvert/
flake8 --max-line 100 --ignore F403,F401
safety check
bandit -r preconvert
