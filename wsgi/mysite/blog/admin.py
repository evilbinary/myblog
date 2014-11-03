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
from widgets import TreeSelect,MySelect
from django.contrib.admin.utils import (quote, unquote, flatten_fieldsets,
    get_deleted_objects, model_format_dict, NestedObjects,
    lookup_needs_distinct)
from django.contrib.admin import widgets, helpers

from django.utils.translation import ugettext as _
from django.utils.translation import ungettext
from django.utils.encoding import force_text, python_2_unicode_compatible

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User



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

	radio_fields = {"post_status": admin.HORIZONTAL }
	view_on_site=True
	#inlines=(TermRelationshipsInline,)
	# list_editable=('post_content',)
	# formfield_overrides = {
 #        models.TextField: {'widget': RichTextEditorWidget},
 #    }

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

	def view_on_site(self, obj):
		return '/blog/article/%s'%obj.id

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
	list_display=('comment_post_post_title','comment_content_more','comment_author','comment_approved','comment_date')
	list_display_links = ('comment_post_post_title',)
	actions=('make_approve','make_unapprove')
	radio_fields = {"comment_approved": admin.HORIZONTAL }
	view_on_site=True
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
	def view_on_site(self, obj):
		return '/blog/?p=%d#comment-%d'%(obj.comment_post.id,obj.comment_id)

	
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

	def comment_content_more(self,obj):
		return obj.comment_content[0:20]#+u'更多'
	comment_content_more.short_description='内容摘要'

class OptionsAdmin(admin.ModelAdmin):
	list_display=('option_name','option_value','autoload')
	list_editable=('autoload',)

	pass

class TermsAdmin(admin.ModelAdmin):
	"""docstring for TermsAdmin"""
	list_display=('name','slug','term_group')
	list_editable=('term_group',)


class TermRelationshipsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
    	args[0].object.post_title="aa"
        super(TermRelationshipsForm, self).__init__(*args, **kwargs)
        
        # change a widget attribute:
        a=self.fields
        b=self
        self.fields['object'].widget.attrs["size"] = 50000000
        self.fields['object'].post_title='aaa'
        # dd
  #   def clean(self):
		# cleaned_data = super(CommentForm, self).clean()
		# tmp_email=cleaned_data.get('email')
		# dd
	def clean_recipients(self):
		
		pass
	object_id=forms.ModelMultipleChoiceField(queryset=Links.objects.all())
    class Meta:
        model = TermRelationships
        pass

class TermRelationshipsAdmin(admin.ModelAdmin):
	list_display=('post_title','cat','term_order')
	list_editable=('term_order',)
	def post_title(self,obj):
		if  obj.term_taxonomy.taxonomy=='category':
			return obj.object.post_title
		elif obj.term_taxonomy.taxonomy=='link_category' :
			return Links.objects.get(link_id=obj.object_id)
		else:
			return obj.term_taxonomy
	post_title.short_description=u'标题'
	def cat(self,obj):
		return obj.term_taxonomy
	cat.short_description=u'分类'

 	def change_view(self, request, object_id, form_url='', extra_context=None):
		extra_context = extra_context or {}
		#extra_context['post_title'] = 'aaa'

		ret=super(TermRelationshipsAdmin, self).change_view(request, object_id,form_url, extra_context=extra_context)
		return ret

	def changeform_view(self, request, object_id=None, form_url='', extra_context=None):

	#def changeform_view(self, *args, **kwargs):


		ret= super(TermRelationshipsAdmin, self).changeform_view(request,object_id,form_url,extra_context)
		xx=ret.__dict__
		# obj = self.get_object(request, object_id)
		# if obj.term_taxonomy.taxonomy=='link_category':
		# 	links=Links.objects.filter(link_id=obj.object_id)
		# 	obj.object.post_title=links
		# 	obj.links=links
		#  	form=self.get_form(request,obj)
		# 	cc=ret.context_data['adminform']
		# 	b=cc.__dict__
		#  	f=b['form']
		#  	f=TermRelationshipsForm(obj)
		#  	x=f.fields.get('object')._queryset.post_title='sss'
			# dd
		# 	f.instance.post_title="xxxxx"
		

		#obj=TermRelationships.objects.filter(object_id=object_id)
		#modelForm=self.get_forms(request,obj)
		#cc=aa.__dict__
		
		#ret.context_data['opts']='bb'
		
		return ret
	# def get_object(self, request, object_id):
	# 	queryset = self.get_queryset(request)
	# 	model = queryset.model
	# 	try:
	# 		object_id = model._meta.pk.to_python(object_id)
	# 		ret= queryset.get(pk=object_id)
	# 		if ret.term_taxonomy.taxonomy=='link_category':
	# 			links=Links.objects.filter(link_id=ret.object_id)
	# 			ret.object.post_title=links
	# 			ret.links=links
	# 		return ret
	# 		pass
	# 	except (model.DoesNotExist, ValidationError, ValueError):
	# 		return None




	def get_queryset(self, request):		
 		qs = super(TermRelationshipsAdmin, self).get_queryset(request)
 		
		if request.user.is_superuser:
			return qs
		return qs.filter(author=request.user)
	def formfield_for_dbfield(self, db_field, **kwargs):
		field = super(TermRelationshipsAdmin, self).formfield_for_dbfield(db_field, **kwargs)
		a=db_field.__dict__
		return field
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		if db_field.name == "object":
			#aa=kwargs["queryset"]
			#pass
			bb=db_field.__dict__
			#kwargs["queryset"] = ''
			return db_field.formfield(widget = MySelect(attrs = {'width':20}))
			#aa
		return super(TermRelationshipsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

	def get_formsets(self, request, obj=None):
		ret=super(TermRelationshipsAdmin, self).get_formsets(request,obj)
		#dd
		return ret
	

class TermTaxonomyAdmin(admin.ModelAdmin):
	"""docstring for TermTaxonomy"""
	list_display=('term','taxonomy','count')

class LinksAdmin(admin.ModelAdmin):
	"""docstring for LinksAdmin"""
	list_display=('link_name','link_url','link_visible')
	list_display_links=('link_name','link_url')
	radio_fields = {"link_visible": admin.HORIZONTAL }

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

admin.site.register(auth.models.User,UserAdmin)
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
