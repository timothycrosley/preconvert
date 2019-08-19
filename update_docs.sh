#!/bin/bash

wget https://raw.githubusercontent.com/hugapi/HOPE/master/all/HOPE-8--Style-Guide-for-Hug-Code.md -O docs/CODING_STANDARD.md
wget https://raw.githubusercontent.com/hugapi/HOPE/master/all/HOPE-11-Code-of-Conduct.md -O docs/CODE_OF_CONDUCT.md
pipenv run pdoc3 -o docs preconvert --template-dir templates --force -c show_type_annotations=True
pipenv run mkdocs gh-deploy
