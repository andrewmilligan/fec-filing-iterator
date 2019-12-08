#!/usr/bin/env python

import os
import setuptools

package_name = 'fec_filing_iterator'

# Version info -- read without importing
_locals = {}
with open(os.path.join(package_name, "_version.py")) as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

packages = [
    package_name,
]

with open("README.rst") as readme:
    long_description = readme.read()

setuptools.setup(
    name=package_name,
    version=version,
    description='Utility to iterate over FEC filings through the FEC API',
    long_description=long_description,
    keywords='fec campaign finance elections',
    url='https://github.com/andrewmilligan/fec-filing-iterator',
    license='ISC',
    author='Ander Milligan',
    author_email='andrew.i.milligan@gmail.com',
    install_requires=[
        'requests>=2.19.0',
    ],
    packages=packages,
)
