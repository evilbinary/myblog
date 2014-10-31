#coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   forms

from django import forms
from django.forms import Form

class CommentForm(forms.Form):
	comment=forms.CharField()
	author=forms.CharField()
	email=forms.EmailField()
	url=forms.URLField(required=False) 
	def clean(self):
		cleaned_data = super(CommentForm, self).clean()
		tmp_email=cleaned_data.get('email')
		author=cleaned_data.get('author')
		comment=cleaned_data.get('comment')
		url=cleaned_data.get('url')

		if tmp_email==None :
			self._errors['email']=self.error_class(['亲，邮箱给我填正确来!'])
		if author==None:
			self._errors['author']=self.error_class(['亲，没昵称谁都不认识你!'])
		if comment==None:
			self._errors['comment']=self.error_class(['我靠，评论不写还评论个啥？'])
		if url==None:
			self._errors['url']=self.error_class(['url没写正确啊！'])
		return cleaned_data