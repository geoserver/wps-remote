# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import pickle

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"


class BusIndependentMessage(object):
    pass


class PresenceMessage(BusIndependentMessage):
    pass


class InviteMessage(BusIndependentMessage):

    def __init__(self, payload, originator):
        self._originator = originator
        self._payload = payload

    def originator(self):
        return self._originator


class RegisterMessage(BusIndependentMessage):

    def __init__(self, originator, service, namespace, descritpion, par, output):
        self._originator = originator
        self.service = service
        self.namespace = namespace
        self.description = descritpion
        self._input_parameter = par
        self.output = output

    def input_parameters(self):
        return self._input_parameter

    def originator(self):
        return self._originator


class ExecuteMessage(BusIndependentMessage):

    @staticmethod
    def deserialize(filepath):
        fp = open(filepath)
        exe_msg = pickle.load(fp)
        fp.close()
        return exe_msg

    def __init__(self, originator, uniqueExeId, baseURL, variables):
        self._uniqueExeId = uniqueExeId
        self._baseURL = baseURL
        self._originator = originator
        self._variables = variables

    def variables(self):
        return self._variables

    def originator(self):
        return self._originator

    def UniqueId(self):
        return self._uniqueExeId

    def BaseURL(self):
        return self._baseURL

    def serialize(self, fileptr):
        pickle.dump(self, fileptr)


class ProgressMessage(BusIndependentMessage):

    def __init__(self, originator, progress):
        self.originator = originator
        self.progress = progress


class LogMessage(BusIndependentMessage):

    def __init__(self, originator, level, msg):
        self.level = level
        self.originator = originator
        self.msg = msg


class CompletedMessage(BusIndependentMessage):

    def __init__(self, originator, base_url, outputs):
        self.originator = originator
        self.base_url = base_url
        self._outputs = outputs

    def outputs(self):
        return self._outputs


class FinishMessage(BusIndependentMessage):

    def __init__(self, payload, originator):
        self.originator = originator
        self.payload = payload


class ErrorMessage(BusIndependentMessage):

    def __init__(self, originator, msg, id=None):
        self.originator = originator
        self.msg = msg
        self.id = id


class AbortMessage(BusIndependentMessage):

    def __init__(self, payload, originator):
        self.originator = originator
        self.payload = payload


class GetLoadAverageMessage(BusIndependentMessage):

    def __init__(self, payload, originator):
        self._originator = originator
        self._payload = payload

    def originator(self):
        return self._originator


class LoadAverageMessage(BusIndependentMessage):

    def __init__(self, originator, outputs):
        self.originator = originator
        self._outputs = outputs

    def outputs(self):
        return self._outputs
