from django import template
from django.utils.html import conditional_escape ,strip_tags
from django.utils.safestring import mark_safe 
import markdown 
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


register=template.Library()



@register.filter(name='dict_get')
def dict_get(value,key,default=None):
    return value.get(key,default)

@register.filter(name='get')
def value_get(value,key,default=None):
    try:
        if isinstance(value,dict):
            return value.get(key,default)
        elif isinstance(value,list):
            return vlaue[key]
        elif isinstance(value,tuple):
            return value[key]
        elif isinstance(value,str):
            return value[key]
        elif isinstance(value,object):
            return getattr(value,key)
        else:
            return ''
    except Exception,e:
        return 'except:',e




@register.filter(name='markdown')
def markdown_filter(value,arg=None):
    extensions=(arg and arg.split(','))
    ret=markdown.markdown(value,extensions=extensions,safe_mode=False,enable_attributes=False)
    return mark_safe(ret)

@register.filter(name='highlight')
def highlight_filter(value,style=None):
    if style!=None:
        HtmlFormatter().get_style_defs(style)
    ret=highlight(value, PythonLexer(), HtmlFormatter())
    return ret
@register.filter(name='autop')
def autop_filter(value,autoescape=None):
    values=value.split('\r\n\r\n')
    ret=''
    esc=None
    if autoescape==None: 
        esc = conditional_escape 
    else: 
        esc = lambda x: x 
        pass
    pa=[]
    pb=[]
    for i in range(0,len(values)):
        if values[i].find('<pre')>=0 and values[i].find('</pre')<0:
            pa.append(i)
        elif values[i].find('<pre')<0 and values[i].find('</pre')>=0:
            pb.append(i)

    if len(pa)==len(pb):
        dela=[]
        for i in range(0,min(len(pa),len(pb))):
            for j in range(pa[i]+1,pb[i]+1):
                values[pa[i]]=values[pa[i]]+'\r\n\r\n'+values[j]
                dela.append(j)
        dela.sort()
        dela.reverse()
        for k in dela:
            #pass
            del values[k]
    for v in values:
        vs=v.split('\r\n')
        ret_p=''
        ret_pre=''
        pre=0
        for vv in vs:
            if vv.find('<pre')>=0:
                pre=pre+1
                ret_pre=ret_pre+esc(vv)
                ret_p='<p>'+ret_p.replace('\r\n','</br>')+'</p>'
                ret=ret+ret_p
                ret_p=''
            elif vv.find('</pre')>=0:
                pre=pre-1
                ret_pre=ret_pre+esc(vv)
                ret=ret+'<p>'+ret_pre+'</p>'
                ret_pre=''
            else:
                if pre<=0:
                    ret_p=ret_p+'<br>'+ret_pre+esc(vv.replace('\r\n','</br>'))
                    #ret=ret+'<p>'+esc(v).replace('\r','')+'</p>'
                else:
                    ret_pre=ret_pre+''+esc(vv)+'\r\n'
                    
                #ret=ret+esc(v).replace('','')
        ret=ret+'<p>'+ret_p+'</p>'
	ret=mark_safe(ret)
    return ret
