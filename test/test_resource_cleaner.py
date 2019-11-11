# (c) 2019 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import unittest
import random
import os
from wpsremote.path import path
from wpsremote.resource_cleaner import Resource

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2019 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"


class TestResourceCleaner(unittest.TestCase):

    def test_instance_methods(self):
        rc = Resource()
        self.assertIsNone(rc.start_time())
        self.assertIsNone(rc.cmd_line())
        self.assertIsNone(rc.unique_id())
        self.assertIsNone(rc.set_unique_id(1))
        self.assertIsNone(rc.sendbox_path())
        self.assertIsNone(rc.processbot_pid())
        self.assertIsNone(rc.set_processbot_pid(1))
        self.assertIsNone(rc.spawned_process_pids())
        self.assertIsNone(rc.spawned_process_cmd())
        sandbox_root = path("./src/wpsremote/xmpp_data/test/test_dir")
        unique_id = str(random.randint(1, 1000)).zfill(5)
        sendbox_path = sandbox_root / str(unique_id)
        rc.set_from_servicebot(unique_id, sendbox_path)
        self.assertEqual(rc.sendbox_path(), sendbox_path)
        self.assertEqual(rc._unique_id, unique_id)
        rc.set_from_processbot(os.getpid(), [unique_id])
        self.assertIn(unique_id, rc._spawned_process_pids)
        try:
            rc.read()
        except Exception as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main()
