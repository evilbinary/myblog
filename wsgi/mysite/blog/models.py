#coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   模型定义

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = db_managed` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
#from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import force_unicode




db_prefix='wp_'
db_managed=True

USER_STATUS=(
    (1,'active'),
    (0,'inactive')
)
STATUS = (
    ('closed', '关闭'),
    ('open', '打开'),
)
POST_STATUS = (
    ('draft', '垃圾'),
    ('inherit', 'inherit'),
    ('private', '私有'),
    ('publish', '已发布'),
)
POST_TYPE = (
    ('attachment', '附件'),
    ('page', '页面'),
    ('post', '文章'),
    ('revision', 'revision'),
    ('nav_menu_item','导航菜单')
)
POST_MIME_TYPE=(
    ('markdown','markdown'),
    ('image/gif','image/gif'),
    ('text/html','text/html '),
    ('text/plain','text/plain'),

)
APPROVED_TYPE=(
    ('1','同意'),
    ('0','未审核'),
    ('spam','垃圾'),
    ('trash','回收站'),
)
TAXONOMY_TYPE=(
    ('category','文章分类'),
    ('post_tag','文章标签'),
    ('post_format','post_format'),
    ('link_category','链接分类'),
    )

VISIBLE_TYPE=(
    ('Y','可见'),
    ('N','私有'),
    )
TARGET_TYPE=(
    ('_blank','新建立窗口'),
    ('_top','弹出'),
    ('_none','同窗口')
    )
class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = db_managed
        db_table = 'django_migrations'


# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin
# import datetime
# class ProfileBase(type):
#     def __new__(cls, name, bases, attrs):
#         module = attrs.pop('__module__')
#         parents = [b for b in bases if isinstance(b, ProfileBase)]
#         if parents:
#             fields = []
#             for obj_name, obj in attrs.items():
#                 if isinstance(obj, models.Field): fields.append(obj_name)
#                 User.add_to_class(obj_name, obj)
#             UserAdmin.fieldsets = list(UserAdmin.fieldsets)
#             UserAdmin.fieldsets.append((name, {'fields': fields}))
#         return super(ProfileBase, cls).__new__(cls, name, bases, attrs)
        
# class Profile(object):
#     __metaclass__ = ProfileBase

# class MyProfile(Profile):
#     nickname = models.CharField(max_length = 255)
#     birthday = models.DateTimeField(null = True, blank = True)
#     city = models.CharField(max_length = 30, blank = True)
#     university = models.CharField(max_length = 255, blank = True)
    
#     def is_today_birthday(self):
#         return self.birthday.date() == datetime.date.today()


class Options(models.Model):
    #option_id = models.BigIntegerField(primary_key=True)
    option_id = models.AutoField(primary_key=True)
    option_name = models.CharField(verbose_name='名称', unique=True, max_length=64)
    option_value = models.TextField(verbose_name='值')
    autoload = models.CharField(verbose_name='自动加载' ,default='',blank=True,max_length=20)
    class Meta:
        managed = db_managed
        db_table = db_prefix+'options'
        verbose_name=u'可选'
        verbose_name_plural = u'可选管理'
    def __unicode__(self):
        return u'id[%s] %s' % (self.option_id,self.option_name)    
    
class Usermeta(models.Model):
    umeta_id = models.BigIntegerField(primary_key=True)
    user_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True)
    meta_value = models.TextField(blank=True)

    class Meta:
        managed = db_managed
        db_table = db_prefix+'usermeta'


class Users(models.Model):
    #id = models.BigIntegerField(primary_key=True)  # Field name made lowercase.
    id=models.AutoField(primary_key=True) 
    user_login = models.CharField(max_length=60)
    user_pass = models.CharField(max_length=64)
    user_nicename = models.CharField(max_length=50)
    user_email = models.CharField(max_length=100)
    user_url = models.CharField(max_length=100)
    user_registered = models.DateTimeField()
    user_activation_key = models.CharField(max_length=60)
    user_status = models.IntegerField(choices=USER_STATUS)
    display_name = models.CharField(max_length=250)
    def __unicode__(self):
        return u'%s' % (self.user_nicename)
        #return u'id['+str(self.id)+'] '+self.user_nicename
    class Meta:
        managed = db_managed
        db_table = db_prefix+'users'
        verbose_name=u'用户'
        verbose_name_plural = u'用户管理'
        #app_label = u'系统管理'

class Postmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True)
    post_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True)
    meta_value = models.TextField(blank=True)

    class Meta:
        managed = db_managed
        db_table = db_prefix+'postmeta'


class Posts(models.Model):
    #id = models.BigIntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    id=models.AutoField(primary_key=True) 
    #post_author = models.BigIntegerField()
    post_author = models.ForeignKey(Users,db_column='post_author',verbose_name='作者')
    post_date = models.DateTimeField(verbose_name='发布时间',default=datetime.datetime.now,blank=True)
    post_date_gmt = models.DateTimeField(default=timezone.now,blank=True)
    post_content = models.TextField(verbose_name='内容')
    post_title = models.TextField(verbose_name='标题')
    post_excerpt = models.TextField(default='',blank=True)
    post_status = models.CharField(verbose_name='发布状态',choices=POST_STATUS,max_length=20)
    comment_status = models.CharField(default='',blank=True,max_length=20)
    ping_status = models.CharField(verbose_name='ping状态',default='',blank=True,max_length=20)
    post_password = models.CharField(default='',blank=True,max_length=20)
    post_name = models.CharField(default='',blank=True,max_length=200)
    to_ping = models.TextField(default='',blank=True)
    pinged = models.TextField(default='',blank=True)
    post_modified = models.DateTimeField(default=datetime.datetime.now,blank=True)
    post_modified_gmt = models.DateTimeField(default=timezone.now,blank=True)
    post_content_filtered = models.TextField(default='',blank=True)
    post_parent = models.BigIntegerField(default=0,blank=True)
    guid = models.CharField(max_length=255,default='',blank=True)
    menu_order = models.IntegerField(default=0,blank=True)
    post_type = models.CharField(verbose_name='发布类型',choices=POST_TYPE,max_length=20)
    post_mime_type = models.CharField(verbose_name='文档类型',choices=POST_MIME_TYPE,max_length=100)
    comment_count = models.BigIntegerField(default=0,blank=True)
    def __unicode__(self):
        return u'%s' % (self.post_title)
        #return u'id['+str(self.id)+'] '+self.post_title
    #@models.permalink
    def get_absolute_url(self):
        # return '/blog/article/%s'%self.id
        # return ('blog.views.article',[str(self.id)])
        return reverse('blog.views.article', args=[str(self.id)])
    class Meta:
        managed = db_managed
        db_table = db_prefix+'posts'
        verbose_name=u'发布'
        verbose_name_plural = u'发布管理'

class Commentmeta(models.Model):
    meta_id = models.BigIntegerField(primary_key=True)
    comment_id = models.BigIntegerField()
    meta_key = models.CharField(max_length=255, blank=True)
    meta_value = models.TextField(blank=True)

    class Meta:
        managed = db_managed
        db_table = db_prefix+'commentmeta'


class Comments(models.Model):
    #comment_id = models.BigIntegerField(db_column='comment_ID', primary_key=True)  # Field name made lowercase.
    comment_id=models.AutoField(primary_key=True)
    #comment_post_id = models.BigIntegerField(db_column='comment_post_ID')  # Field name made lowercase.
    comment_post=models.ForeignKey(Posts)
    comment_author = models.TextField(verbose_name='评论者')
    comment_author_email = models.CharField(max_length=100)
    comment_author_url = models.CharField(max_length=200,blank=True)
    comment_author_ip = models.CharField(default='',max_length=100,blank=True)  # Field name made lowercase.
    comment_date = models.DateTimeField(verbose_name='评论日期',default=datetime.datetime.now,blank=True)
    comment_date_gmt = models.DateTimeField(default=timezone.now,blank=True)
    comment_content = models.TextField(verbose_name='评论内容')
    comment_karma = models.IntegerField(default=0)
    comment_approved = models.CharField(verbose_name='审核情况',choices=APPROVED_TYPE,max_length=20,default=0)
    comment_agent = models.CharField(default='',max_length=255,blank=True)
    comment_type = models.CharField(default='',max_length=20,blank=True)
    comment_parent = models.BigIntegerField(default=0)
    user_id = models.BigIntegerField(default=0)


    def get_absolute_url(self):
        return '/blog/?p=%s#comment-%s'%(self.comment_post.id,self.comment_id)
        # return ('blog.views.article',[str(self.id)])
        #return reverse('blog.views',args=['?p='+str(self.comment_post)] )
    
    class Meta:
        managed = db_managed
        db_table = db_prefix+'comments'
        verbose_name=u'评论'
        verbose_name_plural = u'评论管理'
    def __unicode__(self):
        return u'%s'% (self.comment_id)
        #return u'id['+str(self.id)+'] '+self.post_title
    

class Terms(models.Model):
    term_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,verbose_name=u'分类名')
    slug = models.CharField(unique=True, max_length=200,verbose_name=u'缩略名')
    term_group = models.BigIntegerField(default=0,verbose_name='分组号')
    def __unicode__(self):
        return u'%s' % (self.name)
      
    class Meta:
        managed = db_managed
        db_table = db_prefix+'terms'
        verbose_name=u'目录/标签'
        verbose_name_plural=u'目录/标签管理'


class TermTaxonomy(models.Model):
    term_taxonomy_id = models.AutoField(primary_key=True)
    #term_id = models.BigIntegerField()
    term=models.ForeignKey(Terms,verbose_name=u'目录/标签')
    taxonomy = models.CharField(max_length=32,choices=TAXONOMY_TYPE,verbose_name='分类方法(category/post_tag)')
    description = models.TextField(verbose_name='分类描述')
    parent = models.BigIntegerField(default=0,verbose_name='父分类id')
    count = models.BigIntegerField(default=0,verbose_name='数量统计')
    def __unicode__(self):
        return u'%s ->%s(%s)' % (self.taxonomy,self.term.name,self.description)
    
    class Meta:
        managed = db_managed
        db_table = db_prefix+'term_taxonomy'
        verbose_name=u'目录/标签分类'
        verbose_name_plural=u'目录/标签分类管理'


class Links(models.Model):
    link_id = models.AutoField(primary_key=True)
    link_url = models.CharField(max_length=255,verbose_name='URL链接')
    link_name = models.CharField(max_length=255,verbose_name='名称')
    link_image = models.CharField(default='',blank=True,max_length=255,verbose_name='图片')
    link_target = models.CharField(default='',blank=True,max_length=25,choices=TARGET_TYPE,verbose_name='打开方式')
    link_description = models.CharField(default='',blank=True,max_length=255,verbose_name='描述')
    link_visible = models.CharField(default='Y',blank=True,max_length=20,choices=VISIBLE_TYPE,verbose_name='是否可见')
    link_owner = models.BigIntegerField(default=0,blank=True,verbose_name='拥有者')
    link_rating = models.IntegerField(default=0,blank=True,verbose_name='排名')
    link_updated = models.DateTimeField(default=datetime.datetime.now,blank=True,verbose_name='更新日期')
    link_rel = models.CharField(default='',blank=True,max_length=255)
    link_notes = models.TextField(default='',blank=True,verbose_name='备注')
    link_rss = models.CharField(default='',blank=True,max_length=255,verbose_name='RSS链接')
    class Meta:
        managed = db_managed
        db_table = db_prefix+'links'
        verbose_name=u'链接'
        verbose_name_plural = u'链接管理'

    def __unicode__(self):
        return u'%s  链接:%s' % (self.link_name,self.link_url)

class PostLinkeManager(models.Manager):
    def get_queryset(self):
        
        ret=super(PostLinkeManager, self).get_queryset().filter()
        # for r in ret:
        #     if r.term_taxonomy.taxonomy=='link_category':
        #         #links=Links.objects.get(link_id=r.object_id)
        #         r.object.post_title=links
        #     r.object.post="111"
        return ret

class TermRelationships(models.Model):
    #object_id = models.BigIntegerField(verbose_name='文章/链接')
    term_relationship_id=models.AutoField(primary_key=True)
    #django 这个不适合使用，django two foreign keys with one column a little sad :(
    object=models.ForeignKey(Posts,verbose_name='文章')
    object_link=models.ForeignKey(Links,null=True,verbose_name='链接',db_column='object_link')

    #term_taxonomy_id = models.BigIntegerField()
    term_taxonomy = models.ForeignKey(TermTaxonomy,verbose_name='分类/标签')
    term_order = models.IntegerField(default=0,verbose_name='排序')
    objects=PostLinkeManager()

    def __unicode__(self):
        return u'%s 属于 %s分类' % (self.object_id,self.term_taxonomy.term.name)
    
    def object_link(self):
        return self.object
   

    class Meta:
        managed = db_managed
        db_table = db_prefix+'term_relationships'
        #unique_together=('object','term_taxonomy_id')
        verbose_name_plural=u'文章/链接分类管理'
        verbose_name=u'文章/链接分类'



#manager all models
class Manager(object):
    """docstring for Manager"""
    def __new__(cls,*args,**kwargs):
        #print '#####new'
        if not hasattr(cls,'_instance'):
            o=super(Manager,cls)
            #print 'new',type(o),type(cls),cls
            cls._instance=o.__new__(cls,*args,**kwargs)
            cls.instances={}
            #print 'type:',cls
        return cls._instance
    def _get_class(self,cls=''):
            module_name=''
            class_name=''
            ws=cls.rsplit('.',1)
            if len(ws)==2:
                (module_name, class_name) = ws
            else:
                class_name=ws[0]
                module_name= __file__ and os.path.splitext(os.path.basename(__file__))[0] 
            print module_name
            module_meta = __import__(module_name, globals(), locals(), [class_name]) 
            #print 'module_meta:',module_meta,' class_name:',class_name
            class_meta = getattr(module_meta, class_name) 
            cls=class_meta 
            return cls
    def __init__(self, cls=None,*args,**kwargs):
        #print '#####init self=',self.__class__.__name__,' cls:',cls
        self.cls=cls
        self.args=args
        self.kwargs=kwargs
        if cls==None:
            return
        if isinstance(cls,str):
            cls=self._get_class(cls)
        elif isinstance(cls,cls.__class__):
            self.instances[cls.__class__]=cls
            self.cls=cls.__class__
            return
        if cls in self.instances:
            self=self.instances[cls] 
        else:
            obj=cls(*args,**kwargs)
            self.instances[cls]=obj
            self=obj
    def instance(self,cls=None,*args,**kwargs):
        #print 'membermethod'
        try:
            if cls==None:
                if self.cls==None:
                    return self
                cls=self.cls
            if isinstance(cls,str):
                cls=self._get_class(cls)
            if cls in self.instances:
                return self.instances[cls]
            else:
                #print 'instance no found',type(cls),args,kwargs
                obj=cls(*args,**kwargs)
                self.instances[cls]=obj
                return obj
        except TypeError,e:
            return cls
        except AttributeError,e:
            return  cls
        except Exception , e:
            return e
    @classmethod
    def inst(cls,clz=None,*args,**kwargs):
        if clz==None:
            if cls==None:
                return cls()
            clz=cls
        return cls(clz,*args,**kwargs).instance(*args,**kwargs)
    @staticmethod
    def ins(cls=None,*args,**kwargs):
        return Manager(cls,*args,**kwargs).inst(cls,*args,**kwargs) 
    @classmethod
    def add_member_method(self,cls,fun,*args,**kwargs):
        obj=self.instance(cls,*args,**kwargs);
        setattr(obj,fun.__name__,type.MethodType(fun,obj))
        return obj
    @classmethod
    def add_static_method(self,cls,fun,*args,**kwargs):
        obj=self.instance(cls,*args,**kwargs)
        setattr(obj,fun.__name__,fun)
        return obj
    @classmethod
    def add_class_method(self):
        pass

    def get_head_info(self):
        class HeadInfo:
            def __init__(self,blogname,blogdescription,title='邪恶二进制'):
                self.blogname=blogname
                self.blogdescription=blogdescription
                self.title=title
        blogname=Options.objects.filter(option_name='blogname').last()
        if blogname!=None:
            blogname=blogname.option_value
        else:
            blogname=''

        blogdescription=Options.objects.filter(option_name='blogdescription').last()
        if blogdescription!=None:
            blogdescription=blogdescription.option_value
        else:
            blogdescription=''
        
        info =HeadInfo(blogname,blogdescription)       
        #info={'blogname':'aaa','blogdescription':'aaa'}
        return info
    def get_all_links(self):

        links=Links.objects.filter(link_visible='Y')
        cats=TermRelationships.objects.select_related('term_taxonomy__term').filter(term_taxonomy__taxonomy__in=('link_category',),term_taxonomy__count__gt=0)
        all_links={}
        all_opt={}
        for l in links:
            for c in cats:
                if(c.object_id==l.link_id):
                    if(c.term_taxonomy.term.term_id in all_opt):
                        all_links[c.term_taxonomy.term.term_id].append(l)
                    else:
                        all_links[c.term_taxonomy.term.term_id]=[l,]   
                    all_opt[c.term_taxonomy.term.term_id]=c
        return all_links,all_opt
        pass
