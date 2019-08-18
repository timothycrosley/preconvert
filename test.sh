#!/bin/bash

./lint.sh
pipenv run pytest --cov=preconvert --cov=tests --cov-report=term-missing ${@}
