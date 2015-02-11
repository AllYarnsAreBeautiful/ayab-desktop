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
import glob
import sys

try:
    import py2exe
except:
    #TODO: notify of missing functionality.
    pass

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
    for line in raw_requirements_list:
      l = line.strip(' \t\n\r')
      if not l.startswith("#"):
        requirements_list.append(l)
    return requirements_list

## This builds the long description from Readme file, should be rst.
long_description = read('README.md')  # TODO: Add 'CHANGES.txt'


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)


def find_data_files(source, target, patterns):
    """Locates the specified data-files and returns the matches
    in a data_files compatible format.

    source is the root of the source data tree.
        Use '' or '.' for current directory.
    target is the root of the target data tree.
        Use '' or '.' for the distribution directory.
    patterns is a sequence of glob-patterns for the
        files you want to copy.
    """
    if glob.has_magic(source) or glob.has_magic(target):
        raise ValueError("Magic not allowed in src, target")
    ret = {}
    for pattern in patterns:
        pattern = os.path.join(source, pattern)
        for filename in glob.glob(pattern):
            if os.path.isfile(filename):
                targetpath = os.path.join(target, os.path.relpath(filename, source))
                path = os.path.dirname(targetpath)
                ret.setdefault(path, []).append(filename)
    return sorted(ret.items())


setup(
    name='ayab',
    version=ayab.__version__,
    url='http://ayab-knitting.com/',
    license='GNU GPLv3+',
    author=u'Christian Obersteiner, Andreas Müller, Sebastian Oliva',
    scripts=['bin/ayab'],
    windows=['bin/ayab'],
    skip_archive=True,
    tests_require=['pytest'],
    options={"py2exe": {
        "includes": ["sip"],
        "skip_archive": True
        }},
    data_files=find_data_files('ayab', 'ayab', [
        'README.md',
        'patterns/*',
        '*.ts',
        '*.yapsy-plugin',
        'plugins/*',
        'plugins/ayab_plugin/firmware/*',
        'translations/*',
        ## FIXME: check alternatives for this nasty manual include
        ## http://objectmix.com/python/115674-py2exe-distutils-how-include-tree-files.html
        'plugins/ayab_plugin/firmware/hardware_test/mega2560/*',
        'plugins/ayab_plugin/firmware/hardware_test/uno/*',
        'plugins/ayab_plugin/firmware/kh910/mega2560/*',
        'plugins/ayab_plugin/firmware/kh910/uno/*',
        'plugins/ayab_plugin/firmware/kh930/mega2560/*',
        'plugins/ayab_plugin/firmware/kh930/uno/*',
        ]),
    install_requires=[read_requirements("requirements.txt")],
    cmdclass={'test': PyTest},
    author_email='info@ayab-knitting.com',
    description='GUI for Machine assisted Knitting. Reference implementation for AYAB.',
    long_description=long_description,
    ## TODO: load plugins automatically.
    packages=['ayab',
              'ayab.plugins',
              'ayab.plugins.ayab_plugin',
              'ayab.plugins.dummy_knitting_plugin', ],
    include_package_data=True,
    platforms='any',
    # test_suite='ayab.tests',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Natural Language :: English',
        ],
    extras_require={'testing': ['pytest']}
)
