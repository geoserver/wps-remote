[![Build Status](https://travis-ci.org/geoserver/wps-remote.svg?branch=master)](https://travis-ci.org/geoserver/wps-remote)
[![Coverage Status](https://coveralls.io/repos/github/geoserver/wps-remote/badge.svg?branch=master)](https://coveralls.io/github/geoserver/wps-remote?branch=master)

RemoteWPS
=========

[RemoteWPS] is an open source software written in Python part of the GeoServer (http://geoserver.org) 
project that allows users to publish their executables as GeoServer WPS Processes through the XMPP protocol.

RemoteWPS is meant to be used along with the GeoServer "wps-remote" plugin for the WPS
(https://github.com/geoserver/geoserver/tree/master/src/community/wps-remote).

Being a community-driven project, RemoteWPS is developed, tested, and supported by a diverse group of 
individuals and organizations from around the world.

## License

RemoteWPS licensed under the [GPL](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

## Using

You can install the "wps-remote" Python package by using the PyPi distribution ::

    pip install wps-remote==2.14.1

Please refer to the [user guide](http://docs.geoserver.org/latest/en/user/community/remote-wps/index.html) for detailed 
information on how to install and use RemoteWPS.

## API Reference Doc

http://docs.geoserver.org/latest/en/user/community/remote-wps/install_python.html#annex-a-remote-wps-python-wrapper-reference

## Bugs

Through GeoServer JIRA.

GeoServer uses [JIRA](https://osgeo-org.atlassian.net/projects/GEOS), hosted by 
[Atlassian](https://www.atlassian.com/), for issue tracking.

## Mailing Lists

Through GeoServer Mailing Lists.

The [mailing list page](http://geoserver.org/comm/) on the GeoServer web site provides
access to the various mailing list, as well as some indication of the [code of conduct](http://geoserver.org/comm/userlist-guidelines.html) when posting to the lists

## Contributing

Through GeoServer Process.

Please read [the contribution guidelines](https://github.com/geoserver/geoserver/blob/master/CONTRIBUTING.md) before contributing pull requests to the GeoServer project.

## More Information

Visit the [website](http://geoserver.org/) or read the [docs](http://docs.geoserver.org/). 

Change Log
==========
2.14.1 [2018-09-14 11:48:37] (aligned with GeoServer Remote WPS Plugin - 2.14.x)
 - Fixes: inputs and outputs mime-types declaration on service.config
 - Cleanup: removing non source code stuff
 - Resilience: resource_monitoring now skips non-python/readable processes without dying
 - Resilience: processbot identifies relative paths for executable commands

2.12.0 [2017-07-03 12:13:10] (aligned with GeoServer Remote WPS Plugin - 2.12.x)
 - Fix for: Inputs application/json mapping error
 - Fix for: Inputs application/vnd.geo+json support
 - Fix for: Date input / output parsing
 - Fix for: JSON ID error
 - Improved robustness of wps agent
 - Allowed "-" in string input parameters
 - Fix for: Catch resource clean exception
 - Fix for: Input / output parameters are not sorted according to the process definition

2.11.2 [2017-02-16 10:12:23]
 - SFTP/FTP pluggable uploaders support
 - Minor refactoring and code cleanup

2.9.3 [2016-03-31 17:24:47]
 - Added "processbot" XMPP connection checks
 - Added "servicebot" check "processbot" status error and send error message impersonating the underlying process
 - Added "NetCDF Output" example on service.config

2.9.2 [2016-03-17 17:33:19]
 - Added "process_blacklist" property to "service.config" file
 - Added "proc_is_running(self, proc_names)" to "ResourceMonitor(threading.Thread)" background thread
 
2.9.1 [2016-03-16 11:09:56]
 - Added "GetLoadAverageMessage" XMPP message for resource monitoring
 - Added "ResourceMonitor(threading.Thread)" background thread collecting resource consuption data
 - On GeoServer side the "remoteConfig.properties" file on GEOSERVER_DATA must be updated with the properties
   xmpp_cpu_perc_threshold = 80.0
   xmpp_mem_perc_threshold = 80.0
