# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

# import time
import psutil
import logging
import threading

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

logger = logging.getLogger("servicebot.resource_monitor")


class ProcessWeight(object):

    weight = 0
    coefficient = 1.0

    def __init__(self, process_weight):
        if process_weight:
            self.weight = float(process_weight['weight'])
            self.coefficient = float(process_weight['coefficient'])

    # ability to customize process load on per request basis
    def request_weight(self, exec_request):
        # this one is the default implementation
        return (self.coefficient * self.weight)


class ResourceMonitor(threading.Thread):

    # Total Capacity of this machine
    capacity = 100

    # Current load
    load = 0
    proc_load = 0
    resource_load = 0
    running_procs_load = {}

    load_threshold = 95
    load_average_scan_minutes = 15

    try:
        cores = psutil.cpu_count()
    except BaseException:
        cores = 1
    cpu_perc = []
    vmem_perc = []

    lock = threading.Lock()

    def __init__(self, capacity, load_threshold, load_average_scan_minutes):
        threading.Thread.__init__(self)

        ResourceMonitor.capacity = capacity
        ResourceMonitor.load_threshold = load_threshold
        ResourceMonitor.load_average_scan_minutes = load_average_scan_minutes

        ResourceMonitor.lock.acquire()

        ResourceMonitor.vmem_perc.append(psutil.virtual_memory().percent)
        ResourceMonitor.vmem_perc.append(psutil.virtual_memory().percent)

        ResourceMonitor.cpu_perc.append(psutil.cpu_percent(interval=0, percpu=False))
        ResourceMonitor.cpu_perc.append(psutil.cpu_percent(interval=0, percpu=False))

        ResourceMonitor.lock.release()

    def proc_is_running(self, proc_defs):
        for proc in psutil.process_iter():
            try:
                process = psutil.Process(proc.pid)  # Get the process info using PID
                if process.is_running():
                    pid = str(process.pid)  # noqa
                    ppid = str(process.ppid)  # noqa
                    status = process.status()  # noqa

                    cpu_percent = process.cpu_percent()  # noqa
                    mem_percent = process.memory_percent()  # noqa

                    rss = str(process.memory_info().rss)  # noqa
                    vms = str(process.memory_info().vms)  # noqa
                    username = process.username()  # noqa
                    name = process.name()  # Here is the process name
                    path = process.cwd()  # noqa
                    cmdline = ' '.join(process.cmdline())  # noqa

                    # print("Get the process info using (path, name, cmdline): [%s / %s / %s]" % (path, name, cmdline))
                    for _p in proc_defs:
                        # logger.info("Look for process: [%s] / Status [%s]" % (_p, status.lower()))
                        # print("Look for process: [%s] / Status [%s]" % (_p, status.lower()))
                        if (status.lower() != "sleeping") and \
                            ('name' in _p and _p['name'] in name) and \
                                ('cwd' in _p and _p['cwd'] in path) and \
                                ('cmdline' in _p and _p['cmdline'] in cmdline):
                            ResourceMonitor.proc_load = 100
                            return True
            except BaseException:
                import traceback
                tb = traceback.format_exc()
                logger.debug(tb)
                # print(tb)

        ResourceMonitor.proc_load = 0
        return False

    def update_stats(self):
        try:
            # Acquiring thread lock
            ResourceMonitor.lock.acquire()

            # Used memory perc
            ResourceMonitor.vmem_perc[1] = (ResourceMonitor.vmem_perc[0] + ResourceMonitor.vmem_perc[1]) / 2.0
            ResourceMonitor.vmem_perc[0] = (ResourceMonitor.vmem_perc[1] + psutil.virtual_memory().percent) / 2.0

            # Used cpu perc
            ResourceMonitor.cpu_perc[1] = ResourceMonitor.cpu_perc[0]
            ResourceMonitor.cpu_perc[0] = psutil.cpu_percent(
                interval=(ResourceMonitor.load_average_scan_minutes*60), percpu=False)

            vmem = psutil.virtual_memory().percent
            if ResourceMonitor.vmem_perc[0] > 0:
                vmem = (vmem + ResourceMonitor.vmem_perc[0]) / 2.0

            loadavg = psutil.cpu_percent(interval=0, percpu=False)
            if ResourceMonitor.cpu_perc[0] > 0:
                loadavg = (loadavg + ResourceMonitor.cpu_perc[0]) / 2.0

            if vmem > ResourceMonitor.load_threshold or loadavg > ResourceMonitor.load_threshold:
                ResourceMonitor.resource_load = 100
            else:
                ResourceMonitor.resource_load = 0

        finally:
            # Releaseing thread lock
            ResourceMonitor.lock.release()

    def run(self):
        while True:
            self.update_stats()
