#!/usr/bin/env python3
# coding:utf-8

from setuptools import setup

setup(name='jsonica',
      version='0.1.0',
      description='manage huge json as xlsx statistically.',
      author='setminami',
      author_email='set.minami@gmail.com',
      url='https://setminami.github.io/Jsonica/',
      packages=find_packages(exclude=['contrib', 'docs', 'output', 'Samples', 'tests']),
      install_requires=['openpyxl', 'PyYAML', 'jsonschema'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
      ],
    )
