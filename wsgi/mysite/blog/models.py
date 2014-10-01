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

db_prefix='wp_'
db_managed=True

USER_STATUS=(
    (1,'active'),
    (0,'inactive')
)
STATUS = (
    ('closed', 'closed'),
    ('open', 'open'),
)
POST_STATUS = (
    ('draft', 'draft'),
    ('inherit', 'inherit'),
    ('private', 'private'),
    ('publish', 'publish'),
)
POST_TYPE = (
    ('attachment', 'attachment'),
    ('page', 'page'),
    ('post', 'post'),
    ('revision', 'revision'),
)
POST_MIME_TYPE=(
    ('markdown','markdown'),
    ('image/gif','image/gif'),
    ('text/html','text/html '),
    ('text/plain','text/plain'),

)


class DjangoMigrations(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = db_managed
        db_table = 'django_migrations'





class Links(models.Model):
    link_id = models.BigIntegerField(primary_key=True)
    link_url = models.CharField(max_length=255)
    link_name = models.CharField(max_length=255)
    link_image = models.CharField(max_length=255)
    link_target = models.CharField(max_length=25)
    link_description = models.CharField(max_length=255)
    link_visible = models.CharField(max_length=20)
    link_owner = models.BigIntegerField()
    link_rating = models.IntegerField()
    link_updated = models.DateTimeField()
    link_rel = models.CharField(max_length=255)
    link_notes = models.TextField()
    link_rss = models.CharField(max_length=255)

    class Meta:
        managed = db_managed
        db_table = db_prefix+'links'


class Options(models.Model):
    option_id = models.BigIntegerField(primary_key=True)
    option_name = models.CharField(unique=True, max_length=64)
    option_value = models.TextField()
    autoload = models.CharField(max_length=20)

    class Meta:
        managed = db_managed
        db_table = db_prefix+'options'



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

    class Meta:
        managed = db_managed
        db_table = db_prefix+'users'

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
    post_author = models.ForeignKey(Users)
    post_date = models.DateTimeField()
    post_date_gmt = models.DateTimeField()
    post_content = models.TextField()
    post_title = models.TextField()
    post_excerpt = models.TextField()
    post_status = models.CharField(choices=POST_STATUS,max_length=20)
    comment_status = models.CharField(max_length=20)
    ping_status = models.CharField(max_length=20)
    post_password = models.CharField(max_length=20)
    post_name = models.CharField(max_length=200)
    to_ping = models.TextField()
    pinged = models.TextField()
    post_modified = models.DateTimeField()
    post_modified_gmt = models.DateTimeField()
    post_content_filtered = models.TextField()
    post_parent = models.BigIntegerField()
    guid = models.CharField(max_length=255)
    menu_order = models.IntegerField()
    post_type = models.CharField(choices=POST_TYPE,max_length=20)
    post_mime_type = models.CharField(choices=POST_MIME_TYPE,max_length=100)
    comment_count = models.BigIntegerField()

    class Meta:
        managed = db_managed
        db_table = db_prefix+'posts'


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
    comment_author = models.TextField()
    comment_author_email = models.CharField(max_length=100)
    comment_author_url = models.CharField(max_length=200)
    comment_author_ip = models.CharField(max_length=100)  # Field name made lowercase.
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_date_gmt = models.DateTimeField(auto_now_add=True)
    comment_content = models.TextField()
    comment_karma = models.IntegerField(default=0)
    comment_approved = models.CharField(max_length=20,default=0)
    comment_agent = models.CharField(max_length=255)
    comment_type = models.CharField(max_length=20)
    comment_parent = models.BigIntegerField(default=0)
    user_id = models.BigIntegerField(default=0)

    class Meta:
        managed = db_managed
        db_table = db_prefix+'comments'



class Terms(models.Model):
    term_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(unique=True, max_length=200)
    term_group = models.BigIntegerField()

    class Meta:
        managed = db_managed
        db_table = db_prefix+'terms'


class TermTaxonomy(models.Model):
    term_taxonomy_id = models.BigIntegerField(primary_key=True)
    #term_id = models.BigIntegerField()
    term=models.ForeignKey(Terms)
    taxonomy = models.CharField(max_length=32)
    description = models.TextField()
    parent = models.BigIntegerField()
    count = models.BigIntegerField()

    class Meta:
        managed = db_managed
        db_table = db_prefix+'term_taxonomy'

class TermRelationships(models.Model):
    #object_id = models.BigIntegerField()
    term_relationship_id=models.BigIntegerField(primary_key=True)
    object=models.ForeignKey(Posts)
    #term_taxonomy_id = models.BigIntegerField()
    term_taxonomy = models.ForeignKey(TermTaxonomy)
    term_order = models.IntegerField()

    class Meta:
        managed = db_managed
        db_table = db_prefix+'term_relationships'
        #unique_together=('object','term_taxonomy_id')



