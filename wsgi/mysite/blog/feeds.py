#coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   rss生成


from django.contrib.syndication.views import Feed  
from blog.models import Posts,Comments
from blog.templatetags.myfilter import autop_filter

class CommentsFeed(Feed):
	title=u"evilbinary博客评论"
	link=u"/blog/feeds/rss2"
	description=u"关注evilbinary博客"

	def items(self):
		return  Comments.objects.select_related('comment_post').filter(comment_post__post_status='publish',comment_post__post_type='post').order_by('comment_date')[:50]
	def item_title(self,item):
		return item.comment_post.post_title
	def item_description(self,item):
		return autop_filter(item.comment_content)

	def item_link(self,item):
		return "/blog/article/"+str(item.comment_id)
	def author_name(self, obj):
		return 'evilbinary'
	def author_email(self, obj):
		return 'rootntsd@gmail.com'
	

class ArticlesFeed(Feed):
	title=u"evilbinary博客"
	link="/blog/feeds/rss2"
	description=u"关注evilbinary博客"
	author_email="rootntsd@gmail.com"
	author_name="evilbinary"
	def items(self):
		return Posts.objects.filter(post_status='publish',post_type='post').order_by('-post_date')[:50]
	def item_title(self,item):
		return item.post_title
	def item_description(self,item):
		return autop_filter(item.post_content)

	def item_link(self,item):
		return "/blog/article/"+str(item.id)
	def author_name(self, obj):
		return 'evilbinary'
	def author_email(self, obj):
		return 'rootntsd@gmail.com'


