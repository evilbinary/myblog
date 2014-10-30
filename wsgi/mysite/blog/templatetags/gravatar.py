#coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :  

from django import template
import urllib
import hashlib
from django.conf import settings

register = template.Library() 

GRAVATAR_URL_PREFIX = getattr(settings, "GRAVATAR_URL_PREFIX", "http://www.gravatar.com/avatar/")
GRAVATAR_DEFAULT_IMAGE = getattr(settings, "GRAVATAR_DEFAULT_IMAGE", "/static/img/avatar.jpg")

class GravatarUrlNode(template.Node):
    def __init__(self, email):
        self.email = template.Variable(email)

    def render(self, context):
        try:
            email = self.email.resolve(context)
        except template.VariableDoesNotExist:
            return ''

        default = GRAVATAR_DEFAULT_IMAGE
        size = 40

        gravatar_url = GRAVATAR_URL_PREFIX + hashlib.md5(email.lower()).hexdigest() + "?"
        gravatar_url += urllib.urlencode({'d':default, 's':str(size)})
        return gravatar_url

@register.tag
def gravatar_url(parser, token):
    try:
        tag_name, email = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]

    return GravatarUrlNode(email)

@register.filter
def get_gravatar(email,size=44,verify_default=False):
    try:
        gravatar_url=GRAVATAR_URL_PREFIX + hashlib.md5(email.lower()).hexdigest()+'?s=%d' %size
        if (verify_default):
            gravatar_url += '&d=404'
            try:
                urllib2.urlopen(gravatar_url)
            except urllib2.URLError, e:
                return None
        return gravatar_url
    except Exception,e:
        return ''
