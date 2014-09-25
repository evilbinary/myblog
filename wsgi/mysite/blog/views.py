from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from blog.models import Posts,Comments,TermTaxonomy,Terms,TermRelationships
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator,Page,EmptyPage, PageNotAnInteger
from django.db.models import Avg,Max,Min,Variance,Count
import datetime
from django.db import connection

#This is for response request


def index(request):
    context={
    'header':render_header(request),
    'footer':render_footer(request),
    'contents':render_page(request),
     'sidebar':render_sidebar(request),
    }
    return render_to_response('index.html',context)
def page(request,num='1'):
    context={
    'header':render_header(request),
    'footer':render_footer(request),
    'contents':render_page(request,num),
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
    recent_comments=Comments.objects.select_related('comment_post').filter(comment_post__post_status='publish',comment_post__post_type='post').order_by('comment_date')[:7]
    #recent_comments=''
    #return test(request,{'test':recent_comments})

    recent_posts=Posts.objects.filter(post_status='publish',post_type='post').only('id','post_title').order_by('-post_date')[:7]
    #categories=TermTaxonomy.objects.select_related('term').filter(taxonomy='category',count__gt=0).order_by('terms')
    categories=Terms.objects.select_related('term').filter(termtaxonomy__taxonomy='category',termtaxonomy__count__gt=0).order_by('name')
    
    #this sql equal to SELECT YEAR(post_date) AS `year`, MONTH(post_date) AS `month`, count(ID) as posts FROM e_posts  WHERE post_type = 'post' AND post_status = 'publish' GROUP BY YEAR(post_date), MONTH(post_date) ORDER BY post_date DESC
    #archives=Posts.objects.filter(post_status='publish',post_type='post').extra(select={'year':'year(post_date)','month':'month(post_date)'}).values('year','month').annotate(Count('id')).order_by('-post_date')
    #hack to port to mysql and sqlite
    engine=connection.settings_dict['ENGINE']
    archives=[]
    if engine=='django.db.backends.sqlite3':
        archives=Posts.objects.filter(post_status='publish',post_type='post').extra(select={'year':"strftime('%Y',post_date)",'month':"strftime('%m',post_date)"}).values('year','month').annotate(Count('id')).order_by('-post_date')
    elif engine=='django.db.backends.mysql':
        archives=Posts.objects.filter(post_status='publish',post_type='post').extra(select={'year':'year(post_date)','month':'month(post_date)'}).values('year','month').annotate(Count('id')).order_by('-post_date')
    else:
        pass;

    context={
        'recent_posts':recent_posts,
        'recent_comments':recent_comments,
        'categories':categories,
        'archives':archives,
    }
    return render_to_string('sidebar.html',context)

#for post
def comment(request):
    context={'test':'ttestfasdf'}
    context=RequestContext(context)
    return render_to_response('test.html',context)
    pass;

def search(request):
    return page(request)

def cat(request,num='1'):
    #test=TermRelationships.objects.select_related('object').filter(term_taxonomy_id=num,object__post_type='post')
    posts_list=Posts.objects.select_related('termrelationship').filter(termrelationships__term_taxonomy_id=num,post_type='post')
    
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
    post_list=Posts.objects.all()
    
    cats=TermRelationships.objects.select_related('term_taxonomy__term').filter(term_taxonomy__taxonomy__in=('category', 'post_tag', 'post_format'),object_id__in=post_list)
    context={'test':cats}
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

def article(request,post_id):

    context={
    'header':render_header(request),
    'footer':render_footer(request),
    'contents':render_article(post_id),
     'sidebar':render_sidebar(request),
    }
    return render_to_response('index.html',context)

def feed(request,str=''):
    context={}
    return render_to_response('test.html',context) 


def render_header(request):
    context=RequestContext(request) 
    return render_to_string('header.html',context)
def render_footer(request):
    return render_to_string('footer.html')

def render_contents(posts,cat=''):
    cats=TermRelationships.objects.select_related('term_taxonomy__term').filter(term_taxonomy__taxonomy__in=('category', 'post_tag', 'post_format'),object_id__in=posts)
    #cats=Terms.objects.select_related('termtaxonomy').select_related('termrelationships').filter(termtaxonomy__taxonomy__in=('category', 'post_tag', 'post_format'))
    i=0
    for post in posts:
        if i< len(cats):
            post.cat=cats[i].term_taxonomy.term
        else:
            post.cat=None
        i=i+1
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
def render_comment(comment_post_id):
    context={'comment_post_id':comment_post_id}
    return render_to_string('comment.html',context)

def render_page1(posts,num='1',nator=None,comment=None):
    paginator = MyPaginator(posts, 5)
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


def render_article(post_id):
    objs=Posts.objects.all().filter(post_status='publish',post_type='post')
    prev_post=objs.filter(id__lt=post_id).only('id','post_title').last()
    cur_post=Posts.objects.all().filter(id=post_id,post_status='publish',post_type='post')
    next_post=objs.filter(id__gt=post_id).only('id','post_title').first()
    contents=render_contents(cur_post)
    nator=render_nator2(prev_post,next_post)
    return render_page1(cur_post,1,nator,render_comment(post_id))


def render_page(request,num='1'):
    context={}
    if(long(num)<=0):
        num=1
    page=None
    
    post_id=request.GET.get('p')
    if post_id:
        objs=Posts.objects.all().filter(post_status='publish',post_type='post')
        prev_post=objs.filter(id__lt=post_id).only('id','post_title').last()
        cur_post=Posts.objects.all().filter(id=post_id,post_status='publish',post_type='post')
        next_post=objs.filter(id__gt=post_id).only('id','post_title').first()
        contents=render_contents(cur_post)
        nator=render_nator2(prev_post,next_post)
        # context={
        #     'page_contents':contents,
        #     'page_comment':render_comment(post_id),
        #     'page_nator':nator,
        #     }
        return render_page1(cur_post,1,nator,render_comment(post_id))
    else:
        #get post data
        posts_list=Posts.objects.all().filter(post_status='publish',post_type='post').order_by('-post_date')
        return render_page1(posts_list,num)
        # paginator = MyPaginator(posts_list, 5)
        # try:
        #     page=paginator.page(num)
        # except PageNotAnInteger:
        #     page = paginator.page(1)
        # except EmptyPage:
        #     page= paginator.page(paginator.num_pages)
        # contents=render_contents(page)
        # nator=render_nator(page)
        # context={ 
        #     'page_contents':contents,
        #     'page_nator':nator,
        #    }

    return render_to_string('page.html',context)



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
        

