# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

from wpsagent import WPSAgentService, WPSAgentProcess
from wpsremote.resource_monitor import ResourceMonitor

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"


class FileLikeObjectMock(object):
    def __init__(self, lines, linesep="\n"):
        if isinstance(lines, list):
            self._lines = lines
        else:
            self._lines = lines.split(linesep)
            self._lines = map(lambda l: l.strip(), self._lines)
        self._lp = 0

    def readline(self):
        if self._lp-1 >= len(self._lines):
            return ''
        else:
            self._lp += 1
            return self._lines[self._lp-1]


class MockWPSAgentService(WPSAgentService):

    def run(self):
        pass


class MockWPSAgentProcess(WPSAgentProcess):

    def run(self):
        pass


class MockResourceMonitor(ResourceMonitor):
    def run(self):
        pass


def mock_clean_up_all():
    pass
