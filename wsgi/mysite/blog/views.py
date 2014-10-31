#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   view 视图

from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from blog.models import Manager,Posts,Comments,TermTaxonomy,Terms,TermRelationships,Options,Links
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator,Page,EmptyPage, PageNotAnInteger
from django.db.models import Avg,Max,Min,Variance,Count
import datetime
from django.db import connection
from django.db.models import Q
from django.core.context_processors import csrf
from feeds import ArticlesFeed
from util import anti_resubmit
from django.http import HttpResponseRedirect
from blog.forms import CommentForm

manager=Manager()
#This is for response request


def index(request):
    context={
    'header':render_header(request),
    'footer':render_footer(request),
    'contents':render_pages(request),
     'sidebar':render_sidebar(request),
    }
    return render_to_response('index.html',context)
def page(request,page_id):
    posts_list=Posts.objects.filter(post_status='publish',post_type='page',id=page_id)

    comments=Comments.objects.filter(comment_post_id=page_id,comment_approved='1').order_by('comment_date')
    contents=render_page1(posts_list,1,'',render_comment(request,page_id,comments),1)
    context={
    'header':render_header(request),
    'footer':render_footer(request),
    'contents':contents,
     'sidebar':render_sidebar(request),
    }
    return render_to_response('index.html',context)
    pass

def pages(request,num='1'):
    context={
    'header':render_header(request),
    'footer':render_footer(request),
    'contents':render_pages(request,num),
     'sidebar':render_sidebar(request),
    }
    return render_to_response('index.html',context)

def article_detail(request,year,month,day):
    context={'contents':'article_detail paget:'+year+' '}

    return render_to_response('index.html',context)

def year_archive(request,year):
    context={'contents':year+' '}

    return render_to_response('index.html',context)

def month_archive(request,year,month):
    context={'contents':year+' '+month}
    return render_to_response('index.html',context)


def render_sidebar(request):
    #ToDo profile
    #recent_comments=Comments.objects.all().only('comment_id','comment_post','comment_author').order_by('comment_date')
    recent_comments=Comments.objects.select_related('comment_post').filter(comment_approved='1',comment_post__post_status='publish',comment_post__post_type='post').order_by('-comment_date')[:7]
    #recent_comments=''
    #return test(request,{'test':recent_comments})

    recent_posts=Posts.objects.filter(post_status='publish',post_type='post').only('id','post_title').order_by('-post_date')[:7]
    #categories=TermTaxonomy.objects.select_related('term').filter(taxonomy='category',count__gt=0).order_by('terms')
    categories=Terms.objects.select_related('term').filter(termtaxonomy__taxonomy='category',termtaxonomy__count__gt=0).order_by('name')
    
    #this sql equal to SELECT YEAR(post_date) AS `year`, MONTH(post_date) AS `month`, count(ID) as posts FROM e_posts  WHERE post_type = 'post' AND post_status = 'publish' GROUP BY YEAR(post_date), MONTH(post_date) ORDER BY post_date DESC
    #archives=Posts.objects.filter(post_status='publish',post_type='post').extra(select={'year':'year(post_date)','month':'month(post_date)'}).values('year','month').annotate(Count('id')).order_by('-post_date')
    #hack to port to mysql and sqlite
    engine=connection.vendor
    archives=[]
    if engine=='sqlite':
        archives=Posts.objects.filter(post_status='publish',post_type='post').extra(select={'year':"strftime('%Y',post_date)",'month':"strftime('%m',post_date)"}).values('year','month').annotate(Count('id')).order_by('-year','-month') #.order_by('-post_date') a bug?? wat hell
    elif engine=='mysql':
        archives=Posts.objects.filter(post_status='publish',post_type='post').extra(select={'year':'year(post_date)','month':'month(post_date)'}).values('year','month').annotate(Count('id')).order_by('-post_date')
    else:
        pass;


    links,links_opt=manager.get_all_links()   

    context={
        'recent_posts':recent_posts,
        'recent_comments':recent_comments,
        'categories':categories,
        'archives':archives,
        'links':links,
        'links_opt':links_opt,
   }
    return render_to_string('sidebar.html',context)

