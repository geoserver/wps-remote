# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

class Upload(object):
    def __init__(self, host, username, password, id):
        self.callbacks={}
        self.id = id
        self.host = host
        self.username = username
        self.password = password

    def Upload(self, hostdir='.', text='*.*', binary='', src='.'):
        """
        Upload a set of files.
        Source files are found in the directory named by `src`
        (and its subdirectories recursively).  The files are uploaded
        to the directory named by `hostdir` on the remote host.
        Files that match one of the space-separated patterns in `text`
        are uploaded as text files, those that match the patterns in
        `binary` are uploaded as binary files.
        """
        pass
