#!/usr/bin/env python
from os.path import abspath, dirname, join
from setuptools import setup, find_packages

source_directory = dirname(abspath(__file__))
requirements = [l.strip() for l in open(join(source_directory, 'requirements.txt'))]

setup(
    name='checkio_task_tester',
    version='0.0.5',
    description='CheckiO common line interface for debugging missions on *.checkio.org',
    author='CheckiO',
    author_email='a.lyabah@checkio.org',
    url='https://github.com/CheckiO/checkio-task-tester',
    download_url='https://github.com/CheckiO/checkio-task-tester/tarball/0.0.5',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['cio-task-tester = checkio_task_tester.runner:main'],
    },
    install_requires=requirements,
)
