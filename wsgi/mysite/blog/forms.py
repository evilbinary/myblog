#coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   forms

from django import forms
from django.forms import Form
from django.forms import ModelForm 
from blog.models import Posts ,Users
from blog.widgets import RichTextEditorWidget
from django.db import models
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.forms  import ReadOnlyPasswordHashField


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

		print  self.__dict__

		if tmp_email==None :
			self._errors['email']=self.error_class(['亲，邮箱给我填正确来!'])
		if author==None:
			self._errors['author']=self.error_class(['亲，没昵称谁都不认识你!'])
		if comment==None:
			self._errors['comment']=self.error_class(['我靠，评论不写还评论个啥？'])
		else:
			if len(comment)>200:
				msg='我靠，评论太长了共%d个字符，不能超过200个字符！'%len(comment)
				self._errors['comment']=self.error_class([msg])
		if url==None:
			self._errors['url']=self.error_class(['url没写正确啊！'])
		return cleaned_data

class PostsForm(ModelForm): 
	# post_title=forms.CharField(max_length=200,label='标题')
	# post_title=forms.TextInput(attrs={'size':1,'rows':0.1} )
	post_title=forms.CharField(widget=forms.TextInput(attrs={'size':80,} ),label='标题')
	post_content=forms.CharField(widget=RichTextEditorWidget(),label='内容:')
	class Meta:
		model=Posts




class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    user_login = forms.RegexField(label=_("Username"), max_length=30,
        regex=r'^[\w.@+-]+$',
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    user_pass = forms.CharField(label=_("Password"),widget=forms.PasswordInput)
    # user_pass2 = forms.CharField(label=_("Password confirmation"),
    #widget=forms.PasswordInput,
    #     help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = Users
        # fields = ("user_login","user_pass")
		#fields = '__all__'


    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["user_login"]
        try:
            User._default_manager.get(user_login=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("user_pass")
        password2 = self.cleaned_data.get("user_pass")
        if password1 and password2 and password1 != password2:
        	raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
		return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["user_pass"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    user_login = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                    "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    user_pass = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = Users
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')
    def clean_user_pass(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["user_pass"]