#!/bin/bash

isort --recursive preconvert/
black preconvert/ -l 100
