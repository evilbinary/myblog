#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   Author  :   evilbinary.org
#   E-mail  :   rootntsd@gmail.com
#   Date    :   14/10/1 12:21:19
#   Desc    :   util
import time


try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.
import random
from django.conf import settings
from django.utils.decorators import available_attrs
import hashlib
 
if hasattr(random, 'SystemRandom'):
    randrange = random.SystemRandom().randrange
else:
    randrange = random.randrange
_MAX_CSRF_KEY = 18446744073709551616L     # 2 << 63
 
def _get_new_submit_key():
    return hashlib.md5("%s%s" % (randrange(0, _MAX_CSRF_KEY), settings.SECRET_KEY)).hexdigest()
 
def anti_resubmit(page_key=''):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if request.method == 'GET':
                request.session['%s_submit' % page_key] = _get_new_submit_key()
                print 'session:' + request.session.get('%s_submit' % page_key)
            elif request.method == 'POST':
                old_key = request.session.get('%s_submit' % page_key, '')
                if old_key == '':
                    from django.http import HttpResponseRedirect
                    return HttpResponseRedirect('/blog/page_expir',request)
                request.session['%s_submit' % page_key] = ''
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def anti_frequency(fun):
    def detect(*args,**kwargs):
        request=args[0]
        if request.method=='POST':
            last_comment_time=request.session.get('last_comment_time')
            if last_comment_time==None:
                request.session['last_comment_time']=time.time()
                request.session['frequency_comment']=False
            elif time.time()-last_comment_time <10:
                request.session['frequency_comment']=True
            else:
                request.session['last_comment_time']=time.time()
                request.session['frequency_comment']=False
                pass
        return fun(*args,**kwargs)
    return detect
    pass


def list2tree2(l):
    #{id:(id,pid,child,level)}
    dic={i[0]:[i[0],i[1],[],0] for i in l}
    stack=[]
    for c in dic:
        i=dic[c]
        pid=i[1]
        if pid!=0:
            #print 'dic[%d]:%s'%(pid,dic[pid])
            p=dic[pid]
            #p[2].insert(0,i)
            p[2].append(i)
            i[3]=p[3]+1 
        else:
            stack.insert(0,i)
    result=[]
    while stack:
        top=stack.pop()
        result.append((top[3],top[0]))
        top[2].reverse()
        stack.extend(top[2])
        #stack=stack+top[2][::-1]
        #stack.extend(top[2][::-1])
        #for i in top[2]:
        #   stack.append(i) 
    return result
    pass
