# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Ned Batchelder"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

"""
FtpUpload

Upload files via FTP based on their content changing.

Based on original code by
   Ned Batchelder
   http://www.nedbatchelder.com
   version = '1.0a'

Modified by
   Alessio Fabiani, GeoSolutions S.A.S.
"""

import ftplib, pickle, sys, md5, os, string
import logging      # if not std, http://www.red-dove.com/python_logging.html
import path         # http://www.jorendorff.com/articles/python/path
import upload


class EzFtp:
    """
    A simplified interface to ftplib.

    Lets you use full pathnames, with server-side
    directory management handled automatically.
    """
    def __init__(self, ftp):
        self.ftp = ftp
        self.serverDir = ''

    def setRoot(self, dir):
        """
        Set the remote directory that we'll call the root.
        """
        self.cd(dir, create=True)
        self.ftp.cwd("..")
        self.ftp.cwd(dir)

    def cd(self, dir, create=1):
        """
        Change the directory on the server, if need be.
        If create is true, directories are created if necessary to get to the full path.
        Returns true if the directory is changed.
        """
        if dir != self.serverDir:
            # Move up to the common root.
            while not dir.startswith(self.serverDir):
                logging.info("ftpcd ..")
                self.ftp.cwd("..")
                self.serverDir = os.path.split(self.serverDir)[0]
            # Move down to the right directory
            doDirs = dir[len(self.serverDir):]
            for d in string.split(doDirs, os.sep):
                if d:
                    try:
                        logging.info("ftpcd %s" % d)
                        self.ftp.cwd(d)
                    except:
                        if create:
                            logging.info("ftpmkdir %s" % d)
                            self.ftp.mkd(d)
                            self.ftp.cwd(d)
                        else:
                            return 0
                    self.serverDir = os.path.join(self.serverDir, d)
        return 1

    def putasc(self, this, that):
        """
        Put a text file to the server.
        """
        thatDir, thatFile = os.path.split(that)
        self.cd(thatDir)
        f = open(this, "r")
        logging.info("ftpstorasc %s" % that)
        try:
            self.ftp.storlines("STOR %s" % (thatFile),f)
        except Exception, e:
            logging.exception(e)
            raise

    def putbin(self, this, that):
        """
        Put a binary file to the server.
        """
        thatDir, thatFile = os.path.split(that)
        self.cd(thatDir)
        f = open(this, "rb")
        logging.info("ftpstorbin %s" % that)
        try:
            self.ftp.storbinary("STOR %s" % (thatFile), f, 1024)
        except Exception, e:
            logging.exception(e)
            raise

    def delete(self, that):
        """
        Delete a file on the server.
        """
        thatDir, thatFile = os.path.split(that)
        if self.cd(thatDir, 0):
            logging.info("ftpdel %s" % that)
            try:
                self.ftp.delete(thatFile)
            except:
                pass

    def quit(self):
        """
        Quit.
        """
        self.ftp.quit()


class FtpUpload(upload.Upload):
    """
    Provides intelligent FTP uploading of files, using MD5 hashes to track
    which files have to be uploaded.  Each upload is recorded in a local
    file so that the next upload can skip the file if its contents haven't
    changed.  File timestamps are ignored, allowing regenerated files to
    be properly uploaded only if their contents have changed.

    Call `setHost` and `setMd5File` to establish the settings for a session,
    then `upload` for each set of files to upload.  If you want to have
    removed local files automatically delete the remote files, call
    `deleteOldFiles` once, then `finish` to perform the closing bookkeeping.

    ::

        fu = FtpUpload(config, 'ftp.myhost.com', 'myusername', 'password')
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
            self.ftp = ftplib.FTP()
            self.ftp.set_debuglevel(3)
            if portstr:
                port = int(portstr)
                self.ftp.connect(hoststr, port)
            else:
                self.ftp.connect(hoststr, 21)
            self.ftp.login(username, password)
            self.ftp.set_pasv(1)

    def setMd5File(self, md5file):
        """
        Assign a filename to use for the MD5 tracking.
        """
        self.md5file = md5file
        if self.md5file:
            try:
                inf = open(self.md5file, "r")
                self.md5DictIn = pickle.load(inf)
                self.md5DictUp.update(self.md5DictIn)
                inf.close()
            except IOError:
                self.md5DictIn = {}

    def Upload(self,
               hostdir='.',
               text='*.*',
               binary='',
               src='.'
               ):
        """
        Upload a set of files.
        Source files are found in the directory named by `src`
        (and its subdirectories recursively).  The files are uploaded
        to the directory named by `hostdir` on the remote host.
        Files that match one of the space-separated patterns in `text`
        are uploaded as text files, those that match the patterns in
        `binary` are uploaded as binary files.

        This method can be called a number of times to upload different
        sets of files to or from different directories within the same
        FtpUpload session.
        """

        if not self.ezftp:
            if not self.ftp:
                self.setHost(self.host, self.username, self.password)
            self.ezftp = EzFtp(self.ftp)

        if hostdir != '.':
            self.ezftp.setRoot('/')
            self.ezftp.setRoot(hostdir)

        # patdict is a dict of fnmatch patterns to ftp function.
        patdict = {}
        for pat in text.split():
            patdict[pat] = self.ezftp.putasc
        for pat in binary.split():
            patdict[pat] = self.ezftp.putbin

        # Walk the tree, putting files to the ezftp.
        srcpath = path.path(src)
        for thispath in srcpath.walkfiles():
            thatpath = hostdir + os.sep + srcpath.relpathto(thispath)
            logging.info("thatpath %s" % thatpath)
            thatpathstr = str(thatpath)
            # Compute this file's MD5 fingerprint
            m = md5.new()
            f = open(thispath, "rb")
            for l in f.readlines():
                m.update(l)
            thisMd5 = m.hexdigest()

            # What was the last MD5 fingerprint?
            thatMd5 = self.md5DictIn.get(thatpathstr, '')

            # If the current file is different, then put it to the server.
            if thisMd5 != thatMd5:
                # Find the pattern the file matches, and use the ftp function
                # from the map.
                for pat in patdict.keys():
                    if thispath.fnmatch(pat):
                        ftpfn = patdict[pat]
                        ftpfn(thispath, thatpath)

            # Remember the new fingerprint.
            self.md5DictOut[thatpathstr] = thisMd5
            self.md5DictUp[thatpathstr] = thisMd5

    def deleteOldFiles(self):
        """
        Delete any remote files that we have uploaded previously but
        that weren't considered in this FtpUpload session.  This doesn't
        touch files that exist on the remote host but were never uploaded
        by this module.
        """

        # Files in md5DictIn but not in md5DictOut must have been removed.
        for this in self.md5DictIn:
            if this not in self.md5DictOut:
                self.ezftp.delete(this)
                del self.md5DictUp[this]

    def finish(self):
        """
        Do our final bookkeeping.
        """
        # Done with ftp'ing.
        self.ezftp.quit()

        # Write the md5 control file out for next time.
        if self.md5file:
            outf = open(self.md5file, "w")
            pickle.dump(self.md5DictUp, outf)
            outf.close()

