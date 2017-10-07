#coding=utf-8
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :    
from django import template
from django.utils.html import conditional_escape ,strip_tags,linebreaks
from django.utils.safestring import mark_safe 
import markdown 
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from django.template.loader import render_to_string
from django.template import RequestContext
from bs4 import BeautifulSoup #html解析BeautifulSoup 可以支持多种解析器，如lxml, html5lib, html.parser.  所以很方便，哈哈好，而且兼容性好，PS这里不是在宣传。
from bs4 import NavigableString,Tag
import re

register=template.Library()
flag_tags=-1


@register.filter(name='gen_comment_block')
def gen_comment_block(comments,request=None):
    ret=''
    current_level=0
    for level,comment in comments:
        if level==0:
            while current_level>0:
                ret=ret+'</ol>'
                current_level=current_level-1
            ret=ret+'</li>'
        else:
            if current_level<=0:
                ret=ret+"<ol class='children'>"
                current_level=current_level+1
            else:
                if current_level>level:
                    sub=current_level-level
                    while sub>0:
                        ret=ret+'</ol>'
                        sub=sub-1
                        pass
                    current_level=level
                elif current_level==level:
                    pass
                else:
                    ret=ret+"<ol class='children'>"
                    current_level=current_level+1
                    pass
        context={'comment':comment,'level':level}
        context=RequestContext(request,context) 
        ret=ret+render_to_string('comment_block.html',context)
    return mark_safe(ret)



@register.filter(name='mark_tag')

def mark_tag(tag,c):
    global flag_tags
    if flag_tags>=0:
        childs='len:%d  flag:%d @%s'%(len(tag[1])/2,flag_tags,tag)
        flag_tags=len(tag[1])/2
        for i in range(flag_tags):
            childs=childs+c 
        return mark_safe(childs)
    return '!!!!!!!!!!!!!'
@register.filter(name='mark_tag_end')
def mark_tag_end(tag,child):
    global flag_tags
    flag_tags=-1
@register.filter(name='mark_tag_start')
def mark_tag_start(tag,child):
    global flag_tags
    if flag_tags<0:
        flag_tags=0
        return  child
    return ''


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
    #extensions=['fenced_code']
    ret=markdown.markdown(value,extensions=extensions,safe_mode=True,enable_attributes=False)
    return mark_safe(ret)

@register.filter(name='highlight')
def highlight_filter(value,style=None):
    if style!=None:
        HtmlFormatter().get_style_defs(style)
    ret=highlight(value, PythonLexer(), HtmlFormatter())
    return ret

#p_pre = re.compile(r'<pre (?=[\'"]?\w+[\'"]?).*?>(?P<code>[\w\W]+?)</pre>')
p_pre = re.compile(r'<pre(?P<attr>[\W\w]*?)>(?P<code>[\w\W]*?)</pre[\w\W]*?>')
p_code=re.compile(r'<code[\w\W]*?>(?P<code>[\w\W]+?)</code[\w\W]*?>')

@register.filter(name='autocode')
def auto_mark_code_filter(value,autoescape='True'):
    pre_list = p_pre.findall(value)
    esc=None
    if autoescape and autoescape=='True': 
        esc = conditional_escape 
    else: 
        esc = lambda x: x 
        pass

    if pre_list:
        split_list = p_pre.split(value)
        #print split_list
        for pre_block in p_pre.finditer(value):

            #print 'pre_block:============',pre_block.groups(1),'=====',pre_block.group()
            attr=pre_block.group('attr')
            code = pre_block.group('code')
            #print 'code:=================',code
            if attr:
                attr_index = split_list.index(attr)
                split_list[attr_index]=''

            code_index = split_list.index(code)
            code2_=None
            m_code2=p_code.search(pre_block.group())
            ret_code=''
            if m_code2:
                code2=m_code2.group('code')
                ret_code='<pre '+attr+'><code>'+esc(code2)+'</code></pre>'
            else:
                ret_code='<pre '+(attr).replace('"',"'")+'>'+esc(code)+'</pre>'
            #print 'code==================:', ret_code
            #pre=pre_block.group()
            #print 'tyep====',type(code)
            #index = split_list.index(pre_block)
            #split_list[attr_index]=attr
            split_list[code_index]=ret_code
            pass
        v=['<p>'+v+'</p>' for v in split_list if v!='']
        value=  mark_safe(''.join(v))
        #print 'ret-----------------------\n',value
        return value
    return auto_mark_filter(value)
    pass

@register.filter(name='automark')
def auto_mark_filter(markup,htmlparser=None):
    soup=None
    if htmlparser:
        soup=BeautifulSoup(markup,htmlparser)
    else :
        soup=BeautifulSoup(markup)
    
    #attrMap = soup.attrMap;
    #print "attrMap=",dir(soup);
    esc=None
    autoescape='False'
    if autoescape and autoescape=='True': 
        esc = conditional_escape 
    else: 
        esc = lambda x: unicode(x )
        pass
    ret =''
    body= soup.body or soup
    # print 'body:',body,'[body-----]'
    for c in body:
        a=c
        #c=c.wrap(soup.new_tag('p'))
        # print type(a),'content:',c
        ss=[]
        s=''
        if isinstance(a,NavigableString)  :
            a=c
            s=c.string
        elif isinstance(a,Tag):
            # a=a.unwrap()
            # print 'type======',type(a)
            # print 'a====',a
            # print '===xxxx',a.p
            if a.name=='pre':
                continue
            else:
                s=a.string

            # else:
            #     continue

            # dd

        else:
            continue
        if s!=None:
            ss=s.split('\r\n')
        # ss1=a.string.split('\')
        # if len(ss)<len(ss1):
            # ss=ss1
        # print 'ss:',a.string
        p_tag = soup.new_tag("p")
        i=0
        for s in ss:
            if len(s.strip(''))>0:
                new_tag=soup.new_tag('p')
                new_tag.string=esc(s)
                if i==0:
                    p_tag=new_tag
                elif new_tag.string!='':
                    p_tag.append(new_tag)
                # else:
                #     p_tag.append(new_tag)
                i=i+1
                # print '====',s
        if i>0:
            c.replace_with(p_tag)      
    pre_tags=soup.find_all('pre')
    for pre_node in pre_tags:
        code=pre_node.code or pre_node
        i=0
        for child in code.children:
            s=(esc(child))
            if i==0:
                s=s.strip('\n')
                s=s.strip('\r\n')
            child.replace_with( s )
            i=i+1
         #ret=ret+'###'.join(pre_node.strings)
    ret=soup.body or soup
    #ret=linebreaks(ret)

    return mark_safe(ret)
    # soup.prettify()
    # return mark_safe(''.join(['###########'+unicode(i.string)+'---------------<br>' for i in soup.body.contents]))

    pass

@register.filter(name='autop')
def autop_filter(value,autoescape=None):
    values=value.split('\r\n\r\n')
    ret=''
    esc=None
    if autoescape and autoescape=='True': 
        esc = conditional_escape 
    else: 
        esc = lambda x: x 
        pass
    pa=[]
    pb=[]
    for i in xrange(0,len(values)):
        if values[i].find('<pre')>=0 and values[i].find('</pre')<0:
            pa.append(i)
        elif values[i].find('<pre')<0 and values[i].find('</pre')>=0:
            pb.append(i)

    if len(pa)==len(pb):
        dela=[]
        for i in xrange(0,min(len(pa),len(pb))):
            for j in xrange(pa[i]+1,pb[i]+1):
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
