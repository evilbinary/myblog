#MyBlog
=========
"myblog"是清凉干净的一个开源django的博客,你可以随时下载使用。
#特点
* 兼容wordpress博客系统,数据从wordpress迁移过来毫无压力。
* 支持markdown，SyntaxHighlighter语法高亮功能。
* 支持多种数据库(sqlite、mysql等)。
	
	
# 在线演示
* [http://evilbinary.org](http://evilbinary.org) (这里是个人[博客地址](http://evilbinary.org)，也就是用本开源软件搭建的。)
* [https://github.com/evilbinary/myblog](https://github.com/evilbinary/myblog) （源码地址 ）

#截图
* 博客首页 ![前台博客](https://github.com/evilbinary/myblog/raw/master/data/screen-shot1.png)
* 博客后台管理  ![前台博客](https://github.com/evilbinary/myblog/raw/master/data/screen-shot2.png)
* 喜欢就支持一下，增加作者完善得动力. ![喜欢就支持一下](https://github.com/evilbinary/myblog/raw/master/data/s.png)

#安装说明
===================
##OS X
在苹果系统下安装很容易，首先下载源码，可以直接点击download下载，[猛击这里，注意安全！](https://github.com/evilbinary/myblog/archive/master.zip)，也可以在shell下输入:
	
	git clone https://github.com/evilbinary/myblog.git
	
下载好后，如果是压缩包记得解压，进去后可以看到setup.py这个就是安装文件了，注意你需要有python环境,运行:
	
	python setup.py install
	
然后让它自己安装，安装好后，到wsgi文件夹里面，有个叫mysite这个就是项目的路径，其他的文件不用管了，测试的东西，的点击进去，可以看到blog、manage.py、templates等，然后运行：

	python manage.py collectstatic
	python manage.py syncdb 
同步一下数据库，可能叫你输入第一次创建超级用户，你就输入一个用户，还有密码，成功后应该有个db.sqlite文件出来，再次运行：
	
	python manage.py runserver
	
如果没看到错误，那就可以启动服务器了，让后打开浏览器输入:[http://localhost:8000/](http://localhost:8000/)就可以看到界面了。
##Linux
同mac一样的操作

##Windows
目前，还没时间搞，谁可以帮我测试测试看看，谢谢。

#正式环境部署
===================
如果有app engine之类的账号，比如openshift就可以在上面使用了。

##使用用openshift-v3搭建

使用制作好的docker[镜像](https://hub.docker.com/r/evilbinary/myblog/)

	docker pull evilbinary/myblog
	oc new-app  --docker-image=evilbinary/myblog


##使用用openshift-v2搭建
###1. MyBlog在OpenShift上使用


This git repository helps you get up and running quickly w/ a Django
installation on OpenShift.  The Django project name used in this repo
is 'openshift' but you can feel free to change it.  Right now the
backend is sqlite3 and the database runtime is found in
`$OPENSHIFT_DATA_DIR/sqlite3.db`.

Before you push this app for the first time, you will need to change
the [Django admin password](#admin-user-name-and-password).
Then, when you first push this
application to the cloud instance, the sqlite database is copied from
`wsgi/openshift/sqlite3.db` with your newly changed login
credentials. Other than the password change, this is the stock
database that is created when `python manage.py syncdb` is run with
only the admin app installed.

On subsequent pushes, a `python manage.py syncdb` is executed to make
sure that any models you added are created in the DB.  If you do
anything that requires an alter table, you could add the alter
statements in `GIT_ROOT/.openshift/action_hooks/alter.sql` and then use
`GIT_ROOT/.openshift/action_hooks/deploy` to execute that script (make
sure to back up your database w/ `rhc app snapshot save` first :) )

You can also turn on the DEBUG mode for Django application using the
`rhc env set DEBUG=True --app APP_NAME`. If you do this, you'll get
nicely formatted error pages in browser for HTTP 500 errors.

Do not forget to turn this environment variable off and fully restart
the application when you finish:

```
$ rhc env unset DEBUG
$ rhc app stop && rhc app start
```

###2. Running on OpenShift
--------------------

Create an account at https://www.openshift.com

Install the RHC client tools if you have not already done so:
    
    sudo gem install rhc
    rhc setup

Create a python application

    rhc app create django python-2.6

Add this upstream repo

    cd django
    git remote add upstream -m master git://github.com/openshift/django-example.git
    git pull -s recursive -X theirs upstream master

Then push the repo upstream

    git push

Here, the [admin user name and password will be displayed](#admin-user-name-and-password), so pay
special attention.
	
That's it. You can now checkout your application at:

    http://django-$yournamespace.rhcloud.com

###3. Admin user name and password
----------------------------
As the `git push` output scrolls by, keep an eye out for a
line of output that starts with `Django application credentials: `. This line
contains the generated admin password that you will need to begin
administering your Django app. This is the only time the password
will be displayed, so be sure to save it somewhere. You might want 
to pipe the output of the git push to a text file so you can grep for
the password later.
