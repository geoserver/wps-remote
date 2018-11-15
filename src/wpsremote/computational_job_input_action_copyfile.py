# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import path
import computational_job_input_action

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"


class ComputationalJobInputActionCopyFile(computational_job_input_action.ComputationalJobInputAction):

    def __init__(self, source, target):
        super(ComputationalJobInputActionCopyFile, self).__init__()

        self._source = source if isinstance(source, path.path) else path.path(source)
        self._target = target if isinstance(target, path.path) else path.path(target)

    def set_inputs(self, inputs):
        self._source.copyfile(self._target)
