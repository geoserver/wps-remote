# (c) 2019 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import unittest
import wpsremote.path as path

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2019 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"


class TestPath(unittest.TestCase):

    LIST_DIRS = [
        path.path('./src/wpsremote/xmpp_data/test/asset_schema.json'),
        path.path('./src/wpsremote/xmpp_data/test/test_dir'),
        path.path('./src/wpsremote/xmpp_data/test/wcsOAAonDemand_template.properties.txt'),
        path.path('./src/wpsremote/xmpp_data/test/service.config'),
        path.path('./src/wpsremote/xmpp_data/test/OAAonDemandWrapper_template.properties.txt'),
        path.path('./src/wpsremote/xmpp_data/test/test_file'),
        path.path('./src/wpsremote/xmpp_data/test/test_file_to_write'),
        path.path('./src/wpsremote/xmpp_data/test/test_service.config'),
        path.path('./src/wpsremote/xmpp_data/test/geoserverCommands_template.properties.txt'),
        path.path('./src/wpsremote/xmpp_data/test/oaaOnDemand_template.properties.txt'),
        path.path('./src/wpsremote/xmpp_data/test/test_remote.config'),
        path.path('./src/wpsremote/xmpp_data/test/CMREOAA_MainConfigFile_template.json'),
        path.path('./src/wpsremote/xmpp_data/test/logger_test.properties')
    ]
    DIRS = [path.path('./src/wpsremote/xmpp_data/test/test_dir')]

    def test_path_methods(self):
        p = path.path("test/path")
        self.assertEqual(p.__repr__(), "path('test/path')")
        self.assertEqual(p.__add__("/add"), "test/path/add")
        self.assertEqual(p.__radd__("radd/"), "radd/test/path")
        self.assertEqual(p.__div__("rel"), "test/path/rel")
        self.assertEqual(p.__truediv__("rel"), "test/path/rel")
        self.assertFalse(p.isabs())
        self.assertEqual(p.basename(), "path")
        self.assertEqual(p.name, "path")
        self.assertEqual(p.normcase(), "test/path")
        self.assertEqual(p.normpath(), "test/path")
        self.assertEqual(p.expanduser(), "test/path")
        self.assertEqual(p.expandvars(), "test/path")
        self.assertEqual(p.dirname(), "test")
        self.assertEqual(p.parent, "test")
        self.assertEqual(p.expand(), "test/path")
        self.assertEqual(p._get_namebase(), "path")
        self.assertEqual(p.namebase, "path")
        self.assertEqual(p._get_ext(), "")
        self.assertEqual(p.ext, "")
        self.assertEqual(p._get_drive(), "")
        self.assertEqual(p.drive, "")
        self.assertEqual(p.splitpath(), (path.path('test'), 'path'))
        self.assertEqual(p.splitdrive(), (path.path(''), path.path('test/path')))
        self.assertEqual(p.splitext(), (path.path('test/path'), ''))
        self.assertEqual(p.stripext(), "test/path")
        self.assertEqual(p.joinpath("join", "path"), "test/path/join/path")
        self.assertEqual(p.splitall(), [path.path(''), 'test', 'path'])
        self.assertEqual(p.relpath(), "test/path")
        self.assertEqual(p.relpathto("dest"), "../../dest")
        with self.assertRaises(OSError):
            p.listdir(pattern=None)
        existing_path = path.path("./src/wpsremote/xmpp_data/test")
        self.assertEqual(len(existing_path.listdir(pattern=None)), 12)
        for d in existing_path.listdir(pattern=None):
            self.assertIn(d, TestPath.LIST_DIRS)
        self.assertEqual(len(existing_path.dirs(pattern=None)), 1)
        for d in existing_path.dirs(pattern=None):
            self.assertIn(d, TestPath.DIRS)
        self.assertEqual(len(existing_path.files()), 11)
        for f in existing_path.files():
            self.assertIn(f, TestPath.LIST_DIRS)
        self.assertTrue(existing_path.fnmatch("*test*"))
        self.assertEqual(
            existing_path.glob("*test_dir*"),
            [path.path('./src/wpsremote/xmpp_data/test/test_dir')]
        )
        existing_file = path.path("./src/wpsremote/xmpp_data/test/test_file")
        self.assertIsInstance(existing_file.open(), file)
        self.assertEqual(existing_file.bytes(), "test content")
        existing_file.write_bytes("test file to write")
        self.assertEqual(existing_file.bytes(), "test file to write")
        self.assertEqual(existing_file.text(), "test file to write")
        existing_file.write_text("test content")
        self.assertEqual(existing_file.text(), "test content")
        existing_file.write_lines(["line 1", "line 2"])
        self.assertEqual(
            existing_file.lines(), [
                "line 1\n",
                "line 2\n"
            ]
        )
        existing_file.write_text("test content")
        # Methods for querying the filesystem
        self.assertTrue(existing_file.exists())
        self.assertFalse(path.path("./not/existing/path/test_file").exists())
        self.assertTrue(existing_path.isdir())
        self.assertTrue(existing_file.isfile())
        self.assertTrue(path.path("/").ismount())
        # mkdir
        new_dir = path.path('./src/wpsremote/xmpp_data/test/new_dir')
        new_dir.mkdir()
        self.assertTrue(new_dir.exists())
        new_dirs = path.path('./src/wpsremote/xmpp_data/test/new_dirs/new_dir')
        new_dirs.makedirs()
        self.assertTrue(new_dirs.exists())
        # rmdir
        new_dir.rmdir()
        self.assertFalse(new_dir.exists())
        new_dirs.removedirs()
        self.assertFalse(new_dirs.exists())
        # touch
        touch_file = path.path('./src/wpsremote/xmpp_data/test/new_file')
        self.assertFalse(touch_file.exists())
        touch_file.touch()
        self.assertTrue(touch_file.exists())
        # remove
        touch_file.remove()
        self.assertFalse(touch_file.exists())
        # unlink
        touch_file.touch()
        self.assertTrue(touch_file.exists())
        touch_file.unlink()
        self.assertFalse(touch_file.exists())
        # copyfile
        existing_file.copy('./src/wpsremote/xmpp_data/test/copy_of_test_file')
        copied_file = path.path('./src/wpsremote/xmpp_data/test/copy_of_test_file')
        self.assertTrue(copied_file.exists())
        copied_file.remove()


if __name__ == '__main__':
    unittest.main()
