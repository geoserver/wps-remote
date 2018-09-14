# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import os
import tempfile
import path
import json
import uuid

# ############################################################################################################# #
#                                                                                                               #
#    Text/Plain Output Map Format                                                                               #
#                                                                                                               #
# ############################################################################################################# #
class OutputFileParameter(object):
    
    def __init__(self, par_name, d, template_vars_for_param_types=None, wps_execution_shared_dir=None, uploader=None):
        #{"type": "string", "description": "xml OAA output file", "filepath" : "%workdir\\\\output_file.xml" }
        self._name=par_name
        self._type=None
        self._description = None
        self._title = None
        self._filepath = None
        self._output_mime_type = None

        self._wps_execution_shared_dir = wps_execution_shared_dir
        self._uploader = uploader
        self._backup_on_wps_execution_shared_dir = None
        self._upload_data = None
        self._upload_data_root = None
        self._publish_as_layer = None
        self._publish_layer_name = None
        self._publish_default_style = None
        self._publish_target_workspace = None
        self._publish_metadata = None

        for k,v in d.items():
            if hasattr(self, "_" + k):
                if template_vars_for_param_types != None and isinstance(v, basestring):
                    for var, val in template_vars_for_param_types.items():
                        if var in v:
                            v=v.replace("%" + var,val)
                    
                setattr(self, "_" + k, v)

        self._filepath = path.path(self._filepath)

    def get_name(self):
        return self._name

    def as_json_string(self):
        #{"type": "string", "description": "A persons surname", "max": 1, "default": "Meier"}
        res={}
        attrib_to_convert = ['_type', '_description', '_title', '_output_mime_type', '_publish_as_layer', '_publish_layer_name', '_publish_default_style', '_publish_target_workspace']
        attribute_list = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]
        attribute_list_filtered = [x for x in attribute_list if x in attrib_to_convert]
        for a in attribute_list_filtered:
            res[a[1:]] = getattr(self, a)
        return json.dumps(res)

    def get_value(self):
        if self._backup_on_wps_execution_shared_dir != None and self._backup_on_wps_execution_shared_dir and self._wps_execution_shared_dir != None:
            unique_dirname = str(uuid.uuid4())
            bkp_dir = path.path(self._wps_execution_shared_dir + "/" + unique_dirname)
            bkp_dir.makedirs()
            dst = bkp_dir.abspath() + "/" + self._filepath.basename()

            self._filepath.copy(dst)
            dst = path.path(dst)

            return dst.text()
        elif self._upload_data != None and self._upload_data and self._uploader != None:
            unique_dirname = str(uuid.uuid4())
            bkp_dir = path.path(tempfile.gettempdir() + '/' + unique_dirname)
            bkp_dir.makedirs()
            dst = bkp_dir.abspath() + '/' + self._filepath.basename()

            self._filepath.copy(dst)
            dst = path.path(dst)

            src_path = os.path.abspath(os.path.join(dst.abspath(), os.pardir))
            if self._upload_data_root:
                unique_dirname = self._upload_data_root + '/' + unique_dirname
            self._uploader.Upload(hostdir=unique_dirname, text='', binary='*.*', src=src_path)

            return self._filepath.text()
        else:
            return self._filepath.text()

    def get_type(self):
        return "textual"

    def get_description(self):
        return self._description

    def get_title(self):
        return self._title

    def get_output_mime_type(self):
        return self._output_mime_type

    def is_publish_as_layer(self):
        return (self._publish_as_layer != None and self._publish_as_layer == "true")

    def get_publish_layer_name(self):
        return self._publish_layer_name

    def get_publish_default_style(self):
        return self._publish_default_style

    def get_publish_target_workspace(self):
        return self._publish_target_workspace

    def get_metadata(self):
        if self._publish_metadata != None:
            metadata_file = path.path(self._publish_metadata)

            if metadata_file.isfile():
                return metadata_file.text() 
        return ' '

