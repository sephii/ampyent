#!/usr/bin/env python
from distutils.core import setup
from ampyent import __version__

setup(
    name='ampyent',
    version=__version__,
    packages=['ampyent', 'ampyent.ui'],
    description='Ambiance manager for RPG masters',
    author='Sylvain Fankhauser',
    scripts=['bin/ampyent'],
    url='https://github.com/sephii/ampyent',
    requires=['PyYAML(==3.10)', 'mplayer.py(==0.7.0)'],
)
