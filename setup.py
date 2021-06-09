#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='getotrs',
    version='0.1',
    description='Download otrs ticket attachments',
    url='https://github.com/abbbi/getotrs/',
    author='Michael Ablassmeier',
    author_email='abi@grinser.de',
    license='GPL',
    keywords='libnbd backup libvirt',
    packages=find_packages(exclude=('docs', 'tests', 'env')),
    include_package_data=True,
    install_requires=[
    ],
    scripts=['getotrs'],
    extras_require={
    'dev': [],
    'docs': [],
    'testing': [],
    },
    classifiers=[],
    )
