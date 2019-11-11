# (c) 2019 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import unittest
import wpsremote.ConfigParser as ConfigParser
from wpsremote.ConfigParser import DuplicateSectionError
import wpsremote.config_instance as config_instance
import wpsremote.path as path

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2019 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"


class TestConfigParser(unittest.TestCase):

    DEFAULT_ITEMS = [
        ('service', 'Service'), ('namespace', 'default'), ('description', 'foo service'),
        ('executable_path', '\\code\\etl'), ('executable_cmd', 'python %(executable_path)s\\etl.py'),
        ('output_dir', 'src\\wpsremote\\xmpp_data\\test\\tmp'), ('unique_execution_id', '123'),
        ('workdir', '%(output_dir)s\\%(unique_execution_id)s'), ('active', 'True'),
        ('max_running_time_seconds', '10'), ('servicepassword', 'admin'),
        ('process_weight', '{"weight": "10", "coefficient": "1.5"}')
    ]
    CONFIG_SECTIONS = [
        'Input1', 'Action1', 'Input2', 'Action2', 'Input3', 'Action3', 'Input4', 'Action4', 'Const1', 'Action5',
        'Const2', 'Action6', 'Action7', 'Action8', 'Action9', 'Const3', 'Action10', 'Output', 'Logging'
    ]

    def test_create_config_parser(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        self.assertIsNotNone(cp)
        self.assertIsInstance(cp, ConfigParser.ConfigParser)

    def test_sections(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        sections = cp.sections()
        self.assertIsNotNone(sections)
        for s in sections:
            self.assertIn(s, TestConfigParser.CONFIG_SECTIONS)

    def test_defaults(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        default_section = cp.defaults()
        self.assertIsNotNone(default_section)
        self.assertIsNotNone(default_section.items())
        for d in default_section.items():
            self.assertIn(d, TestConfigParser.DEFAULT_ITEMS)

    def test_add_section(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        self.assertRaises(DuplicateSectionError, lambda: cp.add_section("Input1"))
        self.assertNotIn("Input5", cp.sections())
        cp.add_section("Input5")
        self.assertIn("Input5", cp.sections())

    def test_has_section(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        self.assertTrue(cp.has_section("Input1"))

    def test_options(self):
        options = [
            'class', 'input_ref', 'alias', 'template', 'service', 'namespace', 'description',
            'executable_path', 'executable_cmd', 'output_dir', 'unique_execution_id', 'workdir',
            'active', 'max_running_time_seconds', 'servicepassword', 'process_weight'
        ]
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        opts = cp.options("Action1")
        for o in opts:
            self.assertIn(o, options)

    def test_read(self):
        filenames = ["./src/wpsremote/xmpp_data/test/service.config"]
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        fn = cp.read("./src/wpsremote/xmpp_data/test/service.config")
        self.assertEqual(fn, filenames)

    def test_readfp(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        fp = open("./src/wpsremote/xmpp_data/test/service.config")
        cp.readfp(fp)
        fp.close()
        default_section = cp.defaults()
        for d in default_section.items():
            if d == ('servicePassword', 'admin'):
                self.assertNotIn(d, TestConfigParser.DEFAULT_ITEMS)

    def test_get(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        self.assertEqual("admin", cp.get("DEFAULT", "servicePassword"))

    def test_items(self):
        items_list = [
            ('service', 'Service'), ('namespace', 'default'), ('description', 'foo service'),
            ('executable_path', '\\code\\etl'), ('executable_cmd', 'python \\code\\etl\\etl.py'),
            ('output_dir', 'src\\wpsremote\\xmpp_data\\test\\tmp'), ('unique_execution_id', '123'),
            ('workdir', 'src\\wpsremote\\xmpp_data\\test\\tmp\\123'), ('active', 'True'),
            ('max_running_time_seconds', '10'), ('servicepassword', 'admin'), ('class', 'updateJSONfile'),
            ('input_ref', 'timeHorizon'),
            ('source_filepath', '.\\configs\\OAAonDemand\\CMREOAA_MainConfigFile_template.json'),
            ('target_filepath', 'src\\wpsremote\\xmpp_data\\test\\tmp\\123\\config.json'),
            ('json_path_expr', "['Config']['timeHorizon']"),
            ('process_weight', '{"weight": "10", "coefficient": "1.5"}')
        ]
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        for i in cp.items("Action3"):
            self.assertIn(i, items_list)

    def test_getboolean(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        self.assertIs(True, cp.getboolean("DEFAULT", "active"))

    def test_has_option(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        self.assertTrue(cp.has_option("DEFAULT", "active"))

    def test_set(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        self.assertTrue(cp.getboolean("DEFAULT", "active"))
        cp.set("DEFAULT", "active", "False")
        self.assertFalse(cp.getboolean("DEFAULT", "active"))

    def test_remove_option(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        self.assertTrue(cp.has_option("Action1", "input_ref"))
        cp.remove_option("Action1", "input_ref")
        self.assertFalse(cp.has_option("Action1", "input_ref"))

    def test_remove_section(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        self.assertTrue(cp.has_section("Action1"))
        cp.remove_section("Action1")
        self.assertFalse(cp.has_section("Action1"))

    def test_items_without_defaults(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        for section in TestConfigParser.CONFIG_SECTIONS:
            items = config_instance.items_without_defaults(cp, section, raw=False)
            for i in items:
                self.assertNotIn(i, TestConfigParser.DEFAULT_ITEMS)

    def test_get_list_impl(self):
        list_items = ['item_0', 'item_1', 'item_2']
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        items = config_instance.get_list_impl(cp, "Input1", "list")
        for i in items:
            self.assertIn(i, list_items)

    def test_get_list_list_impl(self):
        list_list = [['item_0'], ['item_1'], ['item_2']]
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        items = config_instance.get_list_list_impl(cp, "Input1", "list")
        for i in items:
            self.assertIsInstance(i, list)
            self.assertIn(i, list_list)

    def test_get_list_int_impl(self):
        int_list = [0, 1, 2, 3]
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        items = config_instance.get_list_int_impl(cp, "Input1", "int_list")
        for i in items:
            self.assertIsInstance(i, int)
            self.assertIn(i, int_list)

    def test_get_list_float_impl(self):
        float_list = [0.12, 1.6, 2.55, 3.4]
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        items = config_instance.get_list_float_impl(cp, "Input1", "float_list")
        for i in items:
            self.assertIsInstance(i, float)
            self.assertIn(i, float_list)

    def test_get_list_path_impl(self):
        path_list = ['src\\wpsremote\\xmpp_data\\test\\tmp\\123', 'src\\wpsremote\\xmpp_data\\test\\tmp']
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        items = config_instance.get_list_path_impl(cp, "Input1", "path_list")
        for i in items:
            self.assertIsInstance(i, path.path)
            self.assertIn(i, path_list)

    def test_get_password(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        psw = config_instance.get_password(cp, "DEFAULT", "servicePassword")
        self.assertEqual("admin", psw)

    def test_get_path(self):
        cp = config_instance.create("./src/wpsremote/xmpp_data/test/test_service.config")
        item = config_instance.get_path(cp, "DEFAULT", "output_dir")
        self.assertIsInstance(item, path.path)
        self.assertEqual("src\\wpsremote\\xmpp_data\\test\\tmp", item)


if __name__ == '__main__':
    unittest.main()
