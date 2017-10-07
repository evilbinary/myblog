#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   cold
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   配置
"""
Django settings for mysite project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'tu^3doh&bqq4e00&@q0z(d$lwb_bqjc7c6#w=eht3vziqakm!k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True


ALLOWED_HOSTS = ['.evilbinary.org','localhost']


# Application definition

INSTALLED_APPS = (
    'django_admin_bootstrapped.bootstrap3',
    'django_admin_bootstrapped',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'ckeditor',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

)

TEMPLATE_CONTEXT_PROCESSORS=("django.contrib.auth.context_processors.auth",
"django.core.context_processors.debug",
"django.core.context_processors.i18n",
"django.core.context_processors.media",
"django.core.context_processors.static",
"django.core.context_processors.tz",
"django.contrib.messages.context_processors.messages")

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'

MEDIA_DIR=BASE_DIR
DATABASE_DIR=BASE_DIR

#OpenShift define here


if os.environ.has_key('OPENSHIFT_REPO_DIR'):
    DEBUG = bool(os.environ.get('DEBUG', False))
    if DEBUG:
        print("WARNING: The DEBUG environment is set to True.")
    TEMPLATE_DEBUG=DEBUG
    MEDIA_DIR=os.path.join(os.environ['OPENSHIFT_DATA_DIR'])
    DATABASE_DIR= os.path.join(os.environ['OPENSHIFT_DATA_DIR'])


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default2':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : 'django',
        'USER' : '',
        'PASSWORD' : '',
        'HOST' : '127.0.0.1',
        'PORT' : '3306'
    },
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATABASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-CN'


LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

#TIME_FORMAT = 'a'
DATETIME_FORMAT='Y/m/d H:i:s'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_LOADERS = (
    'django.template.loaders.eggs.Loader',

    'django.template.loaders.filesystem.Loader', #to load bootstrap must make it after or disable
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS=(
        os.path.join(os.path.dirname(__file__), '../blog/templates').replace('\\','/'),

        )


STATIC_ROOT=os.path.join(BASE_DIR,'../static'.replace('\\','/'))

STATICFILES_FINDERS=(
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "django.contrib.staticfiles.finders.FileSystemFinder",
    )

MYBLOG_PATH=os.path.join(os.path.dirname(__file__), '../blog/').replace('\\','/')


STATICFILES_DIRS = (
        ('css',os.path.join(STATIC_ROOT,'css')),
        ('js',os.path.join(STATIC_ROOT,'js')),
        ('img',os.path.join(STATIC_ROOT,'img')),

        ('admin/css',os.path.join(STATIC_ROOT,'admin/css')),
        ('admin/js',os.path.join(STATIC_ROOT,'admin/js')),
        ('admin/js/admin',os.path.join(STATIC_ROOT,'admin/js/admin')),

        ('admin/img',os.path.join(STATIC_ROOT,'admin/img')),


        ('admin/css',os.path.join(MYBLOG_PATH,'static/admin/css')),
        ('admin/js',os.path.join(MYBLOG_PATH,'static/admin/js')),
        ('admin/js/admin',os.path.join(MYBLOG_PATH,'static/admin/js/admin')),

        ('admin/img',os.path.join(MYBLOG_PATH,'static/admin/img')),
        )

# print  ('admin/css',os.path.join(MYBLOG_PATH,'static/admin/css'))
   
#头像地址
GRAVATAR_URL_PREFIX='https://secure.gravatar.com/avatar/'
#GRAVATAR_DEFAULT_IMAGE=''



MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(MEDIA_DIR, "media")
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'uploads')
# CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'


CKEDITOR_CONFIGS = {
    'default': {
        'toolbar':[        
            ['Source','-','Save','NewPage','Preview','-','Templates'],        
            ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print','SpellChecker','Scayt'],        
            ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],        
            ['Form','Checkbox','Radio','TextField','Textarea','Select','Button', 'ImageButton','HiddenField'], 
            ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],        
            ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],        
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],        
            ['Link','Unlink','Anchor'],        
            ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'],        
            ['Styles','Format','Font','FontSize'],        
            ['TextColor','BGColor'],        
            ['Maximize','ShowBlocks','-','About']        
        ],
        'width': 700,
        'height': 400,
        'toolbarCanCollapse': False,
    },
}

AUTH_USER_MODEL = "blog.Users"
