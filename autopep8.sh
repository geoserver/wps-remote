#!/bin/bash
set -e

autopep8 -v -i -a -a -r *.py
autopep8 -v -i -a -a -r src
autopep8 -v -i -a -a -r test
