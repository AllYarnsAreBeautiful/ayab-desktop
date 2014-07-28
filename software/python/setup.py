#!/usr/bin/python2
# -*- coding: utf-8 -*-
#This file is part of AYAB.
#
#    AYAB is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    AYAB is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with AYAB.  If not, see <http://www.gnu.org/licenses/>.
#
#    Copyright 2014 Sebastian Oliva, Christian Obersteiner, Andreas Müller,
#    https://bitbucket.org/chris007de/ayab-apparat/

from __future__ import print_function
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import ayab

here = os.path.abspath(os.path.dirname(__file__))

## Useful Docs
## https://wiki.python.org/moin/Distutils/Tutorial
## https://pythonhosted.org/setuptools/setuptools.html

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

def read_requirements(file_name):
    file_ob = file(file_name)
    raw_requirements_list = file_ob.readlines()
    requirements_list = []
    for line in requirements_list:
      l = line.strip(' \t\n\r')
      if not l.startswith("#"):
        requirements_list.append(l)
    return requirements_list

## This builds the long description from Readme file, should be rst.
long_description = read('README.md') #, 'CHANGES.txt')


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='ayab',
    version=ayab.__version__,
    url='http://ayab-knitting.com/',
    license='GNU GPLv3+',
    author=u'Christian Obersteiner, Andreas Müller, Sebastian Oliva',
    scripts=['bin/ayab'],
    tests_require=['pytest'],
    install_requires=[read_requirements("requirements.txt")],
    cmdclass={'test': PyTest},
    author_email='info@ayab-knitting.com',
    description='GUI for Machine assisted Knitting. Reference implementation for AYAB.',
    long_description=long_description,
    ## TODO: load plugins automatically.
    packages=['ayab',
              'ayab.plugins',
              'ayab.plugins.ayab_plugin',
              'ayab.plugins.dummy_knitting_plugin',],
    include_package_data=True,
    platforms='any',
    # test_suite='ayab.tests',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        ],
    extras_require={'testing': ['pytest']}
)
