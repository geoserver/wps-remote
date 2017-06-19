# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import logging.config
import logging
import argparse
import sys 
import thread
import path
import traceback

import servicebot
import processbot
import configInstance
import busIndipendentMessages
import resource_cleaner

#-p d:\users\cimino\appdata\local\temp\wps_params_wprbze.tmp process
#-r .\\configs\\remote.config -s .\\configs\\RiskMaps\\service.config -p d:\\users\\cimino\\appdata\\local\\temp\\wps_params_q_245x.tmp process
#-r .\configs\remote.config -s .\configs\RiskMaps\service.config service
#-r .\configs\remote.config -s .\configs\OAAonDemand\service.config service
#-r .\configs\remote.config -s .\configs\OAAonDemand\service.config -p d:\users\cimino\appdata\local\temp\wps_params_ullgiw.tmp process

class WPSAgent(object):
    def __init__(self, args):
        #remove sleek xmpp logging 
        self.verbose = False
        self.args=args

    def find_logger_property_file(self, find_logger_property_file_path):
        if self.args.logconf == None:
            logger_properties_file = find_logger_property_file_path / "logger.properties"
        else:
            logger_properties_file = self.args.logconf
        return logger_properties_file
    
    @staticmethod
    def log_bootstrap_error( msg, stack_trace):
        sys.stderr.write(msg + "\n")
        sys.stderr.write(stack_trace + "\n")

    @staticmethod
    def set_resource_cleaner_parameters(pid_files_dir,process_time_threshold, workdir_time_threshold, sleep_time_seconds):
        resource_cleaner.Resource.pid_files_dir = pid_files_dir
        resource_cleaner.Resource.process_time_threshold = process_time_threshold
        resource_cleaner.Resource.workdir_time_threshold = workdir_time_threshold
        resource_cleaner.Resource.sleep_time_seconds = sleep_time_seconds

    @staticmethod
    def create_logger( logger_config_file, workdir, verbose):
        defaults={}
        if workdir != None:
            defaults['workdir'] = workdir
            #to avoid problems with escape sequence (\ab is apparently a valid hex number?!?!?), use always linux style path separator
            if '\\' in defaults['workdir']:
                defaults['workdir']=defaults['workdir'].replace('\\', '/')

        logging.config.fileConfig(str(logger_config_file),  defaults=defaults)

        logger = logging.getLogger("main.create_logger")
        if not verbose:
            #drop logs from sleekxmlpp
            for h in logger.root.handlers:
                h.addFilter(SleekXMPPLoggerFilter())

        logger.debug("Logger initialized with file " + str(logger_config_file))

    def create_bot(self):
        #template method
        pass

    def run(self):
        #we now have a logger
        logger = logging.getLogger("WPSAgent.run")
        try:
            bot = self.create_bot()
            logger.info("Start bot execution")
            bot.run()
        except Exception as e:
            msg = "Bot failure due to: " + str(e)
            logger.fatal(msg)
            logger.fatal( traceback.format_exc() )
            bot.send_error_message( msg )
            bot.disconnect()
            logger.fatal( "Exit Bot process with code " + str(101) )
            sys.exit(101)

