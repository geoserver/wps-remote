# (c) 2019 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import os
import json
import mock
import pickle
import psutil
import datetime
import unittest
from argparse import Namespace
from wpsremote import introspection
from wpsremote.processbot import ProcessBot
from wpsremote.servicebot import ServiceBot
from wpsremote.resource_cleaner import Resource
import wpsremote.resource_monitor as resource_monitor
import wpsremote.config_instance as config_instance
from wpsremote.xmppBus import XMPPBus
from wpsremote.computation_job_inputs import ComputationJobInputs
from wpsremote.computational_job_input_actions import ComputationalJobInputActions
from wpsremote.output_parameters import OutputParameters
from wpsremote.path import path
from wpsremote.mockutils import (
    MockWPSAgentService, MockWPSAgentProcess, mock_clean_up_all, MockResourceMonitor
)

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2019 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

# due to xmppMessages chdir
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestBot(unittest.TestCase):

    def setUp(self):
        os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        self.remote_config = config_instance.create(
            "./src/wpsremote/xmpp_data/test/test_remote.config"
        )
        self.xmpp_bus = XMPPBus(self.remote_config, "service_name", "service_name_namespace")
        self.xep_0045_plugin = self.xmpp_bus.xmpp.plugin["xep_0045"]
        self.from_obj_mock = mock.Mock()
        self.from_obj_mock.__class__ = mock.Mock
        rooms = {
            self.xmpp_bus._get_MUC_JId(): {
                "resource": {
                    "role": "not_visitor"
                }
            }
        }
        self.xep_0045_plugin.rooms = rooms
        self.from_obj_mock.resource = "resource"
        test_msg = pickle.dumps({
            "test_message": "test message"
        })
        msg = {
            "type": "normal",
            "body": "topic=request&id=123&baseURL=test_base_url&message={}".format(test_msg),
            "from": self.from_obj_mock
        }
        # ExecuteMessage
        self.execute_message = self.xmpp_bus.CreateIndipendentMessage(msg)
        # cleaner
        Resource.clean_up_all = staticmethod(mock_clean_up_all)
        self.cleaner = Resource()
        # monitor
        resource_monitor.ResourceMonitor = MockResourceMonitor
        # wps agent args
        self.params_file = "./src/wpsremote/xmpp_data/test/test_params.p"
        pickle.dump(
            self.execute_message,
            open(self.params_file, "wb")
        )
        self.args = Namespace(
            executionid=None,
            logconf='./src/wpsremote/xmpp_data/test/logger_test.properties',
            params=self.params_file,
            remoteconfig='./src/wpsremote/xmpp_data/test/test_remote.config',
            runtype='service',
            serviceconfig='./src/wpsremote/xmpp_data/test/test_service.config'
        )

    def test_process_bot(self):
        wps_agent = MockWPSAgentProcess(self.args)
        # test bot
        process_bot = wps_agent.create_bot()
        self.assertIsInstance(process_bot, ProcessBot)
        self.assertTrue(process_bot._active)
        self.assertFalse(process_bot._finished)
        self.assertIsInstance(process_bot._input_parameters_defs, ComputationJobInputs)
        self.assertIsInstance(process_bot._input_params_actions, ComputationalJobInputActions)
        self.assertEqual(process_bot._input_values, {"test_message": "test message"})
        self.assertEqual(process_bot._max_running_time, datetime.timedelta(0, 10))
        self.assertEqual(process_bot.max_execution_time(), datetime.timedelta(0, 10))
        self.assertIsInstance(process_bot._output_parameters_defs, OutputParameters)
        self.assertEqual(process_bot._remote_wps_baseurl, "test_base_url")
        self.assertEqual(
            process_bot._resource_file_dir,
            path("./src/wpsremote/xmpp_data/test/resource_dir")
        )
        self.assertEqual(
            process_bot.get_resource_file_dir(),
            path("./src/wpsremote/xmpp_data/test/resource_dir")
        )
        self.assertEqual(len(process_bot._stdout_action), 6)
        for stdout_action in process_bot._stdout_action:
            self.assertIn(stdout_action, ['ignore', 'progress', 'log', 'log', 'log', 'abort'])
        self.assertEqual(len(process_bot._stdout_parser), 6)
        for stdout_parser in process_bot._stdout_parser:
            self.assertIn(stdout_parser, [
                '.*\\[DEBUG\\](.*)',
                '.*\\[INFO\\] ProgressInfo\\:([-+]?[0-9]*\\.?[0-9]*)\\%',
                '.*\\[(INFO)\\](.*)',
                '.*\\[(WARN)\\](.*)',
                '.*\\[(ERROR)\\](.*)',
                '.*\\[(CRITICAL)\\](.*)'
        ])
        self.assertEqual(process_bot._uniqueExeId, "123")
        self.assertEqual(process_bot._uploader, None)
        self.assertEqual(process_bot._wps_execution_shared_dir, None)
        self.assertEqual(process_bot.get_wps_execution_shared_dir(), None)
        self.assertEqual(process_bot.description, "foo service")
        self.assertEqual(process_bot.namespace, "default")
        self.assertEqual(process_bot.service, "Service")
        self.assertEqual(
            process_bot.workdir(),
            process_bot._output_dir + "/" + process_bot._uniqueExeId
        )
        # handle_finish
        finish_msg = {
            "type": "normal",
            "body": "topic=finish",
            "from": self.from_obj_mock
        }
        finished_message = self.xmpp_bus.CreateIndipendentMessage(finish_msg)
        with self.assertRaises(SystemExit) as cm_finish:
            process_bot.handle_finish(finished_message)
            self.assertEqual(cm_finish.exception.code, 0)
        # handle_abort
        abort_msg = {
            "type": "normal",
            "body": "topic=abort",
            "from": self.from_obj_mock
        }
        abort_message = self.xmpp_bus.CreateIndipendentMessage(abort_msg)
        with self.assertRaises(SystemExit) as cm_abort:
            process_bot.handle_abort(abort_message)
            self.assertEqual(cm_abort.exception.code, -1)
        with self.assertRaises(SystemExit):
            process_bot.exit(0)
        # kill process
        self.cleaner.kill_processbot()
        self.assertFalse(psutil.pid_exists(self.cleaner._processbot_pid))

    def test_service_bot(self):
        wps_agent = MockWPSAgentService(self.args)
        # test bot
        service_bot = wps_agent.create_bot()
        self.assertIsInstance(service_bot, ServiceBot)
        self.assertTrue(service_bot._active)
        self.assertIsInstance(service_bot._input_parameters_defs, ComputationJobInputs)
        self.assertEqual(service_bot._max_running_time, datetime.timedelta(0, 10))
        self.assertEqual(
            service_bot._output_dir,
            path('src\\wpsremote\\xmpp_data\\test\\tmp')
        )
        self.assertIsInstance(service_bot._output_parameters_defs, OutputParameters)
        self.assertTrue(service_bot._redirect_process_stdout_to_logger)
        self.assertEqual(
            service_bot._remote_config_filepath,
            './src/wpsremote/xmpp_data/test/test_remote.config'
        )
        self.assertIsNone(service_bot._remote_wps_endpoint)
        self.assertEqual(
            service_bot._resource_file_dir,
            path('./src/wpsremote/xmpp_data/test/resource_dir')
        )
        self.assertEqual(
            service_bot.get_resource_file_dir(),
            path("./src/wpsremote/xmpp_data/test/resource_dir")
        )
        self.assertIsInstance(service_bot._resource_monitor, MockResourceMonitor)
        self.assertEqual(
            service_bot._service_config_file,
            './src/wpsremote/xmpp_data/test/test_service.config'
        )
        self.assertIsNone(service_bot._wps_execution_shared_dir)
        self.assertEqual(
            service_bot.max_execution_time(),
            datetime.timedelta(0, 10)
        )
        self.assertEqual(
            service_bot.get_wps_execution_shared_dir(),
            None
        )
        self.assertIsNotNone(service_bot.bus)
        self.assertEqual(service_bot.description, 'foo service')
        self.assertEqual(service_bot.namespace, 'default')
        self.assertEqual(service_bot.running_process, {})
        self.assertEqual(service_bot.service, 'Service')
        self.assertEqual(
            service_bot._process_blacklist,
            json.loads(service_bot._remote_config.get("DEFAULT", "process_blacklist"))
        )
        self.assertEqual(
            resource_monitor.ResourceMonitor.capacity,
            service_bot._remote_config.getint("DEFAULT", "capacity")
        )
        self.assertEqual(
            resource_monitor.ResourceMonitor.load_threshold,
            service_bot._remote_config.getint("DEFAULT", "load_threshold")
        )
        self.assertEqual(
            resource_monitor.ResourceMonitor.load_average_scan_minutes,
            service_bot._remote_config.getint("DEFAULT", "load_average_scan_minutes")
        )
        PCk = None
        try:
            process_weight_class_name = service_bot._service_config.get("DEFAULT", "process_weight")
            PCk = introspection.get_class_no_arg(process_weight_class_name)
        except BaseException:
            PCk = None
        if not PCk:
            try:
                process_weight = json.loads(
                    service_bot._service_config.get("DEFAULT", "process_weight"))
            except BaseException:
                process_weight = {"weight": "0", "coefficient": "1.0"}
            PCk = resource_monitor.ProcessWeight(process_weight)
        self.assertEqual(PCk.__class__, resource_monitor.ProcessWeight)
        _request_load = PCk.request_weight(None)
        self.assertEqual(_request_load, 15.0)
        # removing tmp files
        params_file_path = path(self.params_file)
        params_file_path.remove()


if __name__ == '__main__':
    unittest.main()
