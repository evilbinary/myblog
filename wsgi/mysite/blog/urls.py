from django.conf.urls import *
from blog import views
from django.conf import settings
from views import *
from django.contrib import admin


urlpatterns= patterns('',
            url(r'^$',views.index),
            url(r'^blog/',views.index),
            url(r'^archive/(\d{4})/(\d{1,2})/$',views.archive),
            url(r'^article/(\d+)/$', views.article),
            url(r'^articles/(\d{4})/$', views.year_archive),
            url(r'^articles/(\d{4})/(\d{2})/$',views.month_archive),
            url(r'^articles/(\d{4})/(\d{2})/(\d+)/$', views.article_detail),
            url(r'^page(?P<num>\d+)/$', views.page),
            url(r'^page/$', views.page),
            url(r'^test(?P<num>\d+)/$', views.page),
            url(r'^comment',views.comment),
            url(r'^search/$',views.search),
            url(r'^cat/(?P<num>\d+)$',views.cat),
            url(r'^feed/(?P<str>\S+)$',views.feed),
            url(r'^test$',views.test),
            )
