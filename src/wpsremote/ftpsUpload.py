# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Ned Batchelder"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

"""
FtpsUpload

Upload files via FTPS based on their content changing.

Based on original code by
   Ned Batchelder
   http://www.nedbatchelder.com
   version = '1.0a'

Modified by
   Alessio Fabiani, GeoSolutions S.A.S.
"""

import ftpUpload
import ftplib, socket, ssl, pickle, sys, md5, os, string
import logging      # if not std, http://www.red-dove.com/python_logging.html
import path         # http://www.jorendorff.com/articles/python/path
import upload


class tyFTP(ftplib.FTP_TLS):
    def __init__(self,
                 host='',
                 user='',
                 passwd='',
                 acct='',
                 keyfile=None,
                 certfile=None,
                 timeout=60):

        ftplib.FTP_TLS.__init__(self,
                                host=host,
                                user=user,
                                passwd=passwd,
                                acct=acct,
                                keyfile=keyfile,
                                certfile=certfile,
                                timeout=timeout)

    """
     - This is for Implicit TLS
    def connect(self, host='', port=0, timeout=-999):
        ""Connect to host.  Arguments are:
         - host: hostname to connect to (string, default previous host)
         - port: port to connect to (integer, default previous port)
        ""
        if host != '':
            self.host = host
        if port > 0:
            self.port = port
        if timeout != -999:
            self.timeout = timeout
        try:
            self.sock = socket.create_connection((self.host, self.port), self.timeout)
            self.af = self.sock.family
            # add this line!!!
            self.sock = ssl.wrap_socket(self.sock,
                                        self.keyfile,
                                        self.certfile,
                                        ssl_version=ssl.PROTOCOL_TLSv1)
            # add end
            self.file = self.sock.makefile('rb')
            self.welcome = self.getresp()
        except:
            logging.exception('Got exception on "tyFTP.connect"')
            logging.info(self.ssl_version)
            raise

        return self.welcome
    """

    def storbinary(self, cmd, fp, blocksize=8192, callback=None, rest=None):
        self.voidcmd('TYPE I')
        conn = self.transfercmd(cmd, rest)
        try:
            while 1:
                buf = fp.read(blocksize)
                if not buf: break
                conn.sendall(buf)
                if callback: callback(buf)
            # shutdown ssl layer
            if isinstance(conn, ssl.SSLSocket):
                conn.unwrap()
        finally:
            conn.close()
        return self.voidresp()

    def storlines(self, cmd, fp, callback=None):
        self.voidcmd('TYPE A')
        conn = self.transfercmd(cmd)
        try:
            while 1:
                buf = fp.readline(self.maxline + 1)
                if len(buf) > self.maxline:
                    raise Error("got more than %d bytes" % self.maxline)
                if not buf: break
                if buf[-2:] != CRLF:
                    if buf[-1] in CRLF: buf = buf[:-1]
                    buf = buf + CRLF
                conn.sendall(buf)
                if callback: callback(buf)
            # shutdown ssl layer
            if isinstance(conn, ssl.SSLSocket):
                conn.unwrap()
        finally:
            conn.close()
        return self.voidresp()    


class FtpsUpload(ftpUpload.FtpUpload):
    """
    Provides intelligent FTPS uploading of files, using MD5 hashes to track
    which files have to be uploaded.  Each upload is recorded in a local
    file so that the next upload can skip the file if its contents haven't
    changed.  File timestamps are ignored, allowing regenerated files to
    be properly uploaded only if their contents have changed.

    Call `setHost` and `setMd5File` to establish the settings for a session,
    then `upload` for each set of files to upload.  If you want to have
    removed local files automatically delete the remote files, call
    `deleteOldFiles` once, then `finish` to perform the closing bookkeeping.

    ::

        fu = FtpsUpload(config, 'ftp.myhost.com', 'myusername', 'password')
        fu.setHost('ftp.myhost.com', 'myusername', 'password')
        fu.setMd5File('myhost.md5') # optional
        fu.upload(
            hostdir='www', src='.',
            text='*.html *.css', binary='*.gif *.jpg'
        )
        # more upload() calls can go here..
        fu.deleteOldFiles()
        fu.finish()

    """

    def __init__(self, host, username, password, id="master"):
        upload.Upload.__init__(self, host, username, password, id)

        self.ftp = None
        self.ezftp = None
        self.md5file = None
        self.md5DictIn = {}
        self.md5DictOut = {}
        self.md5DictUp = {}
        # self.setHost(host, username, password)

    def setHost(self, host, username, password):
        """
        Set the host, the username and password.
        """
        if not self.ftp:
            try:
                hoststr, portstr = host.split(':')
            except:
                hoststr = host
                portstr = None
            self.ftp = tyFTP(timeout=60)
            self.ftp.set_debuglevel(3)
            if portstr:
                port = int(portstr)
                self.ftp.connect(hoststr, port)
            else:
                self.ftp.connect(hoststr, 22)
            # switch to secure data connection.. IMPORTANT! Otherwise, only the user and password is encrypted and not all the file data.
            self.ftp.auth()
            self.ftp.login(username, password)
            self.ftp.prot_p()
            self.ftp.set_pasv(1)
