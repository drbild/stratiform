#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


install_requires = [
    'wrapt'
]

setup(
    name='stratiform',
    version='0.1.0-SNAPSHOT',
    author = "David R. Bild",
    author_email = "david@davidbild.org",
    description="Concise creation of AWS CloudFormation templates.",
    keywords = "cloudformation aws amazon template",
    url="https://github.com/drbild/stratiform",
    packages=['stratiform'],
    install_requires=install_requires,
    classifiers = [
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python'
    ]
)
