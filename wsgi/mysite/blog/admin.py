#coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   admin管理

from django.contrib import admin,auth
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


class TermRelationshipsInline(admin.TabularInline):
	model=TermRelationships
	fk_name='object'
	list_display=('cat_name',)
		
	#fields=('term_relationship_id','cat_name')

	def cat_name(self,obj):
		return obj.term_taxonomy.term.name
		
	


class  PostsAdmin(admin.ModelAdmin):
	#fields=('post_title','post_content','post_author')
	list_display=('post_title','post_content_more','post_author_name','post_date','post_status')
	list_display_links = ('post_title','post_author_name')
	list_select_related = ('post_author', )
	#inlines=(UsersInline,)
	#list_filter=('post_title','post_content')
	search_fields = ['post_title','post_content']
	#list_per_page=10
	#form=PostsAdminFrom
	actions_on_bottom=True
	actions_on_top=False
	actions=('make_publish','make_private',)
	#inlines=(TermRelationshipsInline,)
	# list_editable=('post_content',)
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
	#actions
	def make_publish(self, request, queryset):
		rows_updated=queryset.update(post_status='publish')
		message_bit = "%s 条记录已" % rows_updated
		self.message_user(request, "%s成功修改为发布." % message_bit)
	make_publish.short_description = "标记为发表"
	def make_private(self, request, queryset):
		rows_updated=queryset.update(post_status='private')
		message_bit = "%s 条记录已" % rows_updated
		self.message_user(request, "%s成功修改为私有." % message_bit)
	make_private.short_description = "标记为私有"

	#colums
	def post_author_name(self,obj):
		return obj.post_author.user_nicename
	post_author_name.short_description='发布人'
	def post_content_more(self,obj):
		return obj.post_content[0:200]#+u'更多'
	post_content_more.short_description='内容摘要'
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
		rows_updated =queryset.update(comment_approved='1')
		message_bit = "%s 条记录已" % rows_updated
		self.message_user(request, "%s同意评论." % message_bit)
	make_approve.short_description = "同意评论"
	def make_unapprove(self, request, queryset):
		rows_updated =rows_updated =queryset.update(comment_approved='0')
		message_bit = "%s 条记录已" % rows_updated
		self.message_user(request, "%s不同意评论." % message_bit)
	make_unapprove.short_description = "不同意评论"

	def comment_post_id(self,obj):
		return obj.comment_post.id
	def comment_post_post_title(self,obj):
		return obj.comment_post.post_title
	comment_post_post_title.short_description = "评论文章标题"
class OptionsAdmin(admin.ModelAdmin):
	list_display=('option_name','option_value','autoload')
	pass

class TermsAdmin(admin.ModelAdmin):
	"""docstring for TermsAdmin"""
	list_display=('name','slug','term_group')

class TermRelationshipsAdmin(admin.ModelAdmin):
	list_display=('post_title','cat','term_order')
	def post_title(self,obj):
		return obj.object.post_title
	post_title.short_description=u'标题'
	def cat(self,obj):
		return obj.term_taxonomy
	cat.short_description=u'分类'

class TermTaxonomyAdmin(admin.ModelAdmin):
	"""docstring for TermTaxonomy"""
	list_display=('term','taxonomy','count')

class LinksAdmin(admin.ModelAdmin):
	"""docstring for LinksAdmin"""
	list_display=('link_name','link_url','link_visible')
	list_display_links=('link_name','link_url')
	fieldsets=(
		(None,{
			'fields':('link_name','link_url','link_visible')
		}),
		('其他选项',{
			'classes': ('collapse',),
			'fields':('link_image','link_target','link_description','link_owner','link_rating','link_updated','link_rel','link_notes','link_rss')
		}),
	)
class MyAdminSite(AdminSite):

	site_header='evilbianry 管理'
	site_title='evilbianry 站点管理'
	index_title='evilbinary'
	def __init__(self,name='admin',app_name='admin'):
		super(MyAdminSite,self).__init__(name,app_name)
	pass


# AdminSite.site_header='evilbianry 管理'
# AdminSite.site_title='evilbianry 站点管理'
admin.site=MyAdminSite()

admin.site.register(auth.models.User)
admin.site.register(auth.models.Group)

admin.site.register( Users,UsersAdmin)
admin.site.register( Posts,PostsAdmin)
admin.site.register( Comments,CommentsAdmin)
admin.site.register( Links,LinksAdmin)
admin.site.register( Options,OptionsAdmin)
#admin.site.register( Commentmeta)
#admin.site.register( Postmeta)
admin.site.register( TermRelationships,TermRelationshipsAdmin)
admin.site.register( TermTaxonomy,TermTaxonomyAdmin)
admin.site.register( Terms,TermsAdmin)
#admin.site.register( Usermeta)
