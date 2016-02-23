# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import json
import string

import path

import input_parameters
import input_parameter


class ConfigFileParameter(input_parameter.InputParameter):
    def __init__(self, name): 
        input_parameter.InputParameter.__init__(self, name)
        self._filepath=None

    def inject_values(self, paremeters_types_defs):
        super(ConfigFileParameter, self).inject_values(paremeters_types_defs)
        self._filepath = path.path(self._filepath)

    def get_cmd_line(self):
        self.update_file()
        return ' '

    #todo: rename to write file
    def update_file(self):
        pass
