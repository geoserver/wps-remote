# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import json
import path

import computational_job_input_action

class ComputationalJobInputActionUpdateJSONFile(computational_job_input_action.ComputationalJobInputAction):


    def __init__(self, input_ref, target_json_file, json_path_expr, source_template_json_file):
        super(ComputationalJobInputActionUpdateJSONFile, self).__init__()
        #if not type(input_refs) is list:
        #    self._input_refs = [input_refs]
        #else:
        self._input_ref = input_ref
        #file path that will be updated
        #self._target_json_file = target_json_file
        self._target_json_file = target_json_file if isinstance(target_json_file, path.path) else path.path(target_json_file)
        # Python-like expression to reference the attribute in the json file to be set
        self.jsonpath_expr = json_path_expr
        # If target file doesn't exists it will be created using the template at this file path
        self._config_file_template = source_template_json_file if isinstance(source_template_json_file, path.path) else path.path(source_template_json_file)
        

    def set_inputs(self, inputs):
        if self._input_ref in inputs.names():
            if not self.exists() and self._config_file_template!= None:
                self._config_file_template.copyfile( self._target_json_file )
                self.update_file(inputs)
            elif not self.exists() and self._config_file_template== None:
                raise Exception("Cannot find target JSON file " + str(self._target_json_file) )
            else:
                self.update_file(inputs)

    def update_file(self, inputs):
        json_text = self._target_json_file.text()
        j=json.loads(json_text)
        exec( "j" + self.jsonpath_expr + "=" + str(  inputs[self._input_ref].get_value_as_JSON_literal() ) )
        json.dump( j, self._target_json_file.open('w'), indent=4 )

    def exists(self):
        return self._target_json_file.exists()