#for post
def comment(request):

    if request.method=='POST':
        form=CommentForm(request.POST)
        comment_post_id=request.POST.get('comment_post_ID').strip()
        if form.is_valid():
            comment_content=request.POST.get('comment')
            comment_author=request.POST.get('author').strip()
            comment_email=request.POST.get('email').strip()
            comment_url=request.POST.get('url').strip()
            comment_parent=request.POST.get('comment_parent').strip()
            comment_author_ip=get_client_ip(request)
            comment_agent=request.META.get('HTTP_USER_AGENT',None)
            if comment_post_id==None or comment_parent==None:
                return index(request)
            if comment_author=='' or comment_email=='' or comment_content=='':
                return article(request,comment_post_id)

            p=Posts.objects.get(pk=comment_post_id)
            comment=Comments(comment_post=p,comment_approved='0',comment_author=comment_author,comment_parent=comment_parent,comment_content=comment_content,comment_author_email=comment_email,comment_author_url=comment_url,comment_author_ip=comment_author_ip,comment_agent=comment_agent)
            # comment.comment_date=datetime()
            p.comment_count=p.comment_count+1
            p.save()
            comment.save()

            request.session['comment_author']=comment_author
            request.session['comment_email']=comment_email

            #context={'test':comment_post_id}
            if(p.post_type=='post'):
                #return article(request,comment_post_id)
                return HttpResponseRedirect('/blog/article/'+comment_post_id+'#comment-%s'%comment.comment_id)#防止重复提交
            elif(p.post_type=='page'):
                #return page(request,comment_post_id)
                return HttpResponseRedirect('/blog/page/'+comment_post_id)#防止重复提交
        else:
            #t = loader.get_template('test.html')
            #return HttpResponse(t.render(Context({'form':form})) )
            contexts={'comment_form':form}
            return article(request,comment_post_id,contexts)
            pass
    else:
        pass    
    return index(request)

#页面过期
def page_expir(request):
    comment_post_id=request.POST.get('comment_post_ID')
    if comment_post_id!=None:
        return article(request,comment_post_id)
    return index(request)
    #return render_to_response('index.html',{})
    pass

def search(request):
    s=request.GET.get('s')
    posts_list=[]
    if s!=None:
        posts_list=Posts.objects.all().filter(post_status='publish',post_type='post').filter(Q(post_title__contains=s)|Q(post_content__contains=s))
    
    context={
        'header':render_header(request),
        'footer':render_footer(request),
        'contents':render_page1(posts_list),
         'sidebar':render_sidebar(request),
        }
    return render_to_response('index.html',context,context_instance=RequestContext(request))
    #return page(request)


def cat(request,num='1'):
    #test=TermRelationships.objects.select_related('object').filter(term_taxonomy_id=num,object__post_type='post')
    posts_list=Posts.objects.select_related('termrelationship').filter(termrelationships__term_taxonomy__term_id=num,post_type='post')
    
    context={
    'header':render_header(request),
    'footer':render_footer(request),
    'contents':render_page1(posts_list),
     'sidebar':render_sidebar(request),
    }
    return render_to_response('index.html',context)
    #return render_to_response('test.html',context)
    pass
def test(request):
    #cats=Terms.objects.select_related('termtaxonomy') #.select_related('termrelationships').filter(termtaxonomy__taxonomy__in=('category', 'post_tag', 'post_format'))
    #post_list=Posts.objects.all()
    
    #cats=TermRelationships.objects.select_related('term_taxonomy__term').filter(term_taxonomy__taxonomy__in=('category', 'post_tag', 'post_format'),object_id__in=[ p.id for p in post_list])
    cats=''

    #all_links=Links.objects.all().filter(link_visible='Y')
    #terms=Terms.objects.select_related('term').filter(termtaxonomy__taxonomy='link_category',termtaxonomy__count__gt=0).order_by('name')

    #TermRelationships.objects.select_related('Links').filter(term_taxonomy__taxonomy__in=('link_category',)
    #TermRelationships.objects.select_related('Links').filter(term_taxonomy__taxonomy__in=('link_category',),object__in=[x.link_id for x in links])
    #links=terms #TermRelationships.objects.select_related('Links') #.filter(term_taxonomy__taxonomy__in=('link_category',),object_id__in= link_id )
    
    links=Links.objects.filter(link_visible='Y').extra(select={'post_id':'link_id'})
    cats=TermRelationships.objects.select_related('term_taxonomy__term').filter(term_taxonomy__taxonomy__in=('link_category',),term_taxonomy__count__gt=0)
    all_links={}
    for l in links:
        for c in cats:
            if(c.object_id==l.link_id):
                if(c.term_taxonomy.term.name in all_links):
                    all_links[c.term_taxonomy.term.name].append(l)
                else:
                    all_links[c.term_taxonomy.term.name]=[l,]   

    context=RequestContext(request,{'cats':cats,'links':all_links}) 
    #context={'test':cats}
    return render_to_response('test.html',context)

