# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import computation_job_input

class ComputationJobParam(computation_job_input.ComputationJobInput):

    def __init__(self, name, input_type, title, descr, default=None, formatter=None, min_occurencies=0, max_occurencies=1, input_mime_type=None):
        super(ComputationJobParam, self).__init__(name, input_type, title, descr, default, formatter, input_mime_type)
        self._min = min_occurencies
        self._max = max_occurencies

    def validate(self):
        if not (self._min <= len(self._value) and len(self._value) <= self._max):
            raise TypeError("Actual value for parameter has wrong multiplicity")
        return super(ComputationJobParam, self).validate()





