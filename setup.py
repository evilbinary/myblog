#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   cold
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   

from setuptools import setup

setup(
    name='Blog',
    version='1.1',
    description='evilbinary blog app',
    author='evilbinary',
    author_email='rootntsd@gmail.com',
    url='http://www.python.org/sigs/distutils-sig/',
    install_requires=['Django>=1.7','pytz','markdown','Pygments',],
)
