#!/usr/bin/env python
from setuptools import setup, find_packages
name = "General Tools for GNU Radio"
release = "0.0"
version = "0.0.0"
extensions = []

setup(
    name=name,
    version=version,
    description="GR General Tools",
    url="",
    author="Keith Chow",
    packages=find_packages(),
    tests_require=["pytest"],
    setup_requires=[],
    install_requires=[
        "numpy",
        "pyjnius",
        "SigMF==1.0.0"
    ],
    dependency_links=[],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'docs/source')
            }
        },
)
