#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('requirements.txt', 'r') as r:
    requirements = r.read().splitlines()

with open('README.md', 'r') as r:
    readme = r.read()

setup(
    name='ambiverseclient',
    version='0.1',
    author="Linus Kohl",
    author_email="linus@riskl.io",
    packages=['ambiverseclient'],
    python_requires='>=3.6',
    license='GPLv3',
    long_description=readme,
    install_requires=requirements
)
