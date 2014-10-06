#coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   cold
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   admin管理

from django.contrib import admin
from django.contrib.admin.sites import AdminSite 
from django.contrib.contenttypes.admin import GenericTabularInline
from django import forms
from blog.models import Commentmeta,Comments,Links,Options,Postmeta
from blog.models import Posts,TermRelationships,TermTaxonomy,Terms,Usermeta,Users

#class MyAdminSite(admin.sites.AdminSite):

# Register your models here.
class MyModelAdmin( admin.ModelAdmin ):
	pass

# class PostsAdminFrom(forms.ModelForm):
# 	def __init__(self, *args, **kwargs):
# 		super(PostsAdminFrom, self).__init__(*args, **kwargs)
# 		self.fields['post_author'].queryset = Users.objects.filter(id=self.fields['post_author'].queryset)

# 	pass




class  PostsAdmin(admin.ModelAdmin):
	#fields=('post_title','post_content','post_author')
	list_display=('post_title','post_content','post_author_name','post_date','post_status')
	list_display_links = ('post_title','post_author_name')
	list_select_related = ('post_author', )
	#inlines=(UsersInline,)
	#list_filter=('post_title','post_content')
	search_fields = ['post_title','post_content']
	#list_per_page=10
	#form=PostsAdminFrom
	actions=('make_publish','make_private',)
	fieldsets=(
		(None,{
			'fields':('post_title','post_content','post_author','post_type','post_mime_type','post_status')
		}),
		('高级选项',{
			'classes': ('collapse',),
			'fields':('post_date','post_date_gmt','post_excerpt','comment_status','ping_status','post_password','post_name')
		}),
		('其他选项',{
			'classes': ('collapse',),
			'fields':('to_ping','pinged','post_modified','post_modified_gmt','post_content_filtered','post_parent','guid','menu_order','comment_count')
		}),
	)
	def make_publish(self, request, queryset):
		queryset.update(post_status='publish')
	make_publish.short_description = "标记为发表"
	def make_private(self, request, queryset):
		queryset.update(post_status='private')
	make_private.short_description = "标记为私有"

	def post_author_name(self,obj):
		return obj.post_author.user_nicename

	pass

class  UsersAdmin(admin.ModelAdmin):
	#fields=('post_title','post_content')
	#list_filter=('post_title','post_content')
	list_display=('user_nicename','user_login','user_pass','user_email','user_status','user_registered')
	list_display_links = ('user_nicename','user_login',)

class CommentsAdmin(admin.ModelAdmin):
	list_display=('comment_post_post_title','comment_content','comment_author','comment_approved','comment_date')
	list_display_links = ('comment_post_post_title',)
	actions=('make_approve','make_unapprove')
	#readonly_fields=('',)
	fieldsets=(
		(None,{
			'fields':('comment_post','comment_content','comment_author','comment_date','comment_approved')
		}),
		('其他选项',{
			'classes': ('collapse',),
			'fields':('comment_author_email','comment_author_url','comment_author_ip','comment_date_gmt','comment_karma','comment_agent','comment_type','comment_parent','user_id')
		}),
	)
	
	def make_approve(self, request, queryset):
		queryset.update(comment_approved='1')
	make_approve.short_description = "同意评论"
	def make_unapprove(self, request, queryset):
		queryset.update(comment_approved='0')
	make_unapprove.short_description = "不同意评论"

	def comment_post_id(self,obj):
		return obj.comment_post.id
	def comment_post_post_title(self,obj):
		return obj.comment_post.post_title

class OptionsAdmin(admin.ModelAdmin):
	list_display=('option_id','option_name','option_value')
	pass



admin.site.register( Users,UsersAdmin)
admin.site.register( Posts,PostsAdmin)
admin.site.register( Comments,CommentsAdmin)
admin.site.register( Links)
admin.site.register( Options,OptionsAdmin)
#admin.site.register( Commentmeta)
#admin.site.register( Postmeta)
#admin.site.register( TermRelationships)
#admin.site.register( TermTaxonomy)
#admin.site.register( Terms)
#admin.site.register( Usermeta)
