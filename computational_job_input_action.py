# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

class ComputationalJobInputAction(object):

    def __init__(self):
        pass

    def can_produce_cmd_line(self):
        m = getattr(self, "get_cmd_line", None)
        return callable(m)
