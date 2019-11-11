# (c) 2019 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import unittest
import os
from wpsremote.action import CopyFile, CopyINIFileAddParam
import wpsremote.config_instance as config_instance

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2019 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"


class TestAction(unittest.TestCase):

    def test_copy_file(self):
        copy_path = "./src/wpsremote/xmpp_data/test/test_dir/copy_of_test_file"
        param_dict = {
            "source": "./src/wpsremote/xmpp_data/test/test_dir/test_file",
            "target": copy_path
        }
        cf = CopyFile(param_dict)
        self.assertFalse(os.path.isfile(copy_path))
        cf.execute("blah")
        self.assertTrue(os.path.isfile(copy_path))
        os.remove(copy_path)

    def test_copy_INI_file_add_param(self):
        copy_path = "./src/wpsremote/xmpp_data/test/copy_of_test_service.config"
        param_dict = {
            "source": "./src/wpsremote/xmpp_data/test/test_service.config",
            "target": copy_path,
            "param_section": "Input3",
            "param_name": "another_param",
            "param_value_ref": "input3_another_param"
        }
        cifap = CopyINIFileAddParam(param_dict)
        input_values = {
            "input3_another_param": "Another value"
        }
        self.assertFalse(os.path.isfile(copy_path))
        cifap.execute(input_values)
        self.assertTrue(os.path.isfile(copy_path))
        config = config_instance.create(copy_path)
        self.assertEqual("Another value", config.get("Input3", "another_param"))
        os.remove(copy_path)


if __name__ == '__main__':
    unittest.main()
