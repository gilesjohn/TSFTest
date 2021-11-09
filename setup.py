#!/usr/bin/env python

from setuptools import setup

setup(name='tstest',
      version='0.1.0',
      packages=['tstest'],
      description='TypeScript frontend testing',
      entry_points={
          'console_scripts': [
              'tstest = tstest.__main__:main',
          ],
      },
      package_data={'': ['tstest.html']},
      include_package_data=True, install_requires=['selenium']
      )