#This is for render templete
def archive(request,year='2014',month='01'):
    posts_list=Posts.objects.all().filter(post_status='publish',post_type='post',post_date__year=year,post_date__month=month)
    context={
    'header':render_header(request),
    'footer':render_footer(request),
    'contents':render_page1(posts_list),
     'sidebar':render_sidebar(request),
    }
    return render_to_response('index.html',context)

def article(request,post_id,contexts=None):

    context={
    'header':render_header(request),
    'footer':render_footer(request),
    'contents':render_article(request,post_id,contexts),
     'sidebar':render_sidebar(request),
    }
    return render_to_response('index.html',context)

def feed(request,str=''):
    context={}
    return render_to_response('test.html',context) 


def render_header(request):
    pages=Posts.objects.all().filter(post_status='publish',post_type='page').only('id','post_title').order_by('menu_order','-post_date')
    # headeinfo=
    
    # headinfo={'blogname':'',''}
    # headinfo['blogname']='aaaa'
    # headinfo['blogname']='bbb'
    headinfo=Manager().get_head_info()
    context=RequestContext(request,{'pages':pages,'headeinfo':headinfo}) 
    return render_to_string('header.html',context)
def render_footer(request):
    context=RequestContext(request) 
    return render_to_string('footer.html',context)

def render_contents(posts,cat=''):
    cats=TermRelationships.objects.select_related('term_taxonomy__term').filter(term_taxonomy__taxonomy__in=('category', 'post_tag', 'post_format'),object_id__in=[ p.id for p in posts])
    #cats=Terms.objects.select_related('termtaxonomy').select_related('termrelationships').filter(termtaxonomy__taxonomy__in=('category', 'post_tag', 'post_format'))
    cat_terms={}
    for cat in cats:
        cat_terms[cat.object_id]=cat.term_taxonomy.term
    # i=0
    for post in posts:
        #if i< len(cats):
        #    post.cat=cats[i].term_taxonomy.term
        if post.id in cat_terms:
            post.cat=cat_terms[post.id]
        else:
            post.cat=None
        # i=i+1
        pass
    context={'posts':posts,}
    return render_to_string('content.html',context)

def render_nator(page):
    context={'page':page}
    return render_to_string('page_nator.html',context)

def render_nator2(prev,next):
    context={'prev_post':prev,
            'next_post':next}
    return render_to_string('page_nav.html',context)
def render_comment(request,comment_post_id,comments=[],contexts=None):
    #构造评论嵌套
    #comments=sorted(test.items(), key=lambda d: d[0],reverse=False) #控制回复排序时间
    # dic={}
    # dic_val={}
    # i=0
    # for c in comments:
    #     if c.comment_parent==0:
    #         dic[c.comment_id]=0
    #         dic[c.comment_id]=(i,str(i))
    #         i=i+1
    #     else:
    #         p=dic[c.comment_parent]
    #         n=p[0]+1
    #         s=p[1]+'.%d'%(n)
    #         dic[c.comment_id]=(n,s)
    #     dic_val[c.comment_id]=c

    # l=[( (v[0],v[1]+'' ),dic_val[k]) for k,v in dic.items()]
    # test=sorted(l, key=lambda d:(d[0][1],d[1].comment_parent),reverse=False) 

    #turn into json data 
    dic={}
    stack=[]
    for c in comments:
        dic[c.comment_id]={'self':c,'level':0}
        if c.comment_parent!=0:
            if 'children' in dic[c.comment_parent]:
                dic[c.comment_parent]['children'].insert(0,dic[c.comment_id])
                pass
            else:
                dic[c.comment_parent]['children']=[dic[c.comment_id]]#{c.comment_id:c}
            dic[c.comment_id]['level']= dic[c.comment_parent]['level']+1
        else:
            stack.insert(0,dic[c.comment_id])  
    #now dict is json format and so is the stack(only for comment_parent=0) :).
    #trace the json data
    result=[]
    while len(stack)>0:
        top=stack.pop()
        #result.append(top)
        if 'children' not in top:
            result.append((top['level'],top['self']) )
        else:
            c=top['children']
            l=top['level']
            s=top['self']
            result.append( (l,s))
            stack=stack+c
        pass
    test=result
    comments=result
    context={'comment_post_id':comment_post_id,'comments':comments,'test':test,'request':request,'contexts':contexts }
    if request!=None:
        context.update(csrf(request))
    context=RequestContext(request,context) 
    return render_to_string('comment.html',context)

