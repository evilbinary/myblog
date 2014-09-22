from django.contrib import admin
from blog.models import Commentmeta,Comments,Links,Options,Postmeta
from blog.models import Posts,TermRelationships,TermTaxonomy,Terms,Usermeta,Users
# Register your models here.
class MyModelAdmin( admin.ModelAdmin ):
	pass

admin.site.register( Commentmeta)
admin.site.register( Comments)
admin.site.register( Links)
admin.site.register( Postmeta)
admin.site.register( Posts)
admin.site.register( TermRelationships)
admin.site.register( TermTaxonomy)
admin.site.register( Terms)
admin.site.register( Usermeta)
admin.site.register( Users)
