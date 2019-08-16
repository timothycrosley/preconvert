#!/bin/bash
pdoc3 -o docs preconvert --template-dir templates --force -c show_type_annotations=True
mkdocs gh-deploy
