# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

"""todo: move this module out of  the project in cmre dedicated section"""
import json
import unittest
import datetime

import path

import config_file_parameter
import input_parameters

class CMREOAA_AssetConfigFile(config_file_parameter.ConfigFileParameter):

    shrot_name = "OAAAssetFile"

    def __init__(self, name):
        super(CMREOAA_AssetConfigFile, self).__init__(name)
        self._template_file_path = None

    def _get_file_path(self, id):
        return path.path(self._filepath.replace(self._template_file_path, str(id)))

    def update_file(self):
        asset_id=0
        for v in self._value:
            asset_json=json.loads(v)
            asset_id = int(asset_json['Asset']['id'])
            asset_file= self._get_file_path(asset_id)
            #asset_file.write_text( v )
            with asset_file.open('wb') as outfile:
                json.dump(asset_json, outfile, indent=4)



class CMREOAA_MainConfigFile(config_file_parameter.ConfigFileParameter):

    shrot_name = "OAAConfigFile"

    def __init__(self, name):
        super(CMREOAA_MainConfigFile, self).__init__(name)
        self._config_file_template = path.path('CMREOAA_MainConfigFile_template.json')

    def inject_values(self, paremeters_types_defs):
        super(CMREOAA_MainConfigFile, self).inject_values(paremeters_types_defs)
        if (self._filepath.exists()):
            self._filepath.remove()
      

    def update_file(self):
        #if target files exists open it and update, if doesnt exists load the template, modify it and save to target (it is useful for multiple update on the same file)        
        if (self._filepath.exists()):
            template = json.load(self._filepath.open())
        else:
            template = json.load(self._config_file_template.open())


        if (self.get_name() == 'timeHorizon'):
            template['Config']['timeHorizon'] = int(self._value[0])

        elif (self.get_name() == 'nEvaluations'):
            template['Config']['nEvaluations'] = int(self._value[0])
        else:
            pass #todo: log "Cannot write input pararmeter " + name + " in config file " + str( self._config_file_path )

        with self._filepath.open('wb') as outfile:
            json.dump(template, outfile, indent=4)




class Test(unittest.TestCase):

    def test_asset_config_object(self):

        a1=path.path("d:\\tmp\\asset_1.json")
        a2=path.path("d:\\tmp\\asset_2.json")

        if a1.exists():
            a1.remove()
        if a2.exists():
            a2.remove()

        paramsDef = [('assets' , {"type": "application/json",  "description": "Assets config", "max": 10, "filepath" : "d:\\tmp\\asset_$i.json", "template_file_path" : "$i", "class" : "config_file_parameter_cmre_oaa.CMREOAA_AssetConfigFile"} ) ]

        paramValue = {'assets': ['''{
            "Asset": {
                "Pfa": 0.001, 
                "maxSpeed": 10, 
                "minSpeed": 2, 
                "maxHeading": 2.1, 
                "minHeading": -2.1, 
                "lat0": 12.08, 
                "cost": 1e-06, 
                "obsRange": 50000, 
                "heading0": 0, 
                "lon0": 63.17, 
                "type": "Frigate", 
                "id": 1, 
                "Pd": 0.6, 
                "name": "Ship 1"
            }
        }''', '''{
            "Asset": {
                "Pfa": 0.001, 
                "maxSpeed": 10, 
                "minSpeed": 2, 
                "maxHeading": 2.1, 
                "minHeading": -2.1, 
                "lat0": 13.66, 
                "cost": 1e-06, 
                "obsRange": 50000, 
                "heading0": 0, 
                "lon0": 58.9, 
                "type": "Frigate", 
                "id": 2, 
                "Pd": 0.6, 
                "name": "Ship 2"
            }
        }'''], 
        'numberOfEvaluations': 600, 'timeHorizont': 259200}

        pip = input_parameters.InputParameters(paramsDef)
        pip.parse( paramValue )
        
        res = pip.get_cmd_line()

        self.assertEquals(res.strip(), "")

        self.assertTrue(a1.exists())
        self.assertTrue(a2.exists())

    def test_OAA_main_config_file(self):
        a1=path.path("d:\\tmp\\oaa_config.json")

        if a1.exists():
            a1.remove()


        paramsDef = [
            ('numberOfEvaluations',   {"type": "int", "description": "number of optimizer iterations", "max": 1,  "alias" : "nEvaluations", "class" : "config_file_parameter_cmre_oaa.CMREOAA_MainConfigFile", "filepath" : "d:\\tmp\\oaa_config.json" }), 
            ('referenceDate',         {"type": "datetime", "description": "start date of optimizer", "max": 1, "alias" : "refDate", "formatter" : "%Y%m%d", "class" : "config_file_parameter_cmre_oaa.CMREOAA_MainConfigFile", "filepath" : "d:\\tmp\\oaa_config.json" }), 
            ('timeHorizon',           {"type": "int", "description": "Time horizon in seconds of the optimizer", "max": 1, "class" : "config_file_parameter_cmre_oaa.CMREOAA_MainConfigFile", "filepath" : "d:\\tmp\\oaa_config.json" }),
            ('executiontType',        {"type": "string", "description": "etl execution type", "max": 1, "template" : "value"})
        ]

        paramValue = {'argx' : 'test' }
        paramValue = { 'numberOfEvaluations': 600, 'referenceDate' : '20140901', 'timeHorizon': 259200, 'executiontType' : 'oaaOnDemand' }

        pip = input_parameters.InputParameters(paramsDef)
        pip.parse( paramValue )
        
        res = pip.get_cmd_line()


        self.assertEquals(res.strip(), "--referencedate==20140901 oaaOnDemand" )

        self.assertTrue( a1.exists() )

        configs  = json.load( a1.open() )
        self.assertEqual(configs['Config']['nEvaluations'], 600)
        self.assertEqual(configs['Config']['refDate'], '2014-09-01T00:00:00Z')
        self.assertEqual(configs['Config']['timeHorizon'], 259200)


if __name__ == '__main__':
    unittest.main()