def render_page1(posts,num='1',nator=None,comment=None,num_page=5):
    paginator = MyPaginator(posts, num_page)
    try:
        page=paginator.page(num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page= paginator.page(paginator.num_pages)
    contents=render_contents(page)
    if nator==None:
        nator=render_nator(page) 
    context={ 
        'page_contents':contents,
        'page_nator':nator,
       }
    if comment!=None: 
        context['page_comment']=comment
    return render_to_string('page.html',context)




def render_article(request,post_id,contexts=None):
    objs=Posts.objects.all().filter(post_status='publish',post_type='post')
    prev_post=objs.filter(id__lt=post_id).only('id','post_title').last()
    cur_post=Posts.objects.all().filter(id=post_id,post_status='publish',post_type='post')
    next_post=objs.filter(id__gt=post_id).only('id','post_title').first()
    contents=render_contents(cur_post)
    nator=render_nator2(prev_post,next_post)

    #comment_author=request.POST.get('author')
    #comment_email=request.POST.get('email')
    comment_author=None
    comment_email=None
    if 'comment_author' in request.session and 'comment_email' in request.session:
        comment_author=request.session['comment_author']
        comment_email=request.session['comment_email']

    if comment_author!=None and comment_email!=None:
        comments=Comments.objects.filter(Q(comment_post_id=post_id), Q(comment_approved='1')|(Q(comment_author = comment_author) &Q(comment_author_email=comment_email) &Q(comment_approved = '0')) ).order_by('comment_date')
    else:
        comments=Comments.objects.filter(comment_post_id=post_id,comment_approved='1' ).order_by('comment_date')
    return render_page1(cur_post,1,nator,render_comment(request,post_id,comments,contexts))

def render_pages(request,num='1'):
    context={}
    if(long(num)<=0):
        num=1
    page=None    
    post_id=request.GET.get('p')
    if post_id:
        return render_article(request,post_id)
    else:
        #get post data
        posts_list=Posts.objects.all().filter(post_status='publish',post_type='post').order_by('-post_date')
        return render_page1(posts_list,num)
    return render_to_string('page.html',context)

#get ip for comment
def get_client_ip(request):
    """get the client ip from the request
    """
    PRIVATE_IPS_PREFIX = ('10.', '172.', '192.', '127.')

    ip=''
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip=request.META['HTTP_X_FORWARDED_FOR'];
        proxies=ip.split(',')
        while (len(proxies) > 0 and
                proxies[0].startswith(PRIVATE_IPS_PREFIX)):
            proxies.pop(0)
        if len(proxies) > 0:
            ip = proxies[0]
    else:
        ip=request.META['REMOTE_ADDR']
    return ip

#Paging navigator
class MyPaginator(Paginator):
    def __init__(self,object_list, per_page,range_num=5,orphans=0,allow_empty_first_page=True):
        self.range_num=range_num;
        Paginator.__init__(self,object_list,per_page,orphans,allow_empty_first_page)

    def page(self,number):
        self.page_number=number
        return super(MyPaginator,self).page(number)
    
    def _get_page_range_ext(self):
        page_range=super(MyPaginator,self).page_range
        start=long(self.page_number) -1- self.range_num/2
        end=long(self.page_number)+self.range_num/2
        if(start<=0):
            end=end-start
            start=0
        ret=page_range[start:end]
        return ret
    page_range_ext = property(_get_page_range_ext)

class MyPage(Page):
    """docstring for MyPage"""
    def __init__(self, page):
        super(MyPage, self).__init__(page.object_list, page.number, page.paginator)
        self.object_list=page.object_list

    def _next(self):
        return self.object_list[super(MyPage,self).next_page_number()]
    def _prev(self):
        return self.object_list[super(MyPage,self).previous_page_number()]
    next=property(_next)
    prev=property(_prev)
        

