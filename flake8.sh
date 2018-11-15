#!/bin/bash
set -e

flake8 *.py
flake8 src/wpsremote
flake8 test
