# (c) 2019 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import unittest
from wpsremote.path import path
from wpsremote.ftpUpload import EzFtp, FtpUpload
from wpsremote.sftpUpload import EzFtp as EzSFtp
from wpsremote.ftpsUpload import FtpsUpload
from mock import patch
from ftplib import FTP

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2019 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"


class TestFtpUploads(unittest.TestCase):

    @patch('ftplib.FTP', autospec=True)
    def test_EzFtp(self, mock_ftp):
        mockFTP = mock_ftp.return_value
        ezFtp = EzFtp(mockFTP)
        self.assertEqual(ezFtp.cd("test_dir"), 1)
        try:
            ezFtp.setRoot("root_dir")
            ezFtp.putasc(
                "./src/wpsremote/xmpp_data/test/test_file",
                "/tmp/test_asc"
            )
            ezFtp.putbin(
                "./src/wpsremote/xmpp_data/test/test_file",
                "/tmp/test_bin"
            )
            ezFtp.delete("/tmp/test_bin")
            ezFtp.quit()
        except Exception as e:
            self.fail(e)

    @patch('ftplib.FTP', autospec=True)
    def test_FtpUpload(self, mock_ftp):
        mockFTP = mock_ftp.return_value
        try:
            ftpUpload = FtpUpload("host", "username", "password")
            ftpUpload.ftp = mockFTP
            ftpUpload.setHost("host:port", "username", "password")
            ftpUpload.setMd5File("./src/wpsremote/xmpp_data/test/test_upload")
            ftpUpload.Upload()
            ftpUpload.deleteOldFiles()
            ftpUpload.finish()
            path("./src/wpsremote/xmpp_data/test/test_upload").remove()
        except Exception as e:
            self.fail(e)

    @patch('ftplib.FTP', autospec=FTP())
    def test_EzSFtp(self, mock_ftp):
        mockFTP = mock_ftp.return_value
        ezSFtp = EzSFtp(mockFTP)
        self.assertEqual(ezSFtp.cd("test_dir"), 1)
        try:
            ezSFtp.setRoot("root_dir")
            ezSFtp.putasc(
                "./src/wpsremote/xmpp_data/test/test_file",
                "/tmp/test_asc"
            )
            ezSFtp.putbin(
                "./src/wpsremote/xmpp_data/test/test_file",
                "/tmp/test_bin"
            )
            ezSFtp.delete("/tmp/test_bin")
            ezSFtp.quit()
        except Exception as e:
            self.fail(e)

    @patch('ftplib.FTP', autospec=True)
    def test_FtpsUpload(self, mock_ftp):
        mockFTP = mock_ftp.return_value
        try:
            ftpsUpload = FtpsUpload("host", "username", "password")
            ftpsUpload.ftp = mockFTP
            ftpsUpload.setHost("host:port", "username", "password")
        except Exception as e:
            self.fail(e)


if __name__ == '__main__':
    unittest.main()
