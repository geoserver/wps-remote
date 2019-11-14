import unittest
import subprocess
import os
import time
import ast
import requests
from requests.auth import HTTPBasicAuth
import zipfile
import StringIO
import xml.etree.ElementTree as ET

WPSREMOTE_SOURCE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../src/wpsremote")
)
GEOSERVER_HOST = os.getenv("GEOSERVER_HOST", "localhost")
GEOSERVER_PORT = os.getenv("GEOSERVER_PORT", "8080")
GEOSERVER_URL = "http://{}:{}/geoserver".format(
    GEOSERVER_HOST, GEOSERVER_PORT
)
OWS_URL = "/".join([GEOSERVER_URL, "ows"])
WORKSPACE = "geosolutions"
CHECK_LAYERS_URL = "/".join([GEOSERVER_URL, "rest/layers"])
CHECK_WORKSPACE_URL = "/".join([GEOSERVER_URL, "rest/workspaces"])
CHECK_NAMESPACES_URL = "/".join([GEOSERVER_URL, "rest/namespaces"])
CHECK_DATASTORES_URL = "/".join([
    GEOSERVER_URL,
    "rest/workspaces",
    WORKSPACE,
    "datastores"
])
PARAMS = {
    "strict": "true"
}
HEADERS = {
    "Content-Type": "application/xml"
}
SYNC_XML_DATA = """<?xml version="1.0" encoding="UTF-8"?>
<wps:Execute version="1.0.0" service="WPS"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.opengis.net/wps/1.0.0"
    xmlns:wfs="http://www.opengis.net/wfs"
    xmlns:wps="http://www.opengis.net/wps/1.0.0"
    xmlns:ows="http://www.opengis.net/ows/1.1"
    xmlns:gml="http://www.opengis.net/gml"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:wcs="http://www.opengis.net/wcs/1.1.1"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsAll.xsd">
    <ows:Identifier>default:GdalContour</ows:Identifier>
    <wps:DataInputs>
    <wps:Input>
    <ows:Identifier>{input_id}</ows:Identifier>
    <wps:Data>
    <wps:ComplexData mimeType="application/octet-stream">{input_data}</wps:ComplexData>
    </wps:Data>
    </wps:Input>
    </wps:DataInputs>
    <wps:ResponseForm>
    <wps:RawDataOutput mimeType="application/octet-stream">
    <ows:Identifier>{result}</ows:Identifier>
    </wps:RawDataOutput>
    </wps:ResponseForm>
</wps:Execute>""".format(
    result="result1",
    input_id="interval",
    input_data="<![CDATA[150]]>"
)

ASYNC_XML_DATA = """<?xml version="1.0" encoding="UTF-8"?>
<wps:Execute version="1.0.0" service="WPS"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xmlns="http://www.opengis.net/wps/1.0.0"
    xmlns:wfs="http://www.opengis.net/wfs"
    xmlns:wps="http://www.opengis.net/wps/1.0.0"
    xmlns:ows="http://www.opengis.net/ows/1.1"
    xmlns:gml="http://www.opengis.net/gml"
    xmlns:ogc="http://www.opengis.net/ogc"
    xmlns:wcs="http://www.opengis.net/wcs/1.1.1"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xsi:schemaLocation="http://www.opengis.net/wps/1.0.0 http://schemas.opengis.net/wps/1.0.0/wpsAll.xsd">
    <ows:Identifier>default:GdalContour</ows:Identifier>
    <wps:DataInputs>
    <wps:Input>
    <ows:Identifier>{input_id}</ows:Identifier>
    <wps:Data>
    <wps:ComplexData mimeType="application/octet-stream">{input_data}</wps:ComplexData>
    </wps:Data>
    </wps:Input>
    </wps:DataInputs>
    <wps:ResponseForm>
    <wps:ResponseDocument storeExecuteResponse="true" status="true" lineage="false">
    <wps:Output asReference="true">
    <ows:Identifier>{result}</ows:Identifier>
    </wps:Output>
    </wps:ResponseDocument>
    </wps:ResponseForm>
</wps:Execute>""".format(
    result="result1",
    input_id="interval",
    input_data="<![CDATA[150]]>"
)


