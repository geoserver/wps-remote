# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

import configInstance
import os
import path
import unittest
import datetime
import ConfigParser
import psutil
import json
import time
import logging
import traceback

class Resource(object):
    """
    Identify a process generated by a remote WPS call.
    Every processbot (aka request handler) create a resource file in pid_files_dir once started. 
    The method Resource.cleanup() looks fore pending resource files and if found might decide to kill process id found inside the file.
    """
    sleep_time_seconds = 3600
    process_time_threshold = None
    workdir_time_threshold = None
    pid_files_dir = None #dir where file for each resource is stored
    
    @staticmethod
    def get_pid_files_dir():
        return Resource.pid_files_dir if isinstance(Resource.pid_files_dir, path.path) else path.path(Resource.pid_files_dir)

    @staticmethod
    def clean_up_all():
        """Checks all resource files .pid and execute clean up"""
        logger = logging.getLogger("Resource.clean_up_all")
        logger.info("start resource cleaner main loop")
        while True:
            Resource.clean_up_iteration()

    @staticmethod
    def clean_up_iteration():
        logger = logging.getLogger("Resource.clean_up")
        logger.debug("Sleep for " +  str(Resource.sleep_time_seconds.total_seconds()) + " seconds")
        time.sleep(Resource.sleep_time_seconds.total_seconds())
        logger.debug("look for resources to clean up")
        Resource.pid_files_dir = Resource.get_pid_files_dir()
        for f in Resource.pid_files_dir.listdir("*.pid"):
            logger.debug("found resource file " + str(f))
            r = Resource()
            r.read_from_file(f)
            r.clean_up()

    @staticmethod
    def create_from_file(unique_id, process_bot_pid=None):
        r = Resource()
        if process_bot_pid ==  None:
            r.set_processbot_pid(os.getpid()) 
        else:
            r.set_processbot_pid(process_bot_pid) 
        r.set_unique_id(unique_id) 
        r.read()
        return r

    def __init__(self):
        self._start_time = None #process start time
        self._processbot_cmd_line = None #processbot (aka request handler) cmd line
        self._unique_id = None #processbot (aka request handler) unique execution id (used to crate sand box dir)
        self._sandbox_path = None #processbot (aka request handler) sandbox path
        self._processbot_pid = None #processbot (aka request handler) Process id
        self._spawned_process_pids = None #processbot (aka request handler) spawned processes ids
        self._spawned_process_cmd = None #processbot (aka request handler) spawned processes cmd lines
        self._path =  Resource.get_pid_files_dir() #dir where file for each resource is stored

    def start_time(self):
        return self._start_time

    def start_time_as_str(self):
        return self._start_time.strftime("%Y-%m-%dT%H:%M:%S")

    def cmd_line(self):
        return self._processbot_cmd_line

    def unique_id(self):
        return self._unique_id 

    def set_unique_id(self, unique_id):
        self._unique_id = unique_id

    def sendbox_path(self):
        return self._sandbox_path

    def processbot_pid(self):
        return self._processbot_pid

    def set_processbot_pid(self, pid):
        self._processbot_pid = pid

    def spawned_process_pids(self):
        return self._spawned_process_pids 

    def spawned_process_cmd(self):
        return self._spawned_process_cmd

    def set_from_servicebot(self, unique_id, sendbox_path):
        self._start_time = self.now() 
        self._unique_id = unique_id
        self._sandbox_path = sendbox_path
    
    def set_from_processbot(self, processbot_pid, spawned_process_pids):
        """create the resource except for the information realted to the processbot spawned processes"""
        #if not processbot_pid in psutil.pids():
        if not psutil.pid_exists(processbot_pid):
            raise Exception("cannot find process bot pid + " + str(processbot_pid))
        proc = psutil.Process( processbot_pid )
        try:
            self._processbot_cmd_line = ' '.join(proc.cmdline())
        except:
            self._processbot_cmd_line = ' '.join(proc.cmdline)
        self._processbot_pid = processbot_pid

        """add the processbot spawned processes pids and cmdline to the resource"""
        self._spawned_process_pids=spawned_process_pids
        self._spawned_process_cmd = []
        removed=[]
        for pid in self._spawned_process_pids:
            #if pid is dead remove it from the list
            #if not pid in psutil.pids():
            if not psutil.pid_exists(pid):
                removed.append( pid )
            else:
                try:
                    #here pid *should* exists, however get cmd line in try, except block
                    proc = psutil.Process( pid )
                    try:
                        self._spawned_process_cmd.append( ' '.join(proc.cmdline()) )
                    except:
                        self._spawned_process_cmd.append( ' '.join(proc.cmdline) )
                except:
                    removed.append( pid )
        self._spawned_process_pids = list(set(self._spawned_process_pids) - set(removed))

    def now(self):
        return datetime.datetime.now()

    def filepath(self):
        #return self._path / str(self._processbot_pid) + "__" + str(self._unique_id) + ".pid"
        return self._path / str(self._unique_id) + ".pid"

    def read(self):
        if self.filepath().exists():
            self.read_from_file(  self.filepath() )

    def read_from_file(self, filepath):
        config = configInstance.create( filepath, raw= True) #todo: use file lock
        self._start_time = config.get("DEFAULT", "start_time")
        try: 
            self._start_time = datetime.datetime.strptime( self._start_time, "%Y-%m-%dT%H:%M:%S" )
        except:
            self._start_time = datetime.datetime.strptime( "2000-01-01T00:00:00", "%Y-%m-%dT%H:%M:%S" )

        self._processbot_cmd_line = config.get("DEFAULT", "cmd_line")
        if self._processbot_cmd_line != None and self._processbot_cmd_line !='':
            self._processbot_cmd_line = json.loads(self._processbot_cmd_line)

        self._unique_id = config.get("DEFAULT", "unique_id")
        self._sandbox_path = config.get_path("DEFAULT", "sendbox_path")
        try:
            self._processbot_pid = config.getint("DEFAULT", "processbot_pid")
        except ValueError:
            self._processbot_pid = config.get("DEFAULT", "processbot_pid")

        self._spawned_process_pids = config.get("DEFAULT", "spawned_process_pids")
        if self._spawned_process_pids != None and self._spawned_process_pids !='':
            self._spawned_process_pids = json.loads( self._spawned_process_pids )
        
        self._spawned_process_cmd = config.get("DEFAULT", "spawned_process_cmd")
        if self._spawned_process_cmd != None and self._spawned_process_cmd !='':
            self._spawned_process_cmd = json.loads(self._spawned_process_cmd)
    
    def write(self):
        if self.filepath().exists():
            self.filepath().remove()
        
        config = ConfigParser.ConfigParser()

        config.set("DEFAULT", "start_time",  self.start_time_as_str() if self._start_time != None else "") 
        config.set("DEFAULT", "unique_id", self._unique_id )
        config.set("DEFAULT", "sendbox_path", str(self._sandbox_path) )

        if self._processbot_pid != None:
            config.set("DEFAULT", "processbot_pid", str(self._processbot_pid) ) 
        else:
            config.set("DEFAULT", "processbot_pid", "" ) 

        if self._processbot_cmd_line != None:
            config.set("DEFAULT", "cmd_line", json.dumps(self._processbot_cmd_line) ) 
        else:
            config.set("DEFAULT", "cmd_line", "" ) 

        if self._spawned_process_pids != None:
            config.set("DEFAULT", "spawned_process_pids", json.dumps(self._spawned_process_pids) ) 
        else:
            config.set("DEFAULT", "spawned_process_pids", "" ) 

        if self._spawned_process_cmd != None:
            config.set("DEFAULT", "spawned_process_cmd", json.dumps(self._spawned_process_cmd) ) 
        else:
            config.set("DEFAULT", "spawned_process_cmd", "" ) 

        fp = self.filepath().open('wb') #todo: use file lock
        config.write(fp)
        fp.close()

    def kill_spawned_process(self):
        """kill all spawned process generated bby processbot"""
        res = []
        logger = logging.getLogger("Resource.kill_spawned_process")
        logger.info("Try to kill computational job process(es)")
        for p,c in zip(self._spawned_process_pids, self._spawned_process_cmd):
            res.append ( self.kill_process(p, c) )
        res = list(set(res))
        return len(res)==0 or (len(res)==1 and res[0]) #all success

    def kill_processbot(self):
        return self.kill_process(self._processbot_pid, self._processbot_cmd_line)

    def kill_process(self, pid, cmd_line):
        logger = logging.getLogger("Resource.kill_process")
        logger.info("request for killing process " + str(pid))
        #if pid in psutil.pids():
        if psutil.pid_exists(pid):
            logger.info("process " + str(pid) + " exists try to kill...")
            proc = psutil.Process( pid )
            if proc.cmdline() == cmd_line:
                try:
                    proc.kill()
                    logger.info("process " + str(pid) + " killed")
                    return True
                except Exception as ex:
                    logger.warning("Failure in killing process " + str(pid) + " due to: " + str(ex))
                    logger.debug( traceback.format_exc() )
                    return False
            else:
                logger.info("pid " + str(pid) + " found but with wrong command line. Assuming resource was already correcly cleaned-up")
            return True
        else:
            logger.warning("pid " + str(pid) + " doesn't exist")
            return True

    def delete_sandbox_dir(self):
        logger = logging.getLogger("Resource.delete_sandbox_dir")
        if self._sandbox_path.exists():
            logger.info("try to delete directory " + str(self._sandbox_path))
            try:
                self._sandbox_path.rmtree()
                logger.info("Directory " + str(self._sandbox_path) + " correctly deleted")
                return True
            except Exception as ex:
                logger.warning("Failure in deleting directory " + str(self._sandbox_path) + " due to: " + str(ex))
                logger.debug( traceback.format_exc() )
                return False

        else:
            logger.debug("Directory " + str(self._sandbox_path) + " doesn't exist, nothing to delete")
            return True

    def clean_up(self):
        logger = logging.getLogger("Resource.clean_up")
        now = self.now() 
        dt = now - self._start_time 
        if dt > Resource.process_time_threshold:
            logger.info("start to clean up resource: " + str(self) )    
            res=[]
            res.append( self.kill_spawned_process() )
            res.append( self.kill_processbot() )
            res.append( self.delete_sandbox_dir() )
            
            logger.debug( "kill computational job, kill request handler process,  delete sandbox dir = " + str(res))
            res = list(set(res))
            if (len(res)==1 and res[0]): #all success
                logger.info("all pending resource have been deallocated, remove resource file " + str(self.filepath()))
                self.filepath().remove()
            else:
                logger.info("Cannot deallocate all pending resource, do not remove resource file " + str(self.filepath()))
        else:
            logger.debug(str(self) + " is "+str(dt.total_seconds()) +" seconds old and it is not yet ready to be cleaned up, wait for next round")    

    def __str__(self):
        return "process " + str(self._processbot_pid) + " working on " + str(self._sandbox_path) + " from " + self.start_time_as_str()

