#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'openshift.settings'
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'openshift'))
virtenv = os.environ['APPDIR'] + '/virtenv/'
os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.6/site-packages')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except:
    pass

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
