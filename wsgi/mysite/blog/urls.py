from django.conf.urls import *
from blog.views import * 
from django.conf import settings

urlpatterns= patterns('',
            url(r'^$',index),
            url(r'^blog/',index),
            url(r'^archive',archive),
            )
