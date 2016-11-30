# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import os, sys, inspect, urllib, json
import logging
import traceback

os.chdir(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
sys.path.insert(0, os.getcwd())
sys.path.append(os.path.abspath('lib'))

import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout

class XMPPPresenceMessage(object):

    def __init__(self, xmppChannel):
        self.xmppChannel=xmppChannel

    def send(self):
        self.xmppChannel.send_presence()
        self.xmppChannel.JoinmMUC()

class XMPPRegisterMessage(object):

    def __init__(self, xmppChannel, originator, service, namespace, descritpion, par, output):
        self.xmppChannel=xmppChannel
        self.originator=originator
        self.service=service
        self.namespace=namespace
        self.description=descritpion
        self._input_parameter=par
        self.output=output

    def title(self):
        return self.namespace + "." + self.service 

    def send(self):
        service = {}
        service['title'] = self.title()
        service['namespace'] = self.namespace
        service['description'] = self.description
        #process_buffer & result_size kept for back compatibility with STBGIS protocol 
        service['process_buffer'] = 0
        service['result_size'] = 0
        service['input']= self._input_parameter
        service['output']= self.output
        body = ''.join(['topic=register', '&service=', self.xmppChannel.get_fully_qualified_service_name(), '&message=', urllib.quote(json.dumps(service))])

        #self.xmppChannel.xmpp.send_message(mto=self.originator, mbody=body, mtype='chat')
        self.xmppChannel.xmpp.send_message(mto=self.originator, mbody=body, mtype='chat')

class XMPPProgressMessage(object):

    def __init__(self, originator, xmppChannel, progress):
        self.xmppChannel=xmppChannel
        self.progress=progress
        self.originator=originator

    def send(self):
        body = ''.join(['topic=progress', '&id=', self.xmppChannel.id, '&message=', str( self.progress)])
        self.xmppChannel.xmpp.send_message(mto=self.originator, mbody=body, mtype='chat')

class XMPPLogMessage(object):

    def __init__(self, originator, xmppChannel, level, msg):
        self.xmppChannel=xmppChannel
        self.level=level
        self.msg=msg
        self.originator=originator

    def send(self):
        body = ''.join(['topic=log', '&id=', self.xmppChannel.id, '&level=', self.level, "&message=", self.msg ])
        self.xmppChannel.xmpp.send_message(mto=self.originator, mbody=body, mtype='chat')

class XMPPCompletedMessage(object):

    def __init__(self, originator, xmppChannel, base_url, outputs):
        self.xmppChannel = xmppChannel
        self.originator = originator
        
        self._base_url = base_url
        self._outputs = outputs

    def send(self):
        try:
            message = ""
            for out_param_name, out_param_values in self._outputs.items():
                result = dict()
                result[out_param_name+'_value']         = out_param_values[0] #value
                result[out_param_name+'_description']   = out_param_values[1] #description
                result[out_param_name+'_title']         = out_param_values[2] #title
                result[out_param_name+'_type']          = out_param_values[3] #type
                result[out_param_name+'_pub']           = out_param_values[4] #publish as layer
                result[out_param_name+'_layer_name']    = out_param_values[5] #publish layer name
                result[out_param_name+'_style']         = out_param_values[6] #publish default Style
                result[out_param_name+'_workspace']     = out_param_values[7] #publish target Workspace
                result[out_param_name+'_metadata']      = out_param_values[8] #publish target MetaData
                result_json = json.dumps(result)
                result_json_url_enc=urllib.quote(result_json)
                if len(message) > 0:
                    message = message + "&"
                message = message + out_param_name + "=" + result_json_url_enc

            body = ''.join(['topic=completed', '&id=', self.xmppChannel.id,"&baseURL=",self._base_url, "&message=completed","&",message])
            self.xmppChannel.xmpp.send_message(mto=self.originator, mbody=body, mtype='chat')
        except Exception, err:
            body = ''.join(['topic=error', '&id=', self.xmppChannel.id, "&message=", "Critical error while encoding outuput!"])
            self.xmppChannel.xmpp.send_message(mto=self.originator, mbody=body, mtype='chat')
            logging.exception(str(traceback.format_exc()))
            raise

class XMPPErrorMessage(object):

    def __init__(self, originator, xmppChannel, msg, id=None):
        self.originator = originator
        self.xmppChannel = xmppChannel
        self.msg  = msg
        if id:
            self.id = id
        else:
            self.id = self.xmppChannel.id

    def send(self):

        error_json = json.dumps(self.msg)
        error_json_url_enc=urllib.quote(error_json)

        body = ''.join(['topic=error', '&id=', self.id, "&message=", error_json_url_enc])
        self.xmppChannel.xmpp.send_message(mto=self.originator, mbody=body, mtype='chat')

class XMPPLoadAverageMessage(object):

    def __init__(self, originator, xmppChannel, outputs):
        self.xmppChannel = xmppChannel
        self.originator = originator
        self._outputs = outputs

    def send(self):
        try:
            message = ""
            for out_param_name, out_param_values in self._outputs.items():
                result = dict()
                #print str(out_param_values)
                result[out_param_name+'_value']         = out_param_values[0] #value
                result[out_param_name+'_description']   = out_param_values[1] #description
                result_json = json.dumps(result)
                result_json_url_enc=urllib.quote(result_json)
                if len(message) > 0:
                    message = message + "&"
                message = message + "result_" + out_param_name + "=" + result_json_url_enc

            body = ''.join(['topic=loadavg', '&id=', self.xmppChannel.id, "&message=loadavg","&",message])
            self.xmppChannel.xmpp.send_message(mto=self.originator, mbody=body, mtype='chat')
        except Exception, err:
            print traceback.format_exc()
            body = ''.join(['topic=log', '&id=', self.xmppChannel.id, '&level=warning', "&message=", "Critical error while encoding LoadAverageMessage outuputs!"])
            self.xmppChannel.xmpp.send_message(mto=self.originator, mbody=body, mtype='chat')

