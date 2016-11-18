# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import unittest
import output_file_parameter
import path
from collections import OrderedDict
import logging

class OutputParameters(object):

    @staticmethod
    def create_from_config(output_sections, wps_execution_shared_dir=None, uploader=None):
        '''Static constructor.
        input_sections: a dictionary such as { par1_name : [( 'par1_attrubute1_name' : par1_attrubute1_value ), ( 'par2_attrubute1_name' : par2_attrubute1_value ), ...], par2_name : { ... }, ... }
        '''
        output_sections_reshaped={}
        #force the order of sections in config files: [output1], [output2], etc
        for k in sorted(output_sections):
            d=dict(output_sections[k])
            name = d['name']
            del d['name']
            output_sections_reshaped[name] = d
        return OutputParameters( output_sections_reshaped, wps_execution_shared_dir, uploader )

    def __init__(self, parameters_types_defs, wps_execution_shared_dir, uploader):
        '''
        Static constructor.
        parameters_types: ('out_par_name1', {"out_par_name1_attrib1": "value1", "out_par_name1_attrib1": "value2", ...})
        '''
        self._wps_execution_shared_dir=wps_execution_shared_dir;
        self._params={}

        for name, d in OrderedDict(parameters_types_defs).items():
            if ('type' in d):

                if ('string' == d['type']):
                    self._params[name] = output_file_parameter.OutputFileParameter( name, d, wps_execution_shared_dir=self._wps_execution_shared_dir, uploader=uploader)

                elif ('image/geotiff' in d['type'] or 'text/xml' in d['type'] or 'application/gml' in d['type'] or 'application/zip' in d['type'] or 'application/x-netcdf' in d['type'] or 'video/mp4' in d['type']):
                    self._params[name] = output_file_parameter.RawFileParameter( name, d, wps_execution_shared_dir=self._wps_execution_shared_dir, uploader=uploader)

                elif ('application/owc' in d['type']):
                    self._params[name] = output_file_parameter.OWCFileParameter( name, d, parameters_types_defs, wps_execution_shared_dir=self._wps_execution_shared_dir, uploader=uploader)

                else:
                    logger = logging.getLogger("OutputParameters.__init__")
                    msg="Unknown output parameter " + name + " type"
                    logger.critical(msg)
                    raise Exception(msg)
            else:
                pass

    def get_values(self):
        res=[]
        for k in self._params:
            res.append(self._params[k].get_value())
        return res

    def parameters(self):
        for p in self._params.values():
            yield p

    def as_DLR_protocol(self):
        #[('result', '{"type": "string", ...ut.xml" }')]
        res = []
        for k in self._params.keys():
            n = self._params[k].get_name()
            j = self._params[k].as_json_string()
            res.append( (n,j) )
        return res

class Test(unittest.TestCase):
    
    def test_output_par_from_file(self):

        f=path.path("d:\\tmp\\test.txt")
        msg="this is a test"
        f.write_text(msg)
        
        p = OrderedDict( {"type": "string", "description": "xml OAA output file", "filepath" : "d:\\tmp\\test.txt"}   )
        par_types = [('result', p)]

        pop = OutputParameters(par_types)

        it = pop.parameters()
        val = next(it)
        self.assertEqual( val, msg)

        f.remove()

if __name__ == '__main__':
    unittest.main()
