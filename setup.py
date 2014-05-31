#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess
import jiracards

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    subprocess.call(['python', 'setup.py', 'sdist', 'upload', '--sign'])
    sys.exit()

README = open('README.md').read()
LICENSE = open("LICENSE").read()

setup(
    name='jira-cards',
    version=jiracards.__version__,
    description='Jira-Cards prints agile cards for your physical board from a JIRA board or issues.',
    long_description=(README),
    author='Sebastian Ruml',
    author_email='sebastian@sebastianruml.com',
    url='https://github.com/hypebeast/jira-cards',
    include_package_data=True,
    install_requires=[
        'cement >= 2.2.2',
        'requests >= 2.3.0',
        'jinja2 >= 2.7.2'
    ],
    license=(LICENSE),
    keywords='python, jira, cards, card, agile, scrum, print, issue, issues, board',
    packages=['jiracards'],
    scripts=['bin/jira-cards']
)
