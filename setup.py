#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    "matplotlib",
    "qtpy",
    "six",
]

test_requirements = [
    "nose",
    "coverage",
]

packages = find_packages()

setup(
    name='xrayspectrumanalyzergui',
    version='0.2.0',
    description="GUI for the x-ray spectrum analyzer project",
    long_description=readme + '\n\n' + history,
    author="Hendrix Demers",
    author_email='hendrix.demers@mail.mcgill.ca',
    url='https://github.com/drix00/xrayspectrumanalyzergui',
    packages=packages,
    package_dir={'xrayspectrumanalyzergui':
                 'xrayspectrumanalyzergui'},
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3",
    zip_safe=False,
    keywords='xrayspectrumanalyzergui',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
