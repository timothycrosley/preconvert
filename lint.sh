#!/bin/bash

pipenv run mypy --ignore-missing-imports preconvert/
pipenv run isort --check --diff --recursive preconvert/
pipenv run black --check -l 100 preconvert/
pipenv run flake8 --max-line 100 --ignore F403,F401
pipenv run safety check
pipenv run bandit -r preconvert
