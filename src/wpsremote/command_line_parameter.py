# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import input_parameter

class CommandLineParameter(input_parameter.InputParameter):
    def __init__(self, name):
        input_parameter.InputParameter.__init__(self, name)
        self._template=None

    def get_cmd_line(self):
        cmd=''
        hasName = False
        hasValue = False
        if 'name' in self._template:
            self._template = self._template.replace("name", "%s")
            hasName = True
        if 'value' in self._template:
            self._template = self._template.replace("value","%s")  
            hasValue = True
        for v in self._value:
            if (hasName and hasValue):
                cmd += self._template % (self.get_name(), v) + " "
            elif hasName:
                cmd += self._template % (self.get_name()) + " "
            elif hasValue:
                cmd += self._template % (v) + " "
            else:
                raise Exception("Bad template for command line parameter " + self.get_name())
        return cmd 

class CommandLineParameterConst(CommandLineParameter):
    def __init__(self, name):
        CommandLineParameter.__init__(self, name)
        self._template=None

    def inject_values(self, paremeters_types_defs):
        super(CommandLineParameterConst, self).inject_values(paremeters_types_defs)
        if type(self._value) is not list:
            self._value = [self._value]

    def set_actual_value(self, value):
        """override this function because in this case the param value is set in the constructor not with this function"""
        pass
