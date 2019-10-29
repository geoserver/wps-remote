# (c) 2019 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import unittest
import wpsremote.ConfigParser as ConfigParser
from wpsremote import mockutils
from wpsremote.output_file_parameter import (
    OutputFileParameter, RawFileParameter, OWCFileParameter
)
from wpsremote.output_parameters import OutputParameters

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2019 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"


class TestComputationJobOutputs(unittest.TestCase):

    result1_DLR = [
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
    result2_DLR = [
        (
            'result2',
            '{'
            '"publish_layer_name": "srtm_39_04_c", '
            '"description": "WPS Resource Binary File", '
            '"title": null, '
            '"output_mime_type": null, '
            '"publish_default_style": "raster", '
            '"publish_as_layer": "true", '
            '"type": "image/geotiff", '
            '"publish_target_workspace": "it.geosolutions"'
            '}'
        )

    ]
    result3_DLR = [
        (
            'result3',
            '{'
            '"publish_layer_name": "srtm_39_04_c", '
            '"description": "WPS Resource Binary Stream", '
            '"title": "This Is A GeoTIFF Layer", '
            '"output_mime_type": null, '
            '"publish_default_style": "raster", '
            '"publish_as_layer": "true", '
            '"type": "image/geotiff;stream", '
            '"publish_target_workspace": "it.geosolutions"'
            '}'
        )
    ]
    result4_DLR = [
        (
            'result4',
            '{'
            '"publish_layer_name": "wind", '
            '"description": "NetCDF Binary File", '
            '"title": "Wind", '
            '"output_mime_type": null, '
            '"publish_default_style": "raster", '
            '"publish_as_layer": "true", '
            '"type": "application/x-netcdf", '
            '"publish_target_workspace": "it.geosolutions"'
            '}'
        )
    ]
    result5_DLR = [
        (
            'result5',
            '{'
            '"publish_layer_name": null, '
            '"description": "WPS Resource GML", '
            '"title": null, '
            '"output_mime_type": null, '
            '"publish_default_style": null, '
            '"publish_as_layer": null, '
            '"type": "text/xml;subtype=gml/3.1.1", '
            '"publish_target_workspace": null'
            '}'
        )
    ]
    result6_DLR = [
        (
            'result6',
            '{'
            '"publish_layer_name": null, '
            '"description": "Video MP4 Binary File", '
            '"title": "Wind", '
            '"output_mime_type": null, '
            '"publish_default_style": null, '
            '"publish_as_layer": null, '
            '"type": "video/mp4", '
            '"publish_target_workspace": null'
            '}'
        )
    ]
    result7_DLR = [
        (
            'result7',
            '{'
            '"publish_layer_name": "owc_json_ctx", '
            '"description": "WPS OWC Json MapContext", '
            '"default_styles": "", '
            '"target_workspaces": "", '
            '"output_mime_type": null, '
            '"title": null, '
            '"files_to_publish": "", '
            '"publish_as_layer": "true", '
            '"type": "application/owc"'
            '}'
        )
    ]

    def test_string_output_type_from_ini(self):
        ini_text = '''[Output1]
        name = result1
        type = string
        description = WPS Resource Plain Text
        filepath = ./src/wpsremote/xmpp_data/test/test_file
        '''
        config = ConfigParser.ConfigParser()
        ini_file = mockutils.FileLikeObjectMock(ini_text)
        config.readfp(ini_file)
        output_section = config.items('Output1')
        op = OutputParameters.create_from_config({'Output1': output_section})
        self.assertEqual(self.result1_DLR, op.as_DLR_protocol())
        self.assertEqual(['test content'], op.get_values())
        # OutputFileParameter
        ofp = op._params['result1']
        self.assertIsInstance(ofp, OutputFileParameter)
        self.assertEqual("WPS Resource Plain Text", ofp.get_description())
        self.assertEqual("", ofp.get_metadata().strip(" "))
        self.assertEqual("result1", ofp.get_name())
        # print ofp.get_output_mime_type()
        self.assertIsNone(ofp.get_publish_default_style())
        self.assertIsNone(ofp.get_publish_layer_name())
        self.assertIsNone(ofp.get_publish_target_workspace())
        self.assertIsNone(ofp.get_title())
        self.assertEqual("textual", ofp.get_type())
        self.assertIn(ofp.as_json_string(), self.result1_DLR[0][1])
        self.assertFalse(ofp.is_publish_as_layer())
        self.assertEqual('test content', ofp.get_value())

    def test_image_geotiff_output_type_from_ini(self):
        ini_text = '''[Output2]
        name = result2
        type = image/geotiff
        description = WPS Resource Binary File
        backup_on_wps_execution_shared_dir = true
        publish_as_layer = true
        publish_default_style = raster
        publish_target_workspace = it.geosolutions
        publish_layer_name = srtm_39_04_c
        filepath = ./src/wpsremote/xmpp_data/test/test_file
        '''
        config = ConfigParser.ConfigParser()
        ini_file = mockutils.FileLikeObjectMock(ini_text)
        config.readfp(ini_file)
        output_section = config.items('Output2')
        op = OutputParameters.create_from_config({'Output2': output_section})
        self.assertEqual(self.result2_DLR, op.as_DLR_protocol())
        self.assertEqual(['./src/wpsremote/xmpp_data/test/test_file'], op.get_values())
        # RawFileParameter
        rfp = op._params['result2']
        self.assertIsInstance(rfp, RawFileParameter)
        self.assertEqual("result2", rfp.get_name())
        self.assertEqual("srtm_39_04_c", rfp.get_publish_layer_name())
        self.assertEqual("WPS Resource Binary File", rfp.get_description())
        self.assertIsNone(rfp.get_title())
        self.assertEqual("", rfp.get_metadata().strip(" "))
        # self.assertIsNone(rfp.get_output_mime_type())
        self.assertEqual("raster", rfp.get_publish_default_style())
        self.assertTrue(rfp.is_publish_as_layer())
        self.assertEqual("image/geotiff", rfp.get_type())
        self.assertEqual("it.geosolutions", rfp.get_publish_target_workspace())
        self.assertIn(rfp.as_json_string(), self.result2_DLR[0][1])
        self.assertEqual('./src/wpsremote/xmpp_data/test/test_file', rfp.get_value())

    def test_image_geotiff_stream_output_type_from_ini(self):
        ini_text = '''[Output3]
        name = result3
        type = image/geotiff;stream
        description = WPS Resource Binary Stream
        title = This Is A GeoTIFF Layer
        publish_as_layer = true
        publish_default_style = raster
        publish_target_workspace = it.geosolutions
        publish_layer_name = srtm_39_04_c
        filepath = ./src/wpsremote/xmpp_data/test/test_file
        '''
        config = ConfigParser.ConfigParser()
        ini_file = mockutils.FileLikeObjectMock(ini_text)
        config.readfp(ini_file)
        output_section = config.items('Output3')
        op = OutputParameters.create_from_config({'Output3': output_section})
        self.assertEqual(self.result3_DLR, op.as_DLR_protocol())
        self.assertEqual(['./src/wpsremote/xmpp_data/test/test_file'], op.get_values())
        # RawFileParameter
        rfp = op._params['result3']
        self.assertIsInstance(rfp, RawFileParameter)
        self.assertEqual("result3", rfp.get_name())
        self.assertEqual("srtm_39_04_c", rfp.get_publish_layer_name())
        self.assertEqual("WPS Resource Binary Stream", rfp.get_description())
        self.assertEqual("This Is A GeoTIFF Layer", rfp.get_title())
        self.assertEqual("", rfp.get_metadata().strip(" "))
        # self.assertIsNone(rfp.get_output_mime_type())
        self.assertEqual("raster", rfp.get_publish_default_style())
        self.assertTrue(rfp.is_publish_as_layer())
        self.assertEqual("image/geotiff;stream", rfp.get_type())
        self.assertEqual("it.geosolutions", rfp.get_publish_target_workspace())
        self.assertIn(rfp.as_json_string(), self.result3_DLR[0][1])
        self.assertEqual('./src/wpsremote/xmpp_data/test/test_file', rfp.get_value())

    def test_application_x_netcdf_output_type_from_ini(self):
        ini_text = '''[Output4]
        name = result4
        type = application/x-netcdf
        description = NetCDF Binary File
        title = Wind
        backup_on_wps_execution_shared_dir = true
        publish_as_layer = true
        publish_default_style = raster
        publish_target_workspace = it.geosolutions
        publish_layer_name = wind
        filepath = ./src/wpsremote/xmpp_data/test/test_file
        '''
        config = ConfigParser.ConfigParser()
        ini_file = mockutils.FileLikeObjectMock(ini_text)
        config.readfp(ini_file)
        output_section = config.items('Output4')
        op = OutputParameters.create_from_config({'Output4': output_section})
        self.assertEqual(self.result4_DLR, op.as_DLR_protocol())
        self.assertEqual(['./src/wpsremote/xmpp_data/test/test_file'], op.get_values())
        # RawFileParameter
        rfp = op._params['result4']
        self.assertIsInstance(rfp, RawFileParameter)
        self.assertEqual("result4", rfp.get_name())
        self.assertEqual("wind", rfp.get_publish_layer_name())
        self.assertEqual("NetCDF Binary File", rfp.get_description())
        self.assertEqual("Wind", rfp.get_title())
        self.assertEqual("", rfp.get_metadata().strip(" "))
        # self.assertIsNone(rfp.get_output_mime_type())
        self.assertEqual("raster", rfp.get_publish_default_style())
        self.assertTrue(rfp.is_publish_as_layer())
        self.assertEqual("application/x-netcdf", rfp.get_type())
        self.assertEqual("it.geosolutions", rfp.get_publish_target_workspace())
        self.assertIn(rfp.as_json_string(), self.result4_DLR[0][1])
        self.assertEqual('./src/wpsremote/xmpp_data/test/test_file', rfp.get_value())

    def test_text_xml_output_type_from_ini(self):
        ini_text = '''[Output5]
        name = result5
        type = text/xml;subtype=gml/3.1.1
        description = WPS Resource GML
        filepath = ./src/wpsremote/xmpp_data/test/test_file
        '''
        config = ConfigParser.ConfigParser()
        ini_file = mockutils.FileLikeObjectMock(ini_text)
        config.readfp(ini_file)
        output_section = config.items('Output5')
        op = OutputParameters.create_from_config({'Output5': output_section})
        self.assertEqual(self.result5_DLR, op.as_DLR_protocol())
        self.assertEqual(['./src/wpsremote/xmpp_data/test/test_file'], op.get_values())
        # RawFileParameter
        rfp = op._params['result5']
        self.assertIsInstance(rfp, RawFileParameter)
        self.assertEqual("result5", rfp.get_name())
        self.assertIsNone(rfp.get_publish_layer_name())
        self.assertEqual("WPS Resource GML", rfp.get_description())
        self.assertIsNone(rfp.get_title())
        self.assertIsNone(rfp.get_publish_default_style())
        self.assertFalse(rfp.is_publish_as_layer())
        self.assertEqual("text/xml;subtype=gml/3.1.1", rfp.get_type())
        self.assertIsNone(rfp.get_publish_target_workspace())
        self.assertEqual("", rfp.get_metadata().strip(" "))
        self.assertIn(rfp.as_json_string(), self.result5_DLR[0][1])
        self.assertEqual('./src/wpsremote/xmpp_data/test/test_file', rfp.get_value())

    def test_video_mp4_output_type_from_ini(self):
        ini_text = '''[Output6]
        name = result6
        type = video/mp4
        description = Video MP4 Binary File
        title = Wind
        backup_on_wps_execution_shared_dir = false
        filepath = ./src/wpsremote/xmpp_data/test/test_file
        '''
        config = ConfigParser.ConfigParser()
        ini_file = mockutils.FileLikeObjectMock(ini_text)
        config.readfp(ini_file)
        output_section = config.items('Output6')
        op = OutputParameters.create_from_config({'Output6': output_section})
        self.assertEqual(self.result6_DLR, op.as_DLR_protocol())
        self.assertEqual(['./src/wpsremote/xmpp_data/test/test_file'], op.get_values())
        # RawFileParameter
        rfp = op._params['result6']
        self.assertIsInstance(rfp, RawFileParameter)
        self.assertEqual("result6", rfp.get_name())
        self.assertEqual("Video MP4 Binary File", rfp.get_description())
        self.assertEqual("Wind", rfp.get_title())
        self.assertEqual("video/mp4", rfp.get_type())
        self.assertIsNone(rfp.get_publish_layer_name())
        self.assertIsNone(rfp.get_publish_target_workspace())
        self.assertIsNone(rfp.get_publish_default_style())
        self.assertFalse(rfp.is_publish_as_layer())
        self.assertEqual("", rfp.get_metadata().strip(" "))
        self.assertIn(rfp.as_json_string(), self.result6_DLR[0][1])
        self.assertEqual('./src/wpsremote/xmpp_data/test/test_file', rfp.get_value())

    def test_application_owc_output_type_from_ini(self):
        ini_text = '''[Output7]
        name = result7
        type = application/owc
        description = WPS OWC Json MapContext
        publish_as_layer = true
        publish_layer_name = owc_json_ctx
        filepath = ./src/wpsremote/xmpp_data/test/test_file
        '''
        config = ConfigParser.ConfigParser()
        ini_file = mockutils.FileLikeObjectMock(ini_text)
        config.readfp(ini_file)
        output_section = config.items('Output7')
        op = OutputParameters.create_from_config({'Output7': output_section})
        self.assertEqual(self.result7_DLR, op.as_DLR_protocol())
        self.assertEqual([''], op.get_values())
        # OWCFileParameter
        owcfp = op._params['result7']
        self.assertIsInstance(owcfp, OWCFileParameter)
        self.assertEqual("result7", owcfp.get_name())
        self.assertEqual("WPS OWC Json MapContext", owcfp.get_description())
        self.assertIsNone(owcfp.get_title())
        self.assertEqual("application/owc", owcfp.get_type())
        self.assertEqual("owc_json_ctx", owcfp.get_publish_layer_name())
        self.assertEqual("", owcfp.get_publish_target_workspace().strip(" "))
        self.assertEqual("", owcfp.get_publish_default_style().strip(" "))
        self.assertTrue(owcfp.is_publish_as_layer())
        self.assertEqual("", owcfp.get_metadata().strip(" "))
        self.assertIn(owcfp.as_json_string(), self.result7_DLR[0][1])
        self.assertEqual('', owcfp.get_value())

    def test_string_output_type(self):
        ofp = OutputFileParameter(
            "result1",
            {
                "type": "string",
                "description": "WPS Resource Plain Text",
                "filepath": "./src/wpsremote/xmpp_data/test/test_file"
            }
        )
        self.assertEqual("WPS Resource Plain Text", ofp.get_description())
        self.assertEqual("", ofp.get_metadata().strip(" "))
        self.assertEqual("result1", ofp.get_name())
        # print ofp.get_output_mime_type()
        self.assertIsNone(ofp.get_publish_default_style())
        self.assertIsNone(ofp.get_publish_layer_name())
        self.assertIsNone(ofp.get_publish_target_workspace())
        self.assertIsNone(ofp.get_title())
        self.assertEqual("textual", ofp.get_type())
        self.assertIn(ofp.as_json_string(), self.result1_DLR[0][1])
        self.assertFalse(ofp.is_publish_as_layer())
        self.assertEqual('test content', ofp.get_value())

    def test_image_geotiff_output_type(self):
        rfp = RawFileParameter(
            "result2",
            {
                "type": "image/geotiff",
                "description": "WPS Resource Binary File",
                "filepath": "./src/wpsremote/xmpp_data/test/test_file",
                "backup_on_wps_execution_shared_dir": "true",
                "publish_as_layer": "true",
                "publish_default_style": "raster",
                "publish_target_workspace": "it.geosolutions",
                "publish_layer_name": "srtm_39_04_c"
            }
        )
        self.assertEqual("result2", rfp.get_name())
        self.assertEqual("srtm_39_04_c", rfp.get_publish_layer_name())
        self.assertEqual("WPS Resource Binary File", rfp.get_description())
        self.assertIsNone(rfp.get_title())
        self.assertEqual("", rfp.get_metadata().strip(" "))
        # self.assertIsNone(rfp.get_output_mime_type())
        self.assertEqual("raster", rfp.get_publish_default_style())
        self.assertTrue(rfp.is_publish_as_layer())
        self.assertEqual("image/geotiff", rfp.get_type())
        self.assertEqual("it.geosolutions", rfp.get_publish_target_workspace())
        self.assertIn(rfp.as_json_string(), self.result2_DLR[0][1])
        self.assertEqual('./src/wpsremote/xmpp_data/test/test_file', rfp.get_value())

    def test_image_geotiff_stream_output_type(self):
        rfp = RawFileParameter(
            "result3",
            {
                "type": "image/geotiff;stream",
                "description": "WPS Resource Binary Stream",
                "filepath": "./src/wpsremote/xmpp_data/test/test_file",
                "title": "This Is A GeoTIFF Layer",
                "publish_as_layer": "true",
                "publish_default_style": "raster",
                "publish_target_workspace": "it.geosolutions",
                "publish_layer_name": "srtm_39_04_c"
            }
        )
        self.assertEqual("result3", rfp.get_name())
        self.assertEqual("srtm_39_04_c", rfp.get_publish_layer_name())
        self.assertEqual("WPS Resource Binary Stream", rfp.get_description())
        self.assertEqual("This Is A GeoTIFF Layer", rfp.get_title())
        self.assertEqual("", rfp.get_metadata().strip(" "))
        # self.assertIsNone(rfp.get_output_mime_type())
        self.assertEqual("raster", rfp.get_publish_default_style())
        self.assertTrue(rfp.is_publish_as_layer())
        self.assertEqual("image/geotiff;stream", rfp.get_type())
        self.assertEqual("it.geosolutions", rfp.get_publish_target_workspace())
        self.assertIn(rfp.as_json_string(), self.result3_DLR[0][1])
        self.assertEqual('./src/wpsremote/xmpp_data/test/test_file', rfp.get_value())

    def test_application_x_netcdf_output_type(self):
        rfp = RawFileParameter(
            "result4",
            {
                "type": "application/x-netcdf",
                "description": "NetCDF Binary File",
                "filepath": "./src/wpsremote/xmpp_data/test/test_file",
                "title": "Wind",
                "publish_as_layer": "true",
                "publish_default_style": "raster",
                "publish_target_workspace": "it.geosolutions",
                "publish_layer_name": "wind"
            }
        )
        self.assertEqual("result4", rfp.get_name())
        self.assertEqual("wind", rfp.get_publish_layer_name())
        self.assertEqual("NetCDF Binary File", rfp.get_description())
        self.assertEqual("Wind", rfp.get_title())
        self.assertEqual("", rfp.get_metadata().strip(" "))
        # self.assertIsNone(rfp.get_output_mime_type())
        self.assertEqual("raster", rfp.get_publish_default_style())
        self.assertTrue(rfp.is_publish_as_layer())
        self.assertEqual("application/x-netcdf", rfp.get_type())
        self.assertEqual("it.geosolutions", rfp.get_publish_target_workspace())
        self.assertIn(rfp.as_json_string(), self.result4_DLR[0][1])
        self.assertEqual('./src/wpsremote/xmpp_data/test/test_file', rfp.get_value())

    def test_text_xml_output_type(self):
        rfp = RawFileParameter(
            "result5",
            {
                "type": "text/xml;subtype=gml/3.1.1",
                "description": "WPS Resource GML",
                "filepath": "./src/wpsremote/xmpp_data/test/test_file"
            }
        )
        self.assertEqual("result5", rfp.get_name())
        self.assertIsNone(rfp.get_publish_layer_name())
        self.assertEqual("WPS Resource GML", rfp.get_description())
        self.assertIsNone(rfp.get_title())
        self.assertIsNone(rfp.get_publish_default_style())
        self.assertFalse(rfp.is_publish_as_layer())
        self.assertEqual("text/xml;subtype=gml/3.1.1", rfp.get_type())
        self.assertIsNone(rfp.get_publish_target_workspace())
        self.assertEqual("", rfp.get_metadata().strip(" "))
        self.assertIn(rfp.as_json_string(), self.result5_DLR[0][1])
        self.assertEqual('./src/wpsremote/xmpp_data/test/test_file', rfp.get_value())

    def test_video_mp4_output_type(self):
        rfp = RawFileParameter(
            "result6",
            {
                "type": "video/mp4",
                "description": "Video MP4 Binary File",
                "filepath": "./src/wpsremote/xmpp_data/test/test_file",
                "title": "Wind",
                "backup_on_wps_execution_shared_dir": "false"
            }
        )
        self.assertEqual("result6", rfp.get_name())
        self.assertEqual("Video MP4 Binary File", rfp.get_description())
        self.assertEqual("Wind", rfp.get_title())
        self.assertEqual("video/mp4", rfp.get_type())
        self.assertIsNone(rfp.get_publish_layer_name())
        self.assertIsNone(rfp.get_publish_target_workspace())
        self.assertIsNone(rfp.get_publish_default_style())
        self.assertFalse(rfp.is_publish_as_layer())
        self.assertEqual("", rfp.get_metadata().strip(" "))
        self.assertIn(rfp.as_json_string(), self.result6_DLR[0][1])
        self.assertEqual('./src/wpsremote/xmpp_data/test/test_file', rfp.get_value())

    def test_application_owc_output_type(self):
        owcfp = OWCFileParameter(
            "result7",
            {
                "type": "application/owc",
                "description": "WPS OWC Json MapContext",
                "filepath": "./src/wpsremote/xmpp_data/test/test_file",
                "publish_as_layer": "true",
                "publish_layer_name": "owc_json_ctx"
            },
            {
                "result7": {
                    "type": "application/owc",
                    "description": "WPS OWC Json MapContext",
                    "filepath": "./src/wpsremote/xmpp_data/test/test_file",
                    "publish_as_layer": "true",
                    "publish_layer_name": "owc_json_ctx"
                }
            }
        )
        self.assertEqual("result7", owcfp.get_name())
        self.assertEqual("WPS OWC Json MapContext", owcfp.get_description())
        self.assertIsNone(owcfp.get_title())
        self.assertEqual("application/owc", owcfp.get_type())
        self.assertEqual("owc_json_ctx", owcfp.get_publish_layer_name())
        self.assertEqual("", owcfp.get_publish_target_workspace().strip(" "))
        self.assertEqual("", owcfp.get_publish_default_style().strip(" "))
        self.assertTrue(owcfp.is_publish_as_layer())
        self.assertEqual("", owcfp.get_metadata().strip(" "))
        self.assertIn(owcfp.as_json_string(), self.result7_DLR[0][1])
        self.assertEqual('', owcfp.get_value())


if __name__ == '__main__':
    unittest.main()
