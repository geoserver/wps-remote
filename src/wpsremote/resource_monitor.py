# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

__author__ = "Alessio Fabiani"
__copyright__ = "Copyright 2016 Open Source Geospatial Foundation - all rights reserved"
__license__ = "GPL"

import threading
import thread
import time
import psutil

class ResourceMonitor(threading.Thread):

    cores = psutil.cpu_count()
    cpu_perc = []
    vmem_perc = []
    lock = threading.Lock()
    
    def __init__(self): 
        threading.Thread.__init__(self) 
        ResourceMonitor.lock.acquire() 

        ResourceMonitor.vmem_perc.append(psutil.virtual_memory().percent)
        ResourceMonitor.vmem_perc.append(psutil.virtual_memory().percent)

        ResourceMonitor.cpu_perc.append(psutil.cpu_percent(interval = 0, percpu= False))
        ResourceMonitor.cpu_perc.append(psutil.cpu_percent(interval = 0, percpu= False))

        ResourceMonitor.lock.release() 
 
    def run(self): 
        while True: 
            ResourceMonitor.lock.acquire() 

            ResourceMonitor.vmem_perc[1] = (ResourceMonitor.vmem_perc[0] + ResourceMonitor.vmem_perc[1]) / 2.0
            ResourceMonitor.vmem_perc[0] = (ResourceMonitor.vmem_perc[1] + psutil.virtual_memory().percent) / 2.0

            ResourceMonitor.cpu_perc[1] = ResourceMonitor.cpu_perc[0]
            ResourceMonitor.cpu_perc[0] = psutil.cpu_percent(interval = (15*60), percpu= False)

            ResourceMonitor.lock.release()

