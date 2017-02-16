# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

class Bus(object):
    def __init__(self, id):
        self.callbacks={}
        self.id = id

    def Listen(self):
        pass

    def CheckServerIdentity(self, serverId):
        pass

    def SendMessage(self,Message):
        pass

    def Stop(self, Message):
        pass

    def RegisterMessageCallback(self, message_type, callback):
        self.callbacks[message_type] = callback
