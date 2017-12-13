#!/bin/bash

python -m pytest -l -rfEsxp -s --maxfail=1 $@
