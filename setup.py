#!/usr/bin/env python

from setuptools import setup

setup(name='tsftest',
      version='0.1.0',
      packages=['tsftest'],
      description='TypeScript frontend testing',
      entry_points={
          'console_scripts': [
              'tsftest = tsftest.__main__:main',
          ],
      },
      package_data={'': ['tsftest.html', 'tsconfig.json', 'webpack.config.js']},
      include_package_data=True, install_requires=['selenium']
      )
