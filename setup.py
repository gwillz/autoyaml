#!/usr/bin/env python

from setuptools import setup
import sys, os

requirements = [i for i in open('requirements.txt').read().split()]

def get_long_description(fname):
    try:
        import pypandoc
        return pypandoc.convert(fname, 'rst')
    except:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='autoyaml',
      version="0.1",
      description="Auto loading/defaults for YAML config files",
      long_description=get_long_description('README.md'),
      author='Gwilyn Saunders',
      author_email='gwilyn.saunders@mk2es.com.au',
      url='https://git.mk2es.com.au/gwillz/gslib',
      packages=['autoyaml'],
      install_requires=requirements,
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ]
)
