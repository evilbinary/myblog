#coding=utf-8

from django.contrib import admin
from django import forms
from blog.models import Commentmeta,Comments,Links,Options,Postmeta
from blog.models import Posts,TermRelationships,TermTaxonomy,Terms,Usermeta,Users
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
	list_display=('post_title','post_content','post_author_name')
	list_display_links = ('post_title','post_author_name')
	list_select_related = ('post_author', )
	
	#list_filter=('post_title','post_content')
	search_fields = ['post_title','post_content']
	#list_per_page=10
	#form=PostsAdminFrom
	def post_author_name(self,obj):
		return obj.post_author.user_nicename

	pass

class  UsersAdmin(admin.ModelAdmin):
	#fields=('post_title','post_content')
	#list_filter=('post_title','post_content')
	list_display=('user_nicename','user_login','user_pass','user_email','user_status','user_registered')
	list_display_links = ('user_nicename','user_login',)



admin.site.register( Commentmeta)
admin.site.register( Comments)
admin.site.register( Links)
admin.site.register( Postmeta)
admin.site.register( Posts,PostsAdmin)
admin.site.register( TermRelationships)
admin.site.register( TermTaxonomy)
admin.site.register( Terms)
admin.site.register( Usermeta)
admin.site.register( Users,UsersAdmin)
