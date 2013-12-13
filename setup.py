#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'mnowotka'

import sys

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='epyper',
    version='0.1.0',
    author='Michal Nowotka',
    author_email='mmmnow@gmail.com',
    description='Python driver for Embedded Artists 2.7 inch E-paper Display Module',
    url='https://github.com/mnowotka/epyper',
    license='MIT',
    packages=['epyper'],
    long_description=open('README.md').read(),
    install_requires=['wiringpi2>=1.0.10',
                      'Pillow>=2.2.1'],
    package_data={
        'epyper': ['samples/*'],
        },                  
    include_package_data=False,
    classifiers=['Development Status :: 4 - Beta',
                 "Environment :: Handhelds/PDA's",
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 2.7',
                 'Topic :: Multimedia :: Video :: Display'],
    zip_safe=False,
)