class Test(unittest.TestCase):

    def test_workflow(self):
        
        import subprocess
        import random
        sendbox_root = path.path(".\\")

        Resource.sleep_time_seconds = datetime.timedelta( seconds=5)
        Resource.process_time_threshold = datetime.timedelta( seconds=1)
        Resource.workdir_time_threshold = datetime.timedelta( seconds=1)
        Resource.pid_files_dir = path.path(".\\")

        #srv bot
        #create process bot
        cmd = 'python -c "import time; time.sleep(80000)"'
        invoked_process = subprocess.Popen(args=cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        prcbot_pid = invoked_process.pid
        unique_id = str(random.randint(1, 1000)).zfill(5)
        sendbox_path =  sendbox_root / str(unique_id)

        r = Resource()
        r.set_from_servicebot(unique_id, sendbox_path)
        r.write()

        #proc bot
        #create computation job
        comp_job = subprocess.Popen(args=cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        #add the pid of the computational job to the resource file
        rc = Resource.create_from_file(unique_id, prcbot_pid)
        rc.set_from_processbot( prcbot_pid, [ comp_job.pid ] ) 
        rc.write()

        #resource cleaner, should run in separate thread
        Resource.clean_up_iteration()

        self.assertFalse( r.filepath().exists() )

if __name__ == '__main__':
    unittest.main()
