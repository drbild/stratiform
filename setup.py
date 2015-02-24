#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='stratiform',
    version='0.1.0-SNAPSHOT',
    author = "David R. Bild",
    author_email = "david@davidbild.org",
    description="Concise creation of AWS CloudFormation templates.",
    keywords = "cloudformation aws amazon template",
    url="https://github.com/drbild/stratiform",
    packages=['stratiform'],
    classifiers = [
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python'
    ]
)
