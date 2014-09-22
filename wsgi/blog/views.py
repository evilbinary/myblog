from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from blog.models import Posts
from django.http import HttpResponse
from django.template.loader import render_to_string

def archive(request):
    posts=Posts.objects.all().filter(post_status='publish',post_type='post')
    t=loader.get_template('archive.html')
    c=Context({'posts':posts})
    return HttpResponse(t.render(c))
def get_header(request):
    context=RequestContext(request) 
    return render_to_string('header.html',context)
def get_footer(request):
    return render_to_string('footer.html')

def index(request):
    header=get_header(request)
    footer=get_footer(request)
    contents=get_content(request)
    sidebar=get_sidebar(request)
    context={'header':header,
        'contents':contents,
        'sidebar':sidebar,
        'footer':footer}
    return render_to_response('index.html',context)
def get_content(request):
    posts=Posts.objects.all().filter(post_status='publish',post_type='post').order_by('-post_date')
    context={'posts':posts}
    return render_to_string('content.html',context)

def get_sidebar(request):
    context={}
    return render_to_string('sidebar.html',context)
