#!/usr/bin/env python
import sys
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

if sys.version_info >= (3,6):
    sys.exit('Sorry, The last supported Python version is 3.5')


source_directory = dirname(abspath(__file__))
requirements = [l.strip() for l in open(join(source_directory, 'requirements.txt'))]

setup(
    name='checkio_task_tester',
    version='0.0.6',
    description='CheckiO common line interface for debugging missions on *.checkio.org',
    author='CheckiO',
    author_email='a.lyabah@checkio.org',
    url='https://github.com/CheckiO/checkio-task-tester',
    download_url='https://github.com/CheckiO/checkio-task-tester/tarball/0.0.6',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['cio-task-tester = checkio_task_tester.runner:main'],
    },
    install_requires=requirements,
)
