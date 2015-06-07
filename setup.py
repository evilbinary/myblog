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
    install_requires=['Django==1.7','pytz','Markdown>=2.5.1','Pygments>=1.6','MySQL-python','django-admin-bootstrapped==2.1.0','beautifulsoup4>=4.3.2','Pillow','django-ckeditor'],
)
