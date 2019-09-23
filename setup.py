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
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession
from distutils.core import setup

from setuptools import find_packages

# Parse requirements.txt to get the list of dependencies
inst_req = parse_requirements('requirements.txt',
                              session=PipSession())
REQUIREMENTS = [str(r.req) for r in inst_req]

try:
    readme_text = open('README.md', 'rb').read()
except IOError as e:
    readme_text = ''

setup(
    name="wps-remote",
    version="2.15.0",
    author="GeoServer Developers",
    author_email="geoserver-devel@lists.sourceforge.net",
    description="A library that allows users to publish their executables as GeoServer WPS Processes through the XMPP protocol",  # noqa
    keywords="XMPP Beckend for GeoServer Remote WPS ProcessFactory.",
    long_description=readme_text,
    license="GPL",
    url="https://github.com/geoserver/wps-remote",
    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Environment :: Web Environment',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    package_data={
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
    include_package_data=True,
    test_suite="test",
    install_requires=REQUIREMENTS,
)
