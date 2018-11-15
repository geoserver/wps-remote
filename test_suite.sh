#!/bin/bash
set -e

echo "Running... test_computation_job_inputs"
python test/test_computation_job_inputs.py

echo "Running... test_process_input_parameters"
python test/test_process_input_parameters.py

