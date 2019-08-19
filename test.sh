#!/bin/bash -xe

./lint.sh
pipenv run pytest -s --cov=preconvert --cov=tests --cov-report=term-missing ${@}
