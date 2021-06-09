#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


from getotrs import __version__

setup(
    name='getotrs',
    version=__version__,
    description='Download otrs ticket attachments',
    url='https://github.com/abbbi/getotrs/',
    author='Michael Ablassmeier',
    author_email='abi@grinser.de',
    license='GPL',
    keywords='otrs download attachment',
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
