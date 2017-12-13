#!/bin/bash

python3.6 -m pytest -l -rfEsxp -s --maxfail=1 $@
