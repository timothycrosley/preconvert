#!/bin/bash

./lint.sh
pipenv run pytest -s --cov=preconvert --cov=tests --cov-report=term-missing ${@}
