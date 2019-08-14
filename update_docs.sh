#!/bin/bash
mkdir -p docs/__auto__
pdoc3 preconvert > docs/__auto__/preconvert.md
pdoc3 preconvert.convert > docs/__auto__/preconvert.convert.md
pdoc3 preconvert.converters > docs/__auto__/preconvert.preconvert.converters.md
pdoc3 preconvert.exceptions > docs/__auto__/preconvert.exceptions.md
pdoc3 preconvert.register > docs/__auto__/preconvert.register.md
pdoc3 preconvert.output > docs/__auto__/preconvert.output.md
mkdocs gh-deploy
