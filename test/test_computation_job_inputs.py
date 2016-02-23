# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import wpsremote

import unittest
import json
import ConfigParser

from wpsremote import path
from wpsremote import computation_job_param
from wpsremote import computation_job_inputs
from wpsremote import computational_job_input_actions
from wpsremote import computational_job_input_action_cmd_param
from wpsremote import computational_job_input_action_create_json_file
from wpsremote import computational_job_input_action_update_json_file
from wpsremote import mockutils

class TestComputationJobInputs(unittest.TestCase):

    def test_set_int_param(self):
        p1 = computation_job_param.ComputationJobParam("mypar", "int", "par title", "par descr")
        p1.set_value("1")
        self.assertEquals( p1.get_value_string(), "1" )

                   
    def test_set_int_param_wrong_value(self):
        p1 = computation_job_param.ComputationJobParam("mypar", "int", "par title", "par descr")
        #self.assertRaises( TypeError, p1.set_value("zxc") )
        try:
            p1.set_value("all your base are belong to us")
            self.fail()
        except TypeError:
            self.assertTrue(True)

    def test_set_multiple_int_param(self):
        p1 = computation_job_param.ComputationJobParam("mypar", "int", "par title", "par descr", max_occurencies=2)
        p1.set_value(["1","2"])
        self.assertEquals( p1.get_value_string(), ["1","2"] )

    def test_set_multiple_int_param_wrong_occurrencies(self):
        p1 = computation_job_param.ComputationJobParam("mypar", "int", "par title", "par descr", max_occurencies=1)
        try:
            p1.set_value(["1","2"])
            self.fail()
        except TypeError:
            self.assertTrue(True)


    def test_two_params(self):
        p1 = computation_job_param.ComputationJobParam("mypar1", "int", "par 1", "par descr 1")
        p2 = computation_job_param.ComputationJobParam("mypar2", "string", "par 2", "par descr 2")
        inputs = computation_job_inputs.ComputationJobInputs()
        inputs.add_input( [p1, p2] )
        inputs.set_values( { "mypar1" : "1", "mypar2" : "abc"} )
        self.assertEquals( p1.get_value_string(), "1" )
        self.assertEquals( p2.get_value_string(), "abc" )


    def test_cmd_line_action(self):
        inputs = computation_job_inputs.ComputationJobInputs()
        inputs.add_input(  computation_job_param.ComputationJobParam("mypar1", "int", "par 1", "par descr 1") )

        actions = computational_job_input_actions.ComputationalJobInputActions()
        actions.add_actions( computational_job_input_action_cmd_param.ComputationalJobInputActionCmdParam("mypar1", "--name=value") )

        inputs.set_values( { "mypar1" : "1" } )
        actions.execute( inputs )

        self.assertEquals(actions.get_cmd_line(), "--mypar1=1")


    def test_cmd_line_action_2_values(self):
        p1 = computation_job_param.ComputationJobParam("mypar1", "int", "par 1", "par descr 1")
        p2 = computation_job_param.ComputationJobParam("mypar2", "string", "par 2", "par descr 2")
        inputs = computation_job_inputs.ComputationJobInputs()
        inputs.add_input( [p1, p2] )
        
        actions = computational_job_input_actions.ComputationalJobInputActions()
        actions.add_actions( computational_job_input_action_cmd_param.ComputationalJobInputActionCmdParam("mypar1", "--name=value") )
        actions.add_actions( computational_job_input_action_cmd_param.ComputationalJobInputActionCmdParam("mypar2", "--name=value") )


        inputs.set_values( { "mypar1" : "1", "mypar2" : "abc"} )
        actions.execute( inputs )

        self.assertEquals(actions.get_cmd_line(), "--mypar1=1 --mypar2=abc")

    def test_create_json_file_action(self):
        p1 = computation_job_param.ComputationJobParam("mypar1", "application/json", "par 1", "par descr 1")
        inputs = computation_job_inputs.ComputationJobInputs()
        inputs.add_input( p1 )

        actions = computational_job_input_actions.ComputationalJobInputActions()
        a1 = computational_job_input_action_create_json_file.ComputationalJobInputActionCreateJSONFile("mypar1", path.path("./json_out_${json_path_expr}.json"), "['Asset']['id']", path.path("./src/wpsremote/xmpp_data/test/asset_schema.json")) 
        actions.add_actions( a1 )
        
        
        inputs.set_values( { "mypar1" : TestComputationJobInputs.json_text1 } )
        actions.execute( inputs )

        self.assertTrue( a1.exists() )

    def test_create_2_json_file_action(self):
        p1 = computation_job_param.ComputationJobParam("mypar1", "application/json", "par 1", "par descr 1",  max_occurencies=2)
        inputs = computation_job_inputs.ComputationJobInputs()
        inputs.add_input( p1 )

        actions = computational_job_input_actions.ComputationalJobInputActions()
        a1 = computational_job_input_action_create_json_file.ComputationalJobInputActionCreateJSONFile("mypar1", path.path("./json_out_${json_path_expr}.json"), "['Asset']['id']", path.path("./src/wpsremote/xmpp_data/test/asset_schema.json")) 
        actions.add_actions( a1 )
        
        
        inputs.set_values(  { "mypar1" : [TestComputationJobInputs.json_text1, TestComputationJobInputs.json_text2] } )
        actions.execute( inputs )

        self.assertTrue( a1.exists() )
        
    def test_update_json_file_action_with_int(self):
        target_json_file = path.path("./json_out.json")
        if target_json_file.exists():
            target_json_file.remove()
        source_template_json_file = path.path(r"./src/wpsremote/xmpp_data/test/CMREOAA_MainConfigFile_template.json")

        param1 = computation_job_param.ComputationJobParam("numberOfevaluations", "int", "par 1", "numberOfevaluations descr")
        inputs = computation_job_inputs.ComputationJobInputs()
        action1 = computational_job_input_action_update_json_file.ComputationalJobInputActionUpdateJSONFile("numberOfevaluations", target_json_file , "['Config']['nEvaluations']", source_template_json_file)

        inputs.add_input ( param1 )
        inputs.set_values( { "numberOfevaluations" : "100" } )
        action1.set_inputs( inputs )

        #check target_json_file
        json_text = target_json_file.text()
        j=json.loads(json_text)
        self.assertTrue( 100, j['Config']['nEvaluations'] )

    def test_update_json_file_action_with_string(self):
        target_json_file = path.path("./json_out.json")
        if target_json_file.exists():
            target_json_file.remove()
        source_template_json_file = path.path(r"./src/wpsremote/xmpp_data/test/CMREOAA_MainConfigFile_template.json")

        param1 = computation_job_param.ComputationJobParam("path_file_name", "string", "par 1", "path_file_name descr")
        inputs = computation_job_inputs.ComputationJobInputs()
        action1 = computational_job_input_action_update_json_file.ComputationalJobInputActionUpdateJSONFile("path_file_name", target_json_file , "['Config']['pathFilename']", source_template_json_file)

        inputs.add_input ( param1 )
        inputs.set_values( { "path_file_name" : "thisIsOK.txt" } )
        action1.set_inputs( inputs )

        #check target_json_file
        json_text = target_json_file.text()
        j=json.loads(json_text)
        self.assertTrue( "thisIsOK.txt", j['Config']['pathFilename'] )

    def test_read_param_from_ini(self):
        ini_text = '''[Input1]
        class = param
        name = mypar1
        type = int
        description = mypar descr
        '''
        config = ConfigParser.ConfigParser()
        ini_file = mockutils.FileLikeObjectMock(ini_text)
        config.readfp( ini_file )
        input_section = config.items('Input1')
        inputs = computation_job_inputs.ComputationJobInputs.create_from_config({'Input1' : input_section })

        actions = computational_job_input_action_cmd_param.ComputationalJobInputActionCmdParam("mypar1", "--name=value")

        inputs.set_values( { "mypar1" : "1" } )
        actions.set_inputs( inputs )

        self.assertEquals(actions.get_cmd_line(), "--mypar1=1")
        

    def test_read_action_from_ini(self):
        ini_text = '''[Action1]
        input_ref = mypar1
        class = cmdline
        template = --name=value
        '''
        config = ConfigParser.ConfigParser()
        ini_file = mockutils.FileLikeObjectMock(ini_text)
        config.readfp( ini_file )
        input_section = config.items('Action1')
        
        inputs = computation_job_inputs.ComputationJobInputs()
        inputs.add_input (
            computation_job_param.ComputationJobParam("mypar1", "int", "par 1", "par descr")
        )

        actions = computational_job_input_actions.ComputationalJobInputActions.create_from_config( { 'Action1' : input_section })

        inputs.set_values( { "mypar1" : "1" } )
        actions.execute( inputs )

        self.assertEquals(actions.get_cmd_line(), "--mypar1=1")



    def test_2_cmdpar_from_ini(self):

        ini_text = '''[Input1]
class = param
name = workingdir
type = string
description = OAA process working directory
[Action1]
class = cmdline
input_ref = workingdir
alias = w
template = -name value
[Const1]
class = const
name = etlExecutionType
type = string
description = parameter to choose what type of execution is performed by etl.py script
value = oaaOnDemand
[Action2]
class = cmdline
input_ref = etlExecutionType
template = value'''

        config = ConfigParser.ConfigParser()
        import StringIO

        sio = StringIO.StringIO( ini_text )
        config.readfp( sio )

        inputs = computation_job_inputs.ComputationJobInputs.create_from_config({'Input1' : config.items('Input1'), 'Const1' : config.items('Const1') })
        actions = computational_job_input_actions.ComputationalJobInputActions.create_from_config( { 'Action1' : config.items('Action1'), 'Action2' : config.items('Action2') }) 


        inputs.set_values( {'workingdir' : '.' } )

        actions.execute( inputs )

        self.assertEquals(actions.get_cmd_line(), '-w . oaaOnDemand')

    def test_cmdpar_order(self):

        ini_text = '''[Input2]
class = param
name = coeff
type = float
description = this is a coeff
[Action2]
class = cmdline
input_ref = coeff
alias = k
template = --name=value

[Input1]
class = param
name = workingdir
type = string
description = process working directory
[Action1]
class = cmdline
input_ref = workingdir
alias = w
template = -name value
'''

        config = ConfigParser.ConfigParser()
        import StringIO

        sio = StringIO.StringIO( ini_text )
        config.readfp( sio )

        inputs = computation_job_inputs.ComputationJobInputs.create_from_config({'Input2' : config.items('Input2'), 'Input1' : config.items('Input1') })
        actions = computational_job_input_actions.ComputationalJobInputActions.create_from_config( { 'Action2' : config.items('Action2'), 'Action1' : config.items('Action1') }) 


        inputs.set_values( {'workingdir' : '.', 'coeff' : 2.4 } )

        actions.execute( inputs )

        self.assertEquals(actions.get_cmd_line(), '-w . --k=2.4')

    def test_update_json_list_in_file(self):
        target_json_file = path.path("./json_out.json")
        if target_json_file.exists():
            target_json_file.remove()
        source_template_json_file = path.path(r"./src/wpsremote/xmpp_data/test/CMREOAA_MainConfigFile_template.json")

        param1 = computation_job_param.ComputationJobParam("maxlat", "float", "par title", "max latitude")
        inputs = computation_job_inputs.ComputationJobInputs()
        action1 = computational_job_input_action_update_json_file.ComputationalJobInputActionUpdateJSONFile("maxlat", target_json_file , "['Config']['latLim'][1]", source_template_json_file)

        inputs.add_input ( param1 )
        inputs.set_values( { "maxlat" : "45.5" } )
        action1.set_inputs( inputs )

        #check target_json_file
        json_text = target_json_file.text()
        j=json.loads(json_text)
        self.assertTrue( 45.5, j['Config']['latLim'][1] )

    def test_update_json_list_in_file_two_times(self):
        target_json_file = path.path("./json_out.json")
        if target_json_file.exists():
            target_json_file.remove()
        source_template_json_file = path.path(r"./src/wpsremote/xmpp_data/test/CMREOAA_MainConfigFile_template.json")

        param1 = computation_job_param.ComputationJobParam("minlat", "float", "par title", "min latitude")
        param2 = computation_job_param.ComputationJobParam("maxlat", "float", "par title", "max latitude")
        
        inputs = computation_job_inputs.ComputationJobInputs()
        
        action1 = computational_job_input_action_update_json_file.ComputationalJobInputActionUpdateJSONFile("minlat", target_json_file , "['Config']['latLim'][0]", source_template_json_file)
        #action2 = computational_job_input_action_update_json_file.ComputationalJobInputActionUpdateJSONFile("maxlat", target_json_file , "['Config']['latLim'][1]", source_template_json_file)

        inputs.add_input ( param1 )
        inputs.add_input ( param2 )

        inputs.set_values( { "minlat" : "75.5", "maxlat" : "76.5" } )
        action1.set_inputs( inputs )

        #check target_json_file
        json_text = target_json_file.text()
        j=json.loads(json_text)
        self.assertTrue( 75.5, j['Config']['latLim'][0] )
        self.assertTrue( 76.5, j['Config']['latLim'][1] )


    json_text1 = '''{
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
    }'''

    json_text2 = '''{
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
            "id": 2, 
            "Pd": 0.6, 
            "name": "Ship 2"
        }
    }'''
if __name__ == '__main__':
    unittest.main()