# ############################################################################################################# #
#                                                                                                               #
#    RAW File Output Map Format                                                                                 #
#                                                                                                               #
# ############################################################################################################# #
class RawFileParameter(object):
    
    def __init__(self, par_name, d, template_vars_for_param_types=None, wps_execution_shared_dir=None, uploader=None):
        #{"type": "string", "description": "xml OAA output file", "filepath" : "%workdir\\\\output_file.xml" }
        self._name=par_name
        self._type=None
        self._description = None
        self._title = None
        self._filepath = None
        self._output_mime_type = None

        self._wps_execution_shared_dir = wps_execution_shared_dir
        self._uploader = uploader
        self._backup_on_wps_execution_shared_dir = None
        self._upload_data = None
        self._upload_data_root = None
        self._publish_as_layer = None
        self._publish_layer_name = None
        self._publish_default_style = None
        self._publish_target_workspace = None
        self._publish_metadata = None

        for k,v in d.items():
            if hasattr(self, "_" + k):
                if template_vars_for_param_types != None and isinstance(v, basestring):
                    for var, val in template_vars_for_param_types.items():
                        if var in v:
                            v=v.replace("%" + var,val)
                    
                setattr(self, "_" + k, v)

        self._filepath = path.path(self._filepath)

    def get_name(self):
        return self._name

    def as_json_string(self):
        #{"type": "string", "description": "A persons surname", "max": 1, "default": "Meier"}
        res={}
        attrib_to_convert = ['_type', '_description', '_title', '_output_mime_type', '_publish_as_layer', '_publish_layer_name', '_publish_default_style', '_publish_target_workspace']
        attribute_list = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]
        attribute_list_filtered = [x for x in attribute_list if x in attrib_to_convert]
        for a in attribute_list_filtered:
            res[a[1:]] = getattr(self, a)
        return  json.dumps(res)

    def get_value(self):
        if self._backup_on_wps_execution_shared_dir != None and self._backup_on_wps_execution_shared_dir and self._wps_execution_shared_dir != None:
            unique_dirname = str(uuid.uuid4())
            bkp_dir = path.path(self._wps_execution_shared_dir + "/" + unique_dirname)
            bkp_dir.makedirs()
            dst = bkp_dir.abspath() + "/" + self._filepath.basename()

            self._filepath.copy(dst)
            dst = path.path(dst)

            return dst
        elif self._upload_data != None and self._upload_data and self._uploader != None:
            unique_dirname = str(uuid.uuid4())
            
            if self._upload_data_root:
                unique_dirname = self._upload_data_root + '/' + unique_dirname
            src_path = os.path.abspath(os.path.join(self._filepath.abspath(), os.pardir))
            basename = os.path.basename(self._filepath.abspath())
            basename = os.path.splitext(basename)[0]
            self._uploader.Upload(hostdir=unique_dirname, text='', binary=basename+'*.*', src=src_path)

            return path.path(unique_dirname + "/" + self._filepath.basename())
        else:
            return self._filepath

    def get_type(self):
        return self._type

    def get_description(self):
        return self._description

    def get_title(self):
        return self._title

    def get_output_mime_type(self):
        return self._output_mime_type

    def is_publish_as_layer(self):
        return (self._publish_as_layer != None and self._publish_as_layer == "true")

    def get_publish_layer_name(self):
        return self._publish_layer_name

    def get_publish_default_style(self):
        return self._publish_default_style

    def get_publish_target_workspace(self):
        return self._publish_target_workspace

    def get_metadata(self):
        if self._publish_metadata != None:
            metadata_file = path.path(self._publish_metadata)

            if metadata_file.isfile():
                return metadata_file.text() 
        return ' '


