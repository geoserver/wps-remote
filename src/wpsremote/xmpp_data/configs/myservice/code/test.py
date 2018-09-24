# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import subprocess
import logging.config
import logging
import argparse
import sys
import thread
import traceback
import logging
import sys
import os
import uuid
import zipfile

# constants
#id = os.urandom(10)
id = str(uuid.uuid4())
gdalContour = r'/usr/bin/gdal_contour'
dst = r'contour_'+id[:13]
src = '%s/../../../resource_dir/srtm_39_04/srtm_39_04_c.tif' % os.path.dirname(os.path.abspath(__file__))
trg = '%s/../../../output/%s.shp' % (os.path.dirname(os.path.abspath(__file__)), dst)
cmd = '-a elev'  # just for example!
interval = '-i'

class GDALTest(object):
    def __init__(self, args):
        self.args=args
        self.create_logger("logger_test.properties")
        self.logger.info("ProgressInfo:0.0%")


    def run(self):
        #fullCmd = ' '.join([gdalContour, cmd, self.youCanQuoteMe(src), self.youCanQuoteMe(dst), interval, self.args.interval])
        fullCmd = ' '.join([gdalContour, cmd, src, trg, interval, self.args.interval])
        self.logger.debug("Running command > " + fullCmd)
        proc=subprocess.Popen(fullCmd.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
        for line in proc.stdout:
            self.logger.info(line)

        #call communicate to retrieve return code of subprocess
        proc.communicate()
        ret = proc.returncode

        if (ret == 0):
            # zipf = zipfile.ZipFile(self.args.workdir+'/contour.zip', 'w')
            # self.zipdir(self.args.workdir+'/', zipf)
            output_dir = '%s/../../../output/%s' % (os.path.dirname(os.path.abspath(__file__)), self.args.execution_id)
            zipf = zipfile.ZipFile(output_dir+'/contour.zip', 'w')
            self.zipdir(output_dir+'/', zipf)
            zipf.close()

            self.logger.info("ProgressInfo:100%")
        else:
            self.logger.critical("Error occurred during processing.")

        return ret
    # see note below
    def youCanQuoteMe(self, item):
        return "\"" + item + "\""

    def zipdir(self, path, zip):
        for root, dirs, files in os.walk(path):
            files = [ fi for fi in files if fi.startswith(dst) ]
            for file in files:
                zip.write(os.path.join(root, file))

    def create_logger(self, logger_config_file):
        defaults={}

        logging.config.fileConfig(str(logger_config_file),  defaults=defaults)

        self.logger = logging.getLogger("main.create_logger")

        self.logger.debug("Logger initialized with file " + str(logger_config_file))

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", nargs='?', default="10", help="Elevation interval between contours.")
    parser.add_argument("-w", "--workdir", nargs='?', default="", help="Remote process sandbox working directory.")
    parser.add_argument("-e", "--execution_id", nargs='?', default="", help="Remote process Unique Execution Id.")
    cmdargs = parser.parse_args()

    gdalTest = GDALTest(cmdargs)
    return_code = gdalTest.run()
    sys.exit(return_code)
