#!/usr/bin/env python
# Copyright 2018 Initios Desarrollos
#
# All rights reserved

import os

import setuptools

base_dir = os.path.dirname(__file__)

about = {}

with open(os.path.join(base_dir, 'src', 'aeat', '__about__.py')) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, 'README.rst')) as f:
    long_description = f.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# https://packaging.python.org/tutorials/distributing-packages/

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],

    description=about['__summary__'],
    long_description=long_description,
    license=about['__license__'],
    url=about['__uri__'],

    author=about['__author__'],
    author_email=about['__email__'],

    python_requires='>=3.4,<3.7',

    install_requires=[
        'lxml>=4.1.1,<4.2.0',
        'xmlsec>=1.3.3,<1.4.0',
        'zeep>=2.4.0,<2.5.0',
    ],

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
    ],

    packages=['aeat', 'aeat.rest_framework'],
    package_dir={'': 'src'},
)