class WPSAgentProcess(WPSAgent):
    """This script starts when the user call a new WPS execution. 
        His task is to call the proper external executable/scripts according to the service.config file (option -s in command line) and send back to the WPS logging and progress 
        information and error information if something unexpected happens.
        All the output including the log file is generated in a sand box directory created with joint information from service.config and external process start-up information.
        """
    def __init__(self, args):
        super(WPSAgentProcess, self).__init__(args)
        try:
            config_dir_service = path.path(args.serviceconfig).dirname()
            #deserilize pickled object with process startup info to get the unique_id to create the sand box work dir for the process execution
            self.exe_msg = busIndipendentMessages.ExecuteMessage.deserialize( args.params )
             
            #read the service config file with interpolation=true (raw=False) to get the proper sand box work dir using the unique id as input parameter
            #args.remoteconfig, args.serviceconfig
            serviceConfig = configInstance.create(args.serviceconfig , case_sensitive=True, variables = {'unique_exe_id' : self.exe_msg.UniqueId()}, raw=False) 
            work_dir = serviceConfig.get_path("DEFAULT", "workdir")

            #ensure outdir exists
            if not work_dir.exists():
                work_dir.mkdir()

            #now i can create a logger with output log file in the sandbox dir
            WPSAgent.create_logger( self.find_logger_property_file(config_dir_service), work_dir, self.verbose)

        except Exception as e:
            #here log is not available use log_bootstrap_error func to log somewhere else (e.g. operating system error log, tmp file, stdout)
            msg = "Failure during bot bootstrap due to : " + str(e)
            WPSAgent.log_bootstrap_error(msg, traceback.format_exc())
            sys.exit(100)
        
        #start execution
        self.run()

    def create_bot(self):
        try:
            logger = logging.getLogger("WPSAgentProcess.create_bot")
            logger.info("Create process bot")
            bot =  processbot.ProcessBot( self.args.remoteconfig, self.args.serviceconfig,  self.exe_msg )
            #create resource cleaner
            self.set_resource_cleaner_parameters(bot.get_resource_file_dir(), bot.max_execution_time(), bot.max_execution_time(), bot.max_execution_time())
            return bot
        except Exception as e:
            msg = "Failure during bot bootstrap due to : " + str(e)
            WPSAgent.log_bootstrap_error(msg, traceback.format_exc())
            sys.exit(100)

class WPSAgentService(WPSAgent):

    def __init__(self, args):
        try:
            super(WPSAgentService, self).__init__(args)
            remote_config_dir = path.path(args.remoteconfig).dirname()
            self.create_logger(self.find_logger_property_file( remote_config_dir ), None, self.verbose)
        except Exception as e:
            #here log is not available use log_bootstrap_error func to log somewhere else (e.g. operating system error log, tmp file, stdout)
            msg = "Failure during bot bootstrap due to : " + str(e)
            WPSAgent.log_bootstrap_error(msg, traceback.format_exc())
            sys.exit(100)

        #start execution
        self.run()

    def create_bot(self):
        try:
            logger = logging.getLogger("WPSAgentService.create_bot")
            logger.info("Create process bot")
            bot = servicebot.ServiceBot(self.args.remoteconfig, self.args.serviceconfig)
            logger.info("Create resource cleaner")
            WPSAgent.set_resource_cleaner_parameters(bot.get_resource_file_dir(), bot.max_execution_time(), bot.max_execution_time(), bot.max_execution_time())
            #start infinite loop for resource clenaer thread
            thread.start_new_thread( resource_cleaner.Resource.clean_up_all,())
            return bot
        except Exception as e:
            msg = "Failure during bot bootstrap due to : " + str(e)
            WPSAgent.log_bootstrap_error(msg, traceback.format_exc())
            sys.exit(100)

class SleekXMPPLoggerFilter(logging.Filter):

    def filter(self, record):
        return not 'sleekxmpp' in record.name 

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--remoteconfig", nargs='?', default="remote.config", help="Config file containing connection information on the calling agent (e.g. XMPP server)")
    parser.add_argument("-s", "--serviceconfig",nargs='?', default="service.config", help="Config file containing information concerning the local process to be invoked by WPS")
    parser.add_argument("-l", "--logconf", nargs="?", default=None, help="Logger config file if not provided logger.conf in remoteconfig directory (runtype=service) or logger.conf in serviceconfig directory (runtype=process) will be used")
    parser.add_argument("-p", "--params", nargs="?", help="JSON file containing input parameters")
    parser.add_argument("-e", "--executionid", nargs="?", help="Unique execution id")
    parser.add_argument("runtype", help="Run type [service|process])") #, choices=['service', 'process'])
    cmdargs = parser.parse_args()

    if cmdargs.runtype=='service':
        WPSAgentService(cmdargs)
    else: #process
        WPSAgentProcess(cmdargs)
