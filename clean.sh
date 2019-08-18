#!/bin/bash

pipenv run isort --recursive preconvert/
pipenv run black preconvert/ -l 100