class TestWpsOperations(unittest.TestCase):

    def setUp(self):
        os.chdir(WPSREMOTE_SOURCE_PATH)
        self.command = "python wpsagent.py %s %s %s" % (
            "-r ./xmpp_data/configs/remote.config",
            "-s ./xmpp_data/configs/myservice/service.config",
            "service"
        )

    def test_async_gdal_contour(self):
        # run_threads.sh
        subprocess.Popen(
            args=self.command.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        time.sleep(10)
        r = requests.post(
            url=OWS_URL,
            params=PARAMS,
            data=ASYNC_XML_DATA,
            headers=HEADERS,
            auth=HTTPBasicAuth("admin", "geoserver")
        )
        self.assertEqual(r.status_code, 200)
        resp_xml = ET.fromstring(r.text)
        if "statusLocation" not in resp_xml.attrib:
            self.fail("No status location attribute in geoserver response: {}".format(resp_xml))
        else:
            status_url = resp_xml.attrib["statusLocation"]
            while True:
                status_resp = requests.post(status_url)
                status_resp_xml = ET.fromstring(status_resp.text)
                # Errors
                if "ExceptionReport" in str(status_resp_xml.tag):
                    subprocess.call("./kill_threads.sh", shell=True)
                    self.fail(status_resp_xml[0][0].text)
                    break
                else:
                    try:
                        # if no "percentCompleted" attribute is available the following line raise exception
                        # so we consider an error in the response
                        status = status_resp_xml[1][0].attrib["percentCompleted"]
                        print status
                        # Completed
                        if int(status) == 100:
                            break
                    except Exception:
                        subprocess.call("./kill_threads.sh", shell=True)
                        self.fail("Error in geoserver response\nRequest: {}\nResponse: {}".format(
                            status_url, status_resp.text
                        ))
                    time.sleep(5)
        subprocess.call("./kill_threads.sh", shell=True)
        # TODO: retrieve execution id/store and do assertions
        # Check publication on Geoserver through geoserver REST api
        #     check_layers = requests.get(
        #         CHECK_LAYERS_URL,
        #         auth=HTTPBasicAuth("admin", "geoserver")
        #     )
        #     layers_dict = ast.literal_eval(check_layers.text)
        #     self.assertTrue(len(filter(
        #         lambda l: "geosolutions:contour_%s" % layer_id in l["name"],
        #         layers_dict["layers"]["layer"])) > 0
        #     )
        #     check_workspaces = requests.get(
        #         CHECK_WORKSPACE_URL,
        #         auth=HTTPBasicAuth("admin", "geoserver")
        #     )
        #     workspaces_dict = ast.literal_eval(check_workspaces.text)
        #     self.assertTrue(len(filter(
        #         lambda w: "geosolutions" in w["name"],
        #         workspaces_dict["workspaces"]["workspace"])) > 0
        #     )
        #     check_namespaces = requests.get(
        #         CHECK_NAMESPACES_URL,
        #         auth=HTTPBasicAuth("admin", "geoserver")
        #     )
        #     namespaces_dict = ast.literal_eval(check_namespaces.text)
        #     self.assertTrue(len(filter(
        #         lambda n: "geosolutions" in n["name"],
        #         namespaces_dict["namespaces"]["namespace"])) > 0
        #     )
        #     check_datastores = requests.get(
        #         CHECK_DATASTORES_URL,
        #         auth=HTTPBasicAuth("admin", "geoserver")
        #     )
        #     datastores_dict = ast.literal_eval(check_datastores.text)
        #     self.assertTrue(len(filter(
        #         lambda d: store in d["name"],
        #         datastores_dict["dataStores"]["dataStore"])) > 0
        #     )
        #     # Check file in /tmp
        #     self.assertTrue(os.path.exists("/tmp/%s" % layer_id))
        #     self.assertTrue(os.path.exists("/tmp/%s/contour" % layer_id))
        #     self.assertTrue(os.path.isfile("/tmp/%s/contour.zip" % layer_id))
        #     self.assertTrue(os.path.isfile("/tmp/%s/%s.dbf" % (layer_id, store)))
        #     self.assertTrue(os.path.isfile("/tmp/%s/%s.shp" % (layer_id, store)))
        #     self.assertTrue(os.path.isfile("/tmp/%s/%s.shx" % (layer_id, store)))
        #     self.assertTrue(os.path.isfile("/tmp/%s/%s.prj" % (layer_id, store)))

    def test_sync_gdal_contour(self):
        # run_threads.sh
        subprocess.Popen(
            args=self.command.split(),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        )
        time.sleep(10)
        r = requests.post(
            url=OWS_URL,
            params=PARAMS,
            data=SYNC_XML_DATA,
            headers=HEADERS,
            auth=HTTPBasicAuth("admin", "geoserver")
        )
        self.assertEqual(r.status_code, 200)
        # Check file in response
        file = StringIO.StringIO(r.content)
        self.assertTrue(zipfile.is_zipfile(file))
        z = zipfile.ZipFile(file)
        self.assertIsNone(z.testzip())
        for info in z.infolist():
            self.assertIn(info.filename[-4:], [".dbf", ".shp", ".shx", ".prj"])
            self.assertIn("contour", info.filename)
        path_split = info.filename.split("/")
        layer_id = path_split[1]
        store = path_split[2][:-4]
        subprocess.call("./kill_threads.sh", shell=True)
        # Check publication on Geoserver through geoserver REST api
        check_layers = requests.get(
            CHECK_LAYERS_URL,
            auth=HTTPBasicAuth("admin", "geoserver")
        )
        layers_dict = ast.literal_eval(check_layers.text)
        self.assertTrue(len(filter(
            lambda l: "geosolutions:contour_%s" % layer_id in l["name"],
            layers_dict["layers"]["layer"])) > 0
        )
        check_workspaces = requests.get(
            CHECK_WORKSPACE_URL,
            auth=HTTPBasicAuth("admin", "geoserver")
        )
        workspaces_dict = ast.literal_eval(check_workspaces.text)
        self.assertTrue(len(filter(
            lambda w: "geosolutions" in w["name"],
            workspaces_dict["workspaces"]["workspace"])) > 0
        )
        check_namespaces = requests.get(
            CHECK_NAMESPACES_URL,
            auth=HTTPBasicAuth("admin", "geoserver")
        )
        namespaces_dict = ast.literal_eval(check_namespaces.text)
        self.assertTrue(len(filter(
            lambda n: "geosolutions" in n["name"],
            namespaces_dict["namespaces"]["namespace"])) > 0
        )
        check_datastores = requests.get(
            CHECK_DATASTORES_URL,
            auth=HTTPBasicAuth("admin", "geoserver")
        )
        datastores_dict = ast.literal_eval(check_datastores.text)
        self.assertTrue(len(filter(
            lambda d: store in d["name"],
            datastores_dict["dataStores"]["dataStore"])) > 0
        )
        # Check file in /tmp
        self.assertTrue(os.path.exists("/tmp/%s" % layer_id))
        self.assertTrue(os.path.exists("/tmp/%s/contour" % layer_id))
        self.assertTrue(os.path.isfile("/tmp/%s/contour.zip" % layer_id))
        self.assertTrue(os.path.isfile("/tmp/%s/%s.dbf" % (layer_id, store)))
        self.assertTrue(os.path.isfile("/tmp/%s/%s.shp" % (layer_id, store)))
        self.assertTrue(os.path.isfile("/tmp/%s/%s.shx" % (layer_id, store)))
        self.assertTrue(os.path.isfile("/tmp/%s/%s.prj" % (layer_id, store)))


if __name__ == "__main__":
    unittest.main()
