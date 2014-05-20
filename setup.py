#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import join, dirname
from setuptools import setup, find_packages


def get_version(fname='kavahq/__init__.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])

setup(
    name='apiclient-kava',
    version=get_version(),
    packages=find_packages(),
    requires=['python (>= 2.7)', ],
    install_requires=[],
    tests_require=[],
    description='wrapper over kavahq.com API',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author='42 Coffee Cups',
    author_email='contact@42cc.co',
    url='https://github.com/42cc/apiclient-kava',
    download_url='https://github.com/42cc/apiclient-kava/archive/master.zip',
    license='GPL v2 License',
    keywords=['kavahq', 'api'],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Programming Language :: Python',
    ],
)
