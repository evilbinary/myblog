#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 11:21:19
#   Desc    :   url定义

from django.conf.urls import *
from blog import views
from django.conf import settings
from views import *
from django.contrib import admin
from feeds import ArticlesFeed,CommentsFeed


urlpatterns= patterns('',
            url(r'^$',views.index),
            url(r'^blog/',views.index),
            url(r'^archive/(\d{4})/(\d{1,2})/$',views.archive),
            url(r'^article/(\d+)/$', views.article),
            url(r'^articles/(\d{4})/$', views.year_archive),
            url(r'^articles/(\d{4})/(\d{2})/$',views.month_archive),
            url(r'^articles/(\d{4})/(\d{2})/(\d+)/$', views.article_detail),
            url(r'^pages(?P<num>\d+)/$', views.pages),
            url(r'^pages/$', views.pages),
            url(r'^pages/(?P<num>\d+)/$', views.pages),
            url(r'^page/(?P<page_id>\d+)$', views.page),
            url(r'^test(?P<num>\d+)/$', views.page),
            url(r'^comment',views.comment),
            url(r'^search/$',views.search),
            url(r'^cat/(?P<num>\d+)$',views.cat),
            url(r'^feeds/rss2$',ArticlesFeed()),
            url(r'^feeds/comments-rss2$',CommentsFeed()),
            url(r'^feeds/(?P<str>\S+)$',views.feed),
            url(r'^test$',views.test),
            url(r'^page_expir$',views.page_expir),
            
            )
