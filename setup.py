# (c) 2016 Open Source Geospatial Foundation - all rights reserved
# (c) 2014 - 2015 Centre for Maritime Research and Experimentation (CMRE)
# (c) 2013 - 2014 German Aerospace Center (DLR)
# This code is licensed under the GPL 2.0 license, available at the root
# application directory.

"""
   To deploy a new version of the package on PyPi

   1. Update "version"
   2. Update REAMDE.md Change Log and pip install version

   3. Follow the instruction at http://peterdowns.com/posts/first-time-with-pypi.html

   4. Deploy on pypitest:

      python setup.py sdist upload -r pypitest
      python setup.py bdist --format=gztar upload -r pypitest
      python setup.py bdist_wheel upload -r pypitest

   5. Deploy on pypi:

      python setup.py sdist upload -r pypi
      python setup.py bdist --format=gztar upload -r pypi
      python setup.py bdist_wheel upload -r pypi
"""
from setuptools import setup, find_packages

try:
    readme_text = file('README.md', 'rb').read()
except IOError,e:
    readme_text = ''

setup(
    name = "wps-remote",
    version = "2.14.2",
    author = "GeoServer Developers",
    author_email = "geoserver-devel@lists.sourceforge.net",
    description = "A library that allows users to publish their executables as GeoServer WPS Processes through the XMPP protocol",
    keywords = "XMPP Beckend for GeoServer Remote WPS ProcessFactory.",
    long_description = readme_text,
    license = "GPL",
    url = "https://github.com/geoserver/wps-remote",
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    package_dir = {'':'src'},
    packages = find_packages('src'),
    package_data = {
        '': [
            'xmpp_data/*.*',
            'xmpp_data/configs/*.*',
            'xmpp_data/configs/myservice/*.*',
            'xmpp_data/configs/myservice/code/*.*',
            'xmpp_data/output/*.*',
            'xmpp_data/resource_dir/*.*',
            'xmpp_data/resource_dir/srtm_39_04/*.*',
            'xmpp_data/share/placemark',
            'xmpp_data/ssl/*.*',
            'xmpp_data/test/*.*',
        ]
    },
    include_package_data = True,
    test_suite = "test",
    install_requires = [
        "astroid==1.4.4",
        "colorama==0.3.6",
        "flake8==2.5.4",
        "functools32",
        "jsonschema==2.5.1",
        "lazy-object-proxy==1.2.1",
        "mccabe==0.4.0",
        "paramiko",
        "pep8==1.7.0",
        "psutil>=4.0.0",
        "pycrypto",
        "pyflakes==1.0.0",
        "pylint==1.5.4",
        "six==1.10.0",
        "sleekxmpp>=1.3.1",
        "wheel==0.24.0",
        "wrapt==1.10.10",
    ],
)
