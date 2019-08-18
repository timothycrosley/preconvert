#!/bin/bash

./lint.sh
pytest --cov=preconvert --cov=tests --cov-report=term-missing ${@}
