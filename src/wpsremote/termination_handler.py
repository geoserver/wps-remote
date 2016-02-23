# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import SocketServer
import socket
import threading
import path 
import os
import thread
import datetime

class  TerminationHandler(object):
    def __init__(self, handler):
        self._handler = handler

        HOST, PORT = "localhost", 0

        setattr(ThreadedTCPRequestHandler, '_handle', handler)

        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        self.ip, self.port = server.server_address
        self._write_pid_file()
        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

    def _write_pid_file(self):
        pid = os.getpid()
        workdir = path.path("d:\\tmp\\wpsproc\\")
        pidfile = workdir / path.path(str(pid) +  ".pid")

        if pidfile.exists():
            pidfile.remove()

        pidfile.write_lines( ['cmdline=', 'pid='+str(pid), 'start_time=' + str(datetime.datetime.now()), 'tcp_port=' + str(self.port) ] )


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    
    def handle(self):
        data = self.request.recv(1024)

        #if (data=="kill"):
        cur_thread = threading.current_thread()
        response = "{}: {}".format( cur_thread.name, self._handle() )
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def clean_up1(threadedTCPRequestHandler):
    return "clean_up1"

def clean_up2(threadedTCPRequestHandler):
    return "clean_up2"


def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))

    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()

# #############################################################

class WatchDog(object):
    """
        run as service every 15 minutes

        #iterate over pids of all process bots
        for pid in path.path("d:\\tmp\\wpsproc\\").files(): #[1.pid, 2.pid,] 
            read file:
                cmdline=...
                pid=...
                start_time=...
                tcp port=...

            if pid is running and cmdline is ok and time is expired:
                #kill
                open socket(port)
                write "kill" to socket

                
            elif pids is not running:
                del "/var/proc/wpsproc/<pid>.pid

           
    """
    pass

# #############################################################

if __name__ == '__main__':
    # Port 0 means to select an arbitrary unused port

    th =TerminationHandler(clean_up1)


    client(th.ip, th.port, "Hello World 1")
    client(th.ip, th.port, "Hello World 2")
    client(th.ip, th.port, "Hello World 3")

    #server.shutdown()

    #th.set_handler(clean_up2)