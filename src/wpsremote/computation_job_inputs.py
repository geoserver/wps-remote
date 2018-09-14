# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

from collections import OrderedDict

import computation_job_param
import computation_job_const
class ComputationJobInputs(object):
    """Encapsulate a set of input parameters"""

    @staticmethod
    def create_from_config(input_sections):
        '''Static constructor: 
        create a ComputationJobInputs object from a input_sections: a dictionary such as { input1 : [( 'par1_input1_name' , par1_input1_value ), ( 'par2_input1_name' , par2_input1_value ), ...], input2 : [ .... ], ... }
        '''
        input_sections_reshaped=OrderedDict()
        #force the order of sections in config files: [input1], [input2], etc
        for k in sorted(input_sections):
            d=dict(input_sections[k])
            name = d['name']
            del d['name']
            input_sections_reshaped[name] = d
        return ComputationJobInputs.create_from_dict( input_sections_reshaped )

    @staticmethod
    def create_from_dict(paremeters_types_defs):
        '''Static constructor: 
        create a ComputationJobInputs object from paremeters_types_defs: {par1_name : { 'par1_attrubute1_name' : par1_attrubute1_value, ... }, par2_name : { 'par2_attrubute1_name' : par2_attrubute1_value, ... }, ... }
        '''
        cji = ComputationJobInputs()
        input_to_add = None
        for name, d in OrderedDict(paremeters_types_defs).items():
            if ('class' in d):
                if d['class'] == 'param':
                    title = d['title'] if "title" in d else None
                    default = d['default'] if "default" in d else None
                    formatter = d['formatter'] if "formatter" in d else None
                    mininum = int(d['min']) if "min" in d else 1
                    maximum = int(d['max']) if "max" in d else 1
                    input_mime_type = d['input_mime_type'] if "input_mime_type" in d else None
                    input_to_add = computation_job_param.ComputationJobParam(name, d['type'], title, d['description'], default, formatter, mininum, maximum, input_mime_type)
                elif d['class'] == 'const':
                    title = d['title'] if "title" in d else None
                    input_to_add = computation_job_const.ComputationJobConst(name, d['type'], title, d['description'], d['value'])
                else:
                    raise TypeError("Unknown class value "+ str(d['class']) + " for input " + str(name))
            else:
                raise TypeError("Cannot create computational job input without attribute class")
            cji.add_input( input_to_add )

        return cji

    def __init__(self):
        self._inputs = OrderedDict()

    def parse(self):
        pass

    def validate(self):
        pass

    def add_input(self, inputs):
        if (type(inputs) is list):
            self._inputs.update (dict( (v.get_name(), v) for v in inputs) )
        else:
            v=inputs
            self._inputs[ v.get_name() ] = v

    def set_values(self, values):
        for name, val in values.items():
            if name in self._inputs:
                self._inputs[name].set_value( val )

    def values(self):
        for v in self._inputs.itervalues():
            yield v

    def names(self):
        for k in self._inputs.iterkeys():
            yield k

    def __getitem__(self, k):
        return self._inputs[k] 

    def as_DLR_protocol(self):
        #[('result', '{"type": "string", ...ut.xml" }')]
        res = []
        for k in self._inputs.keys():
            if type(self._inputs[k]) is computation_job_const.ComputationJobConst:
                continue
            n = self._inputs[k].get_name()
            j = self._inputs[k].as_json_string()
            res.append( (n,j) )
        return res
