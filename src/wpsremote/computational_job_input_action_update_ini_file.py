# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

#[Action8]
#class = updateINIfile
#input_ref = timeHorizon
#source_filepath = wcsOAAonDemand_template.properties
#target_filepath= %(workdir)s\wcsOAAonDemand.properties
#section = DEFAULT
#alias = time_horizont_days

import ConfigParser
import path

import computational_job_input_action

class ComputationalJobInputActionUpdateINIFile(computational_job_input_action.ComputationalJobInputAction):


    def __init__(self, input_ref, source, target, section, alias=None):
        super(ComputationalJobInputActionUpdateINIFile, self).__init__()
        #if not type(input_refs) is list:
        #    self._input_refs = [input_refs]
        #else:
        self._input_ref = input_ref
        self._source = source if isinstance(source, path.path) else path.path(source)
        self._target = target if isinstance(target, path.path) else path.path(target)
        self._section = section
        self._alias = alias
        self._value = None


    def set_inputs(self, inputs):
        if self._input_ref in inputs.names():
            self._value = inputs[self._input_ref].get_value()
            if not self.exists() and self._source != None:
                self._source.copyfile( self._target )
                self.update_file(inputs)
            elif not self.exists() and self._source == None:
                raise Exception("Cannot find target INI file " + str(self._target) )
            else:
                self.update_file(inputs)

    def update_file(self, inputs):
        srcINI = ConfigParser.RawConfigParser()
        #read
        src = self._target.open()
        srcINI.readfp(src)
        src.close()

        #update
        srcINI.set(self._section, self.get_attribute_name(), self._value)
                
        #write
        trg = self._target.open('w')
        srcINI.write( trg )
        trg.close()

    def get_attribute_name(self):
        return self._input_ref if self._alias==None else self._alias

    def exists(self):
        return self._target.exists()


class ComputationalJobInputActionUpdateINIFileAsList(ComputationalJobInputActionUpdateINIFile):


    def __init__(self, input_ref, source, target, section, alias=None):
        super(ComputationalJobInputActionUpdateINIFileAsList, self).__init__(input_ref, source, target, section, alias)



    def update_file(self, inputs):
        srcINI = ConfigParser.RawConfigParser()
        #read
        src = self._target.open()
        srcINI.readfp(src)
        src.close()

        json_list_str = ",".join( [ '"' + str(token) + '"' for token in self._value.split(",")] )

        #update
        srcINI.set(self._section, self.get_attribute_name(), "[" + json_list_str + "]")
                
        #write
        trg = self._target.open('w')
        srcINI.write( trg )
        trg.close()

