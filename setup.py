#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Carlos Gálvez
"""
from codecs import open
from setuptools import find_packages, setup


def get_readme():
    try:
        import pypandoc
        readme = pypandoc.convert('README.md', 'rst')
    except (ImportError, IOError):
        with open('README.md', 'r') as file_data:
            readme = file_data.read()
    return readme


setup(
    name='BabyCam',
    version='0.0.1',
    author='Carlos Gálvez Mártinez',
    author_email='jcarlosgalvezm@gmail.com',
    description='BabyMonitor with motion detection',
    long_description=get_readme(),
    license='GPLv3',
    keywords='raspberry pi cam baby streaming',
    url='https://github.com/jcarlosgalvezm/babycam/',
    packages=find_packages(),
    package_data={
        '': ['*.html'],
        'babycam': ['templates/*.html'],
    },
    include_package_data=True,
    platforms='raspbian',
    scripts=['babycam/babystream', 'babycam/babyconfig'],
    zip_safe=False,
    install_requires=open('requirements.txt').read().split(),
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'License :: OSI Approved :: GNU GENERAL PUBLIC LICENSE',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Development Status :: 4 - Beta'
	'Natural Language :: English'
    ]
)
