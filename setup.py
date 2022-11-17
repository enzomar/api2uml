# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='api2uml',
    version='0.0.1',
    description='',
    long_description=readme,
    author='',
    author_email='',
    license=license,
    packages=find_packages()
)