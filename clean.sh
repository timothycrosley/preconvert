#!/bin/bash -xe

pipenv run isort --recursive preconvert/ tests/
pipenv run black preconvert/ tests/ -l 100
