# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

from collections import OrderedDict
import path
import introspection
import ConfigParser

def action_factory(config_section_items):
    actions = OrderedDict()
    for a in config_section_items:
        d = dict(config_section_items[a])
        if ('type' in d):
            actions[a] = introspection.get_class_one_arg( d['type'], d )

    return actions

class CopyFile(object):
    def __init__(self, param_dict):
        self.source = path.path(param_dict['source'])
        self.target = path.path(param_dict['target'])

    def execute(self, input_values):
         self.source.copy(self.target)


class CopyINIFileAddParam(object):
    def __init__(self, param_dict):
        self.source = path.path(param_dict['source'])
        self.target = path.path(param_dict['target'])
        self.param_section = param_dict['param_section']
        self.param_name = param_dict['param_name']
        self.param_value_ref = param_dict['param_value_ref']

    def execute(self, input_values):
        self.source.copy(self.target)
        config = ConfigParser.ConfigParser(allow_no_value=True)
        fp = self.target.open() 
        config.readfp( fp  )
        fp.close()

        config.set(self.param_section, self.param_name, input_values[self.param_value_ref])
       
        with self.target.open('wb') as configfile:
            config.write(configfile)