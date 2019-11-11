# (c) 2019 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import os
import unittest
import mock
import pickle
import wpsremote.config_instance as config_instance
from wpsremote.busIndependentMessages import (
    RegisterMessage, ProgressMessage, LogMessage, CompletedMessage, ErrorMessage, AbortMessage,
    LoadAverageMessage, InviteMessage, GetLoadAverageMessage, ExecuteMessage, FinishMessage,
    CannotExecuteMessage
)
from wpsremote.xmppBus import XMPPBus
from wpsremote.xmppMessages import (
    XMPPRegisterMessage, XMPPProgressMessage, XMPPLogMessage,
    XMPPCompletedMessage, XMPPErrorMessage, XMPPLoadAverageMessage,
    XMPPCannotExecuteMessage
)

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2019 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

# due to xmppMessages chdir
os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestBusIndependentMessages(unittest.TestCase):

    def setUp(self):
        self.remote_config = config_instance.create(
            "./src/wpsremote/xmpp_data/test/test_remote.config"
        )
        self.xmpp_bus = XMPPBus(self.remote_config, "service_name", "service_name_namespace")
        self.xep_0045_plugin = self.xmpp_bus.xmpp.plugin["xep_0045"]
        self.from_obj_mock = mock.Mock()

    def test_invite_message(self):
        rooms = {
            self.xmpp_bus._get_MUC_JId(): {
                "resource": {
                    "role": "not_visitor"
                }
            }
        }
        self.xep_0045_plugin.rooms = rooms
        self.from_obj_mock.resource = "resource"
        msg = {
            "type": "normal",
            "body": "topic=invite",
            "from": self.from_obj_mock
        }
        # InviteMessage
        message = self.xmpp_bus.CreateIndipendentMessage(msg)
        self.assertIsInstance(message, InviteMessage)
        self.assertEqual(message.originator(), self.from_obj_mock)

    def test_convert_register_message(self):
        input_DLR = [
            (
                'Input1',
                '{'
                '"class": param, '
                '"name": "interval", '
                '"title": Elevation Interval, '
                '"type": application/json, '
                '"description": Elevation interval between contours, '
                '"min": 1, '
                '"max": 1, '
                '"default": 200'
                '}'
            )
        ]
        output_DLR = [
            (
                'result1',
                '{'
                '"publish_layer_name": null, '
                '"description": "WPS Resource Plain Text", '
                '"title": null, '
                '"output_mime_type": null, '
                '"publish_default_style": null, '
                '"publish_as_layer": null, '
                '"type": "string", '
                '"publish_target_workspace": null'
                '}'
            )
        ]
        # RegisterMessage
        r_msg = RegisterMessage(
            originator=self.from_obj_mock,
            service="test_service",
            namespace="test_namespace",
            descritpion="test_description",
            par=input_DLR,
            output=output_DLR
        )
        c_msg = self.xmpp_bus.Convert(r_msg)
        self.assertIsInstance(c_msg, XMPPRegisterMessage)
        self.assertEqual(c_msg.title(), "test_namespace.test_service")

    def test_execute_message(self):
        rooms = {
            self.xmpp_bus._get_MUC_JId(): {
                "resource": {
                    "role": "not_visitor"
                }
            }
        }
        self.xep_0045_plugin.rooms = rooms
        from_obj_mock = mock.Mock()
        from_obj_mock.resource = "resource"
        test_msg = pickle.dumps("test_message")
        msg = {
            "type": "normal",
            "body": "topic=request&id=123&baseURL=test_base_url&message={}".format(test_msg),
            "from": from_obj_mock
        }
        # ExecuteMessage
        message = self.xmpp_bus.CreateIndipendentMessage(msg)
        self.assertIsInstance(message, ExecuteMessage)

    def test_progress_message(self):
        # ProgressMessage
        r_msg = ProgressMessage(self.from_obj_mock, 1.34)
        c_msg = self.xmpp_bus.Convert(r_msg)
        self.assertIsInstance(c_msg, XMPPProgressMessage)
        self.assertEqual(c_msg.originator, self.from_obj_mock)
        self.assertEqual(c_msg.progress, 1.34)
        self.assertEqual(c_msg.xmppChannel, self.xmpp_bus)

    def test_convert_log_message(self):
        # LogMessage
        r_msg = LogMessage(self.from_obj_mock, "INFO", "test_message_text")
        c_msg = self.xmpp_bus.Convert(r_msg)
        self.assertIsInstance(c_msg, XMPPLogMessage)
        self.assertEqual(c_msg.originator, self.from_obj_mock)
        self.assertEqual(c_msg.level, "INFO")
        self.assertEqual(c_msg.msg, "test_message_text")

    def test_convert_completed_message(self):
        outputs = {
            'result1': {
                "publish_layer_name": None,
                "description": "WPS Resource Plain Text",
                "title": None,
                "output_mime_type": None,
                "publish_default_style": None,
                "publish_as_layer": None,
                "type": "string",
                "publish_target_workspace": None
            }
        }
        # CompletedMessage
        r_msg = CompletedMessage(self.from_obj_mock, "test_base_url", outputs)
        c_msg = self.xmpp_bus.Convert(r_msg)
        self.assertIsInstance(c_msg, XMPPCompletedMessage)
        self.assertEqual(c_msg.originator, self.from_obj_mock)
        self.assertEqual(c_msg._base_url, "test_base_url")
        self.assertEqual(c_msg._outputs, outputs)

    def test_finish_message(self):
        rooms = {
            self.xmpp_bus._get_MUC_JId(): {
                "resource": {
                    "role": "not_visitor"
                }
            }
        }
        self.xep_0045_plugin.rooms = rooms
        self.from_obj_mock.resource = "resource"
        msg = {
            "type": "normal",
            "body": "topic=finish",
            "from": self.from_obj_mock
        }
        # FinishMessage
        message = self.xmpp_bus.CreateIndipendentMessage(msg)
        self.assertIsInstance(message, FinishMessage)

    def test_convert_error_message(self):
        # ErrorMessage
        r_msg = ErrorMessage(self.from_obj_mock, "test_error_message_text")
        c_msg = self.xmpp_bus.Convert(r_msg)
        self.assertIsInstance(c_msg, XMPPErrorMessage)
        self.assertEqual(c_msg.originator, self.from_obj_mock)
        self.assertEqual(c_msg.xmppChannel, self.xmpp_bus)
        self.assertEqual(c_msg.id, self.xmpp_bus.id)
        self.assertEqual(c_msg.msg, "test_error_message_text")

    def test_abort_message(self):
        rooms = {
            self.xmpp_bus._get_MUC_JId(): {
                "resource": {
                    "role": "not_visitor"
                }
            }
        }
        self.xep_0045_plugin.rooms = rooms
        self.from_obj_mock.resource = "resource"
        msg = {
            "type": "normal",
            "body": "topic=abort",
            "from": self.from_obj_mock
        }
        # AbortMessage
        message = self.xmpp_bus.CreateIndipendentMessage(msg)
        self.assertIsInstance(message, AbortMessage)

    def test_get_load_average_message(self):
        rooms = {
            self.xmpp_bus._get_MUC_JId(): {
                "resource": {
                    "role": "not_visitor"
                }
            }
        }
        self.xep_0045_plugin.rooms = rooms
        self.from_obj_mock.resource = "resource"
        msg = {
            "type": "normal",
            "body": "topic=getloadavg",
            "from": self.from_obj_mock
        }
        # GetLoadAverageMessage
        message = self.xmpp_bus.CreateIndipendentMessage(msg)
        self.assertIsInstance(message, GetLoadAverageMessage)
        self.assertEqual(message.originator(), self.from_obj_mock)

    def test_convert_load_average_message(self):
        outputs = {
            'result1': {
                "publish_layer_name": None,
                "description": "WPS Resource Plain Text",
                "title": None,
                "output_mime_type": None,
                "publish_default_style": None,
                "publish_as_layer": None,
                "type": "string",
                "publish_target_workspace": None
            }
        }
        # LoadAverageMessage
        r_msg = LoadAverageMessage(self.from_obj_mock, outputs)
        c_msg = self.xmpp_bus.Convert(r_msg)
        self.assertIsInstance(c_msg, XMPPLoadAverageMessage)
        self.assertEqual(c_msg.originator, self.from_obj_mock)
        self.assertEqual(c_msg._outputs, outputs)
        self.assertEqual(c_msg.send(), None)

    def test_convert_cannot_execute_message(self):
        outputs = {
            'result1': {
                "publish_layer_name": None,
                "description": "WPS Resource Plain Text",
                "title": None,
                "output_mime_type": None,
                "publish_default_style": None,
                "publish_as_layer": None,
                "type": "string",
                "publish_target_workspace": None
            }
        }
        # CannotExecuteMessage
        r_msg = CannotExecuteMessage(self.from_obj_mock, outputs)
        c_msg = self.xmpp_bus.Convert(r_msg)
        self.assertIsInstance(c_msg, XMPPCannotExecuteMessage)
        self.assertEqual(c_msg.originator, self.from_obj_mock)
        self.assertEqual(c_msg._outputs, outputs)
        self.assertEqual(c_msg.xmppChannel, self.xmpp_bus)
        self.assertEqual(c_msg.send(), None)

    def test_clone_for_process(self):
        clone = self.xmpp_bus.clone_for_process("not_master")
        self.assertEqual(clone.config, self.xmpp_bus.config)
        self.assertEqual(clone.address, self.xmpp_bus.address)
        self.assertEqual(clone.domain, self.xmpp_bus.domain)
        self.assertEqual(clone.MUC_name, self.xmpp_bus.MUC_name)
        self.assertEqual(clone.username, self.xmpp_bus.username)
        self.assertEqual(clone.password, self.xmpp_bus.password)
        self.assertEqual(clone.nameSpacePassword, self.xmpp_bus.nameSpacePassword)
        self.assertEqual(clone._service_name, self.xmpp_bus._service_name)
        self.assertEqual(clone._service_name_namespace, self.xmpp_bus._service_name_namespace)
        self.assertEqual(
            clone._fully_qualified_service_name,
            self.xmpp_bus._fully_qualified_service_name
        )

    def test_get_MUC_JId(self):
        self.assertEqual(
            "service_name_namespace@conference.geoserver.org",
            self.xmpp_bus._get_MUC_JId()
        )

    def test_get_fully_qualified_service_name(self):
        self.assertEqual(
            "service_name_namespace.service_name",
            self.xmpp_bus.get_fully_qualified_service_name()
        )

    def test_state(self):
        self.assertEqual("disconnected", self.xmpp_bus.state())


if __name__ == '__main__':
    unittest.main()
