
:begin
echo off

pylint -r n --disable=C --disable=W0141 wpsagent.py
pylint -r n --disable=C --disable=W0141 servicebot.py
pylint -r n --disable=C --disable=W0141 computation_job_inputs.py 
pylint -r n --disable=C --disable=W0141 computation_job_input.py 
pylint -r n --disable=C --disable=W0141 output_parameters.py 
pylint -r n --disable=C --disable=W0141 output_file_parameter.py
pylint -r n --disable=C --disable=W0141 xmppBus.py
pylint -r n --disable=C --disable=W0141 bus.py
pylint -r n --disable=C --disable=W0141 computation_job_param.py 
pylint -r n --disable=C --disable=W0141 computation_job_const.py 
pylint -r n --disable=C --disable=W0141 resource_cleaner.py 
pylint -r n --disable=C --disable=W0141 computational_job_input_action.py
pylint -r n --disable=C --disable=W0141 computational_job_input_action_cmd_param.py
pylint -r n --disable=C --disable=W0141 computational_job_input_action_copyfile.py
pylint -r n --disable=C --disable=W0141 computational_job_input_action_create_json_file.py
pylint -r n --disable=C --disable=W0141 computational_job_input_action_update_ini_file.py
pylint -r n --disable=C --disable=W0141 computational_job_input_action_update_json_file.py
pylint -r n --disable=C --disable=W0141 computational_job_input_actions.py
pylint -r n --disable=C --disable=W0141 test_computation_job_inputs.py
pylint -r n --disable=C --disable=W0141 output_file_parameter.py


python test_computation_job_inputs.py
python test_process_input_parameters.py
python resource_cleaner.py

IF "%1"=="" GOTO exit

ping -n 6 127.0.0.1 > NUL

GOTO :begin 

:exit