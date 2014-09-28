from django import template
from django.utils.html import conditional_escape 
from django.utils.safestring import mark_safe 


register=template.Library()


@register.filter(name='autop')
def autop_filter(value,autoescape=None):
    values=value.split('\n\r')
    ret=''
    esc=None
    if autoescape==None: 
        esc = conditional_escape 
    else: 
        esc = lambda x: x 
        pass
    for v in values:
      	if v=='\r':
    		ret=esc(ret)+'<br>'
    	else:
			ret=ret+'<p>'+esc(v).replace('\r','<br>')+'</p>'
	ret=mark_safe(ret)
    return ret

