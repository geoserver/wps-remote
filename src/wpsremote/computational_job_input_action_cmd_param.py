# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import copy
import computational_job_input_action

class ComputationalJobInputActionCmdParam(computational_job_input_action.ComputationalJobInputAction): #computational_job_input_action.ComputationalJobInputAction

    def __init__(self, input_ref, template="--name=value", alias=None):
        super(ComputationalJobInputActionCmdParam, self).__init__()
        #if not type(input_refs) is list:
        #    self._input_refs = [input_refs]
        #else:
        self._input_ref = input_ref
        self._template = template
        self._cmdline = ""
        self._alias = alias

    def set_inputs(self, inputs):
        #for varname in self._input_ref:
        if self._input_ref in inputs.names():
            self._cmdline += ' ' + self._instance_template( self._input_ref, inputs[self._input_ref].get_value_string() ) 
        self._cmdline = self._cmdline.strip()

    def _instance_template(self, name, value_str):
        cmd=''
        if self._alias!=None:
            name = self._alias
        hasName = False
        hasValue = False
        template = copy.deepcopy(self._template)
        if 'name' in template:
            template = template.replace("name", "%s")
            hasName = True
        if 'value' in self._template:
            template =template.replace("value","%s")  
            hasValue = True

        if (hasName and hasValue):
            cmd += template % (name, value_str) 
        elif hasName:
            cmd += template % (name)
        elif hasValue:
            cmd += template % (value_str)
        else:
            raise Exception("Bad template for command line parameter " + name)

        return cmd 

    def get_cmd_line(self):
        return self._cmdline

