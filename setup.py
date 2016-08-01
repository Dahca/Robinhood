#! /usr/bin/env python
from setuptools import setup

setup(name='robinhood',
      version='1.0.0',
      description='Stock Trading API based on Robinhood',
      author='Ian Glen Neal',
      author_email='ian.gl.neal@gmail.com',
      url='https://github.com/Dahca/Robinhood/',
      packages=['robinhood', "robinhood.test"],
      test_suite="nose.collector"
)
