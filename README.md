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

    pip install wps-remote==2.17.0

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

## Change Log

### 2.17.0 [2019-11-11 16:08:42] (aligned with GeoServer Remote WPS Plugin - 2.17.x)
  <li> 2019-11-11: afabiani <a href="https://github.com/geoserver/wps-remote/commit/55407ace0c2136b55e2774ab3e547e535d0c97db" target="blank"> [Fixes #42] Async Request Management Proposal</a></li>
  <li> 2019-11-07: afabiani <a href="https://github.com/geoserver/wps-remote/commit/c8d3b4b8bdd7f33ec99331c89d0e822508f944fa" target="blank"> [Fixes #40] Typos on class name</a></li>
  <li> 2019-11-07: afabiani <a href="https://github.com/geoserver/wps-remote/commit/9999b4ce19d8a05ffc04d719b942f868f963cb28" target="blank">  - Minor fixes to the sample gdalContour service config</a></li>
  <li> 2019-11-05: geosolutions <a href="https://github.com/geoserver/wps-remote/commit/37edd2c439ead6bd05864ea50df389cb15228046" target="blank">  - get rid of redounant print</a></li>
  <li> 2019-11-05: gioscarda <a href="https://github.com/geoserver/wps-remote/commit/462205d40691b94d0a493cbf0fa8c1698a07c5f3" target="blank"> [Fixes #38] Added missing tests for actions and resource_cleaner</a></li>
  <li> 2019-11-05: gioscarda <a href="https://github.com/geoserver/wps-remote/commit/c96f19ff218be17e4008bae14fa85a4563ba4613" target="blank"> [Fixes #36] tests for FTP uploads</a></li>
  <li> 2019-11-04: gioscarda <a href="https://github.com/geoserver/wps-remote/commit/716a117ef5a6a55df4e9b3647e13fb8ab59830e2" target="blank"> [Fixes #34] Clean up unused files</a></li>
  <li> 2019-10-31: gioscarda <a href="https://github.com/geoserver/wps-remote/commit/59723bee62ad0c7600a69c5f73478f4edc37f27b" target="blank"> [Fixes #32] testing path</a></li>
  <li> 2019-10-31: gioscarda <a href="https://github.com/geoserver/wps-remote/commit/f811c32560d3bb4ae54bc355745d3ced6ecdddc0" target="blank"> [Fixes #30] ProcessBot and ServiceBot tests</a></li>
  <li> 2019-10-25: gioscarda <a href="https://github.com/geoserver/wps-remote/commit/d5fe88f828868ed3e9e1459fa93d37d2b83b2b17" target="blank"> [Fixes #28] Add BusIndependentMessage tests</a></li>
  <li> 2019-10-23: gioscarda <a href="https://github.com/geoserver/wps-remote/commit/3eb8b9f100b6b820d211094bd365341e164094ad" target="blank"> [Fixes #26] configparser tests</a></li>
  <li> 2019-10-23: gioscarda <a href="https://github.com/geoserver/wps-remote/commit/31fedae9cc438f12503e51d429eb1d00fa3301fb" target="blank"> [Fixes #24] computational jobs outputs tests</a></li>
  <li> 2019-10-22: afabiani <a href="https://github.com/geoserver/wps-remote/commit/288272c4f312487ccf7a8dd6f8d23e009dfc6a6e" target="blank"> fix travis build</a></li>
  <li> 2019-10-22: afabiani <a href="https://github.com/geoserver/wps-remote/commit/32983a81f0529c4ec52404a9d3a814adcf53efee" target="blank"> fix travis build</a></li>
  <li> 2019-10-22: gioscarda <a href="https://github.com/geoserver/wps-remote/commit/cc885f21b42d6ef89447845e5250828a08d524f8" target="blank"> [Fixes #10] Add missing tests about input parameters</a></li>
  <li> 2019-10-18: afabiani <a href="https://github.com/geoserver/wps-remote/commit/beac9c03ee5d240e0a8f5bc086fa569116d37b3d" target="blank"> minor formatting</a></li>
  <li> 2019-09-23: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/5fc088f2c6963830fcf5154eb40ee9920656865d" target="blank"> Travis CI: Run tests on Python 3.7 in allow_failures mode</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/5f7fc0774af8058316b46bb9d52d9a47265a063a" target="blank"> Don't cache $HOME</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/f02b01751f3f3eebd4fa78431816c2cf15ad908a" target="blank"> cache $HOME</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/02d7a945b3d3904a76b6601c44a85d04a5953941" target="blank"> Don’t cache $HOME</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/6f56c2ce0af5dc593e9bf5479d56a6e6e93b5a8e" target="blank"> Shorten a long line</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/31940142533b2ccfde5aaac905b2f6145f84d2dc" target="blank"> Flake8: ignore W504 line break after binary operator</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/1a742b334f16d5f83cfe72fce9459b07614ff31c" target="blank"> Remove unused import 'time'</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/20f8bf8e41eb163a65a6344b537c72a321836778" target="blank"> Update .travis.yml</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/c827056bd8ea0be5d1101117b62c2aa346a38402" target="blank"> python: 2.7.8       dist: precise</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/46f0526d40e1db6a0fc66e4877c9d29455a00313" target="blank"> Upgrade flake8 and allow it to specify its dependencies</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/a6a9c347c8e6b48793c8e70adf6277a452586f29" target="blank"> Update .travis.yml</a></li>
  <li> 2019-09-22: Christian Clauss <a href="https://github.com/geoserver/wps-remote/commit/ab68602b4b4d74fad8b325ff45d45011c41912d7" target="blank"> Travis-CI: The sudo: tag is deprecated in Travis</a></li>
  <li> 2019-09-20: dependabot[bot] <a href="https://github.com/geoserver/wps-remote/commit/3c5b3b36318207363e434ef0e1ede6f53cc60c1f" target="blank"> Bump paramiko from 2.4.1 to 2.4.2</a></li>
  <li> 2019-01-14: afabiani <a href="https://github.com/geoserver/wps-remote/commit/60c4ca2e2f170ebcdac7f2c270783c1d3fdd539a" target="blank">  - Resource Monitor: minor refactoring to the data collection main cycle. Trying to take into account runtime deltas.</a></li>
  <li> 2018-12-12: afabiani <a href="https://github.com/geoserver/wps-remote/commit/9abaf9ef2dc77b5a59795f011130c86a58cec8ca" target="blank">  - better management of failure states of the spawned processbot</a></li>
  <li> 2018-11-15: afabiani <a href="https://github.com/geoserver/wps-remote/commit/8436d3a05999122c1eb1c28218007ad565be0bc3" target="blank"> - preparing for test suite / introducing pep8 format checks</a></li>
  <li> 2018-11-15: afabiani <a href="https://github.com/geoserver/wps-remote/commit/c2ca09b9b939b1309d82d092bd88f7e9a2a99ec6" target="blank">  - preparing for test suite / introducing pep8 format checks</a></li>

### 2.15.0 [2018-11-15 11:48:37] (aligned with GeoServer Remote WPS Plugin - 2.15.x)
  <li> 2018-11-15: afabiani <a href="https://github.com/geoserver/wps-remote/commit/14dfecf258ce55f71aa9b34f288da80f30165bec" target="blank">  - Bump to version 2.15.0</a></li>
  <li> 2018-11-15: afabiani <a href="https://github.com/geoserver/wps-remote/commit/26f892a6b8edad6f18e3d190e4aa30c8a2cac629" target="blank">  - added a delay to the test service</a></li>
  <li> 2018-10-03: afabiani <a href="https://github.com/geoserver/wps-remote/commit/40299ef8ef1bba7c7ddebce57f214c63d39efe37" target="blank">  - Improving "resource_monitor" process is running method info</a></li>
  <li> 2018-09-28: afabiani <a href="https://github.com/geoserver/wps-remote/commit/77c27f9c65e5e0af36c447a4f1ae4724c3dcb1ef" target="blank">  - minor improvements to the test.py service (gdalContour)</a></li>
  <li> 2018-09-28: afabiani <a href="https://github.com/geoserver/wps-remote/commit/653fad367ed6018e83d60fa76e7568c1a1484cd4" target="blank"> - patch: boolean string properties checks are wrong on "output_file_parameter"</a></li>
  <li> 2018-09-27: afabiani <a href="https://github.com/geoserver/wps-remote/commit/55d55fb8554afbf4a49effe5cf90cf674baa3c5f" target="blank">  - patch: boolean string properties checks are wrong on "output_file_parameter"</a></li>
  <li> 2018-09-24: afabiani <a href="https://github.com/geoserver/wps-remote/commit/a5a7a4c436c3f62a65eb5fde891273c9fcd241ab" target="blank"> - handle "abort" message from xmppBus</a></li>
  <li> 2018-09-24: afabiani <a href="https://github.com/geoserver/wps-remote/commit/8ca369893e4361b35f2c95e464da9f0a7147dd80" target="blank">  - handle "abort" message from xmppBus</a></li>
  <li> 2018-09-14: Alessio Fabiani <a href="https://github.com/geoserver/wps-remote/commit/e0db01cb0a601d7bc80c52449384cbc3e82808be" target="blank"> Update README.md</a></li>

### 2.14.1 [2018-09-14 11:48:37] (aligned with GeoServer Remote WPS Plugin - 2.14.x)
 - Fixes: inputs and outputs mime-types declaration on service.config
 - Cleanup: removing non source code stuff
 - Resilience: resource_monitoring now skips non-python/readable processes without dying
 - Resilience: processbot identifies relative paths for executable commands
  <li> 2018-09-14: afabiani <a href="https://github.com/geoserver/wps-remote/commit/2eba26fab4f26af32825b1dccc84dfd50fb54cbb" target="blank"> - Version 2.14.1</a></li>
  <li> 2018-09-14: afabiani <a href="https://github.com/geoserver/wps-remote/commit/42a24b4d1379ba4303fa1e7438aac4a3d7a5c5ac" target="blank">  - .gitignore stuff</a></li>
  <li> 2018-09-14: afabiani <a href="https://github.com/geoserver/wps-remote/commit/283ccca70a1e7591fe07b9ac09d7f23f51661f30" target="blank"> - Version 2.14.x</a></li>

### 2.12.0 [2017-07-03 12:13:10] (aligned with GeoServer Remote WPS Plugin - 2.12.x)
 - Fix for: Inputs application/json mapping error
 - Fix for: Inputs application/vnd.geo+json support
 - Fix for: Date input / output parsing
 - Fix for: JSON ID error
 - Improved robustness of wps agent
 - Allowed "-" in string input parameters
 - Fix for: Catch resource clean exception
 - Fix for: Input / output parameters are not sorted according to the process definition
  <li> 2017-07-03: geosolutions <a href="https://github.com/geoserver/wps-remote/commit/bfa507b613f58ef81f29db116cfdf34297dd07a5" target="blank">  - Version 2.12.0</a></li>
  <li> 2017-07-03: geosolutions <a href="https://github.com/geoserver/wps-remote/commit/72ae466114ab2afdda436614420f1a5ace97e157" target="blank">  - Version 2.12.0</a></li>
  <li> 2017-07-03: geosolutions <a href="https://github.com/geoserver/wps-remote/commit/f3cf0c8935d0f9d0a743ff5fd89d9098450c52cf" target="blank">  - Version 2.12.0</a></li>
  <li> 2017-07-03: geosolutions <a href="https://github.com/geoserver/wps-remote/commit/75dd297e9c86617d9dd2889f17f9dd44fcf2a6a0" target="blank">  - Version 2.12.0</a></li>
  <li> 2017-06-28: geosolutions <a href="https://github.com/geoserver/wps-remote/commit/f9d3b57b16e7a2188a8aff52bb1f451a070f8350" target="blank">  - Make processbot more resilient to errors</a></li>
  <li> 2017-06-27: torse <a href="https://github.com/geoserver/wps-remote/commit/6d82453ba1fa9b257f1f77613be0fe3b6a1c0467" target="blank"> Make json_path_expr configuration optional</a></li>
  <li> 2017-06-26: geosolutions <a href="https://github.com/geoserver/wps-remote/commit/25b4ace2dcfca3c85d979e5bcadd42d21c96b5fd" target="blank">  - Make processbot and servicebot more resilient to errors</a></li>
  <li> 2017-06-19: geosolutions <a href="https://github.com/geoserver/wps-remote/commit/dd83b1dc5686d528f5481413cd053abb6d11703a" target="blank"> close #8 : An unhandled exception might crash wpsagent and related WPS process</a></li>
  <li> 2017-06-19: geosolutions <a href="https://github.com/geoserver/wps-remote/commit/5d81e2cbef6e7c421388a02fa528e09aa19b8057" target="blank"> close #8 : An unhandled exception might crash wpsagent and related WPS process</a></li>
  <li> 2017-06-14: torse <a href="https://github.com/geoserver/wps-remote/commit/5e2ae86380350d33babde5980efdbbd783a8c1b1" target="blank"> Fix parsing of dateTime input and format the parameter for the commandline</a></li>
  <li> 2017-06-14: torse <a href="https://github.com/geoserver/wps-remote/commit/d3deecfb4a4bfa104a7c9009dc5d7ac0e8ea1c3c" target="blank"> Catch exception in resource cleaner write function and log error</a></li>
  <li> 2017-06-14: torse <a href="https://github.com/geoserver/wps-remote/commit/43159046599f1ec8b560c1dee5d7d9fe8a6eeb6f" target="blank"> Allow '-' characters in string input parameters</a></li>

### 2.11.2 [2017-02-16 10:12:23]
 - SFTP/FTP pluggable uploaders support
 - Minor refactoring and code cleanup

### 2.9.3 [2016-03-31 17:24:47]
 - Added "processbot" XMPP connection checks
 - Added "servicebot" check "processbot" status error and send error message impersonating the underlying process
 - Added "NetCDF Output" example on service.config

### 2.9.2 [2016-03-17 17:33:19]
 - Added "process_blacklist" property to "service.config" file
 - Added "proc_is_running(self, proc_names)" to "ResourceMonitor(threading.Thread)" background thread
 
### 2.9.1 [2016-03-16 11:09:56]
 - Added "GetLoadAverageMessage" XMPP message for resource monitoring
 - Added "ResourceMonitor(threading.Thread)" background thread collecting resource consuption data
 - On GeoServer side the "remoteConfig.properties" file on GEOSERVER_DATA must be updated with the properties
   xmpp_cpu_perc_threshold = 80.0
   xmpp_mem_perc_threshold = 80.0
