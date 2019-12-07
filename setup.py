#!/usr/bin/env python

import os
import setuptools

package_name = 'fec_crawler'
binary_name = 'fec-crawler'

# Set up some directories we'll need
app_dir = os.path.dirname(os.path.realpath(__file__))
package_dir = os.path.join(app_dir, package_name)
config_dir = os.path.join(package_dir, 'apps')

# Set up data files we need
package_files = []

# Version info -- read without importing
_locals = {}
with open(os.path.join(package_name, "_version.py")) as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

packages = [
    package_name,
]

sub_packages = []
packages += [f"{package_name}.{sub}" for sub in sub_packages]

setuptools.setup(
    name=package_name,
    version=version,
    description='Utility to iterate over FEC filings through the FEC API',
    url='https://github.com/andrewmilligan/fec-crawler',
    author='Ander Milligan',
    author_email='andrew.i.milligan@gmail.com',
    install_requires=[],
    packages=packages,
    package_data={'fec_crawler': package_files},
    # entry_points={
    #     "console_scripts": [
    #         "{} = {}.main:program.run".format(binary_name, package_name)
    #     ]
    # },
)
