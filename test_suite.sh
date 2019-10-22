#!/bin/bash
set -e

echo "Running... test_computation_job_inputs"
coverage run --source=src test/test_computation_job_inputs.py

echo "Running... test_process_input_parameters"
coverage run --source=src test/test_process_input_parameters.py

