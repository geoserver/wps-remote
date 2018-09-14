# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import introspection
from collections import OrderedDict

import command_line_parameter

class InputParameters(object):

        @staticmethod
        def create_from_config(input_sections):
            '''Create a InputParameters object.

            input_sections: a dictionary such as { input1 : [( 'par1_input1_name' , par1_input1_value ), ( 'par2_input1_name' , par2_input1_value ), ...], input2 : [ .... ], ... }
            '''
            input_sections_reshaped = OrderedDict()
            #force the order of sections in config files: [input1], [input2], etc
            for k in sorted(input_sections):
                d=dict(input_sections[k])
                name = d['name']
                del d['name']
                input_sections_reshaped[name] = d
            return InputParameters( input_sections_reshaped )

        def __init__(self, paremeters_types_defs):
            '''Create a input parameters set from a definitions

            paremeters_types_defs is a dictionary such as {par1_name : { 'par1_attrubute1_name' : par1_attrubute1_value, ... }, par2_name : { 'par2_attrubute1_name' : par2_attrubute1_value, ... }, ... }
            '''
            self._params = OrderedDict()

            for name, d in OrderedDict(paremeters_types_defs).items():
                if ('class' in d):
                    try:
                        self._params[name] = introspection.get_class_one_arg( d['class'], name )
                    except:
                        raise #log("Cannot create parameter object from class name "+d['class']+" for parameter " + name)
                else:
                    self._params[name] = command_line_parameter.CommandLineParameter(name)
                self._params[name].inject_values( d ) 

        def parse(self, input_variables=None):
            """if input_variables is None all params are of type CommandLineParameterConst and input data is read from config file"""
            for n,v in input_variables.items():
                if n in self._params.keys():
                    self._params[n].set_actual_value(v)
                else:
                    pass #todo: log "received unknown input parameter " + n 
            self.validate()

        def validate(self):
            for k in self._params.keys():
                self._params[k].validate()  

        def get_cmd_line(self):
            cmd_line=''
            for k in self._params.keys():
                c = self._params[k].get_cmd_line()
                if c <> None:
                    cmd_line +=  c 
            return cmd_line

        def as_DLR_protocol(self):
            #[('result', '{"type": "string", ...ut.xml" }')]
            res = []
            for k in self._params.keys():
                n = self._params[k].get_name_no_alias()
                j = self._params[k].as_json_string()
                res.append( (n,j) )
            return res
        
        def checkForCodeInsertion(self, argList):
            ''' Check user input for bad code insertion
            
                @param argList: user arguments
                @return: False if bad code found, else True
            '''
            # Check command line insertions
            maliciousCommands = ['>', '<', '>>', '|', '>&', '<&']
            # Check for bad code insertion
            maliciousCode = ['eval(', 'exec(', 'execfile(', 'input(']

            # Evaluate malicious commands
            if any(e in maliciousCommands for e in argList):
                raise IOError('Found bad code in user input')
            # Evaluate maliciousCode
            for element in argList:
                for code in maliciousCode:
                    if code in element:
                        raise IOError('Found bad code in user input')