# ############################################################################################################# #
#                                                                                                               #
#    OWC Json Output Map Format                                                                                 #
#                                                                                                               #
# ############################################################################################################# #
class OWCFileParameter(object):
    
    def __init__(self, par_name, d, parameters_types_defs, template_vars_for_param_types=None, wps_execution_shared_dir=None, uploader=None):
        #{"type": "string", "description": "xml OAA output file", "filepath" : "%workdir\\\\output_file.xml" }
        self._name=par_name
        self._type=None
        self._description = None
        self._title = None
        self._output_mime_type = None

        self._layers_to_publish = None

        self._wps_execution_shared_dir = wps_execution_shared_dir
        self._uploader = uploader
        self._backup_on_wps_execution_shared_dir = None
        self._upload_data = None
        self._upload_data_root = None
        self._publish_as_layer = "true"
        self._publish_layer_name = None
        self._publish_metadata = None

        for k,v in d.items():
            if hasattr(self, "_" + k):
                if template_vars_for_param_types != None and isinstance(v, basestring):
                    for var, val in template_vars_for_param_types.items():
                        if var in v:
                            v=v.replace("%" + var,val)
                    
                setattr(self, "_" + k, v)

        self._files_to_publish  = ''
        self._default_styles    = ''
        self._target_workspaces = ''

        if self._layers_to_publish != None:
            self._parameters_types_defs = parameters_types_defs

            layer_names = self._layers_to_publish.split(';')
            for name in layer_names:
                if self._parameters_types_defs[name] != None:
                    publish_layer_name = self._parameters_types_defs[name].get('publish_layer_name')
                    publish_layer_name = publish_layer_name if publish_layer_name != None else ' '

                    publish_default_style = self._parameters_types_defs[name].get('publish_default_style')
                    publish_default_style = publish_default_style if publish_default_style != None else ' '

                    publish_target_workspace = self._parameters_types_defs[name].get('publish_target_workspace')
                    publish_target_workspace = publish_target_workspace if publish_target_workspace != None else ' '

                    self._files_to_publish += publish_layer_name + ";"
                    self._default_styles   += publish_default_style + ";"
                    self._target_workspaces+= publish_target_workspace + ";"

    def get_name(self):
        return self._name

    def as_json_string(self):
        #{"type": "string", "description": "A persons surname", "max": 1, "default": "Meier"}
        res={}
        attrib_to_convert = ['_type', '_description', '_title', '_output_mime_type', '_publish_as_layer', '_publish_layer_name', '_files_to_publish', '_default_styles', '_target_workspaces']
        attribute_list = [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]
        attribute_list_filtered = [x for x in attribute_list if x in attrib_to_convert]
        for a in attribute_list_filtered:
            res[a[1:]] = getattr(self, a)
        return  json.dumps(res)

    def get_value(self):
        if self._backup_on_wps_execution_shared_dir != None and self._backup_on_wps_execution_shared_dir and self._wps_execution_shared_dir != None:
            unique_dirname = str(uuid.uuid4())
            bkp_dir = path.path(self._wps_execution_shared_dir + "/" + unique_dirname)
            bkp_dir.makedirs()

            tokens = self._files_to_publish.split(';')

            files_to_publish = ""
            for token in tokens:
                filepath = path.path(token)
                dst = bkp_dir.abspath() + "/" + filepath.basename()
                filepath.copy(dst)
                dst = path.path(dst)

                if len(files_to_publish) > 0:
                    files_to_publish = files_to_publish + ";"
                files_to_publish = files_to_publish + dst.abspath()

            return files_to_publish
        elif self._upload_data != None and self._upload_data and self._uploader != None:
            unique_dirname = str(uuid.uuid4())
            bkp_dir = path.path(tempfile.gettempdir() + '/' + unique_dirname)
            bkp_dir.makedirs()

            tokens = self._files_to_publish.split(';')

            if self._upload_data_root:
                unique_dirname = self._upload_data_root + '/' + unique_dirname

            files_to_publish = ""
            for token in tokens:
                filepath = path.path(token)
                dst = bkp_dir.abspath() + '/' + filepath.basename()
                filepath.copy(dst)
                dst = path.path(dst)

                if len(files_to_publish) > 0:
                    files_to_publish = files_to_publish + ';'
                files_to_publish = files_to_publish + '/' + unique_dirname + '/' + filepath.basename()

            self._uploader.Upload(hostdir=unique_dirname, text='', binary='*.*', src=bkp_dir.abspath())

            return files_to_publish
        else:
            return self._files_to_publish

    def get_type(self):
        return self._type

    def get_description(self):
        return self._description

    def get_title(self):
        return self._title

    def get_output_mime_type(self):
        return self._output_mime_type

    def is_publish_as_layer(self):
        return (self._publish_as_layer != None and self._publish_as_layer == "true")

    def get_publish_layer_name(self):
        return self._publish_layer_name

    def get_publish_default_style(self):
        return self._default_styles

    def get_publish_target_workspace(self):
        return self._target_workspaces

    def get_metadata(self):
        if self._publish_metadata != None:
            metadata_file = path.path(self._publish_metadata)

            if metadata_file.isfile():
                return metadata_file.text() 
        return ' '
