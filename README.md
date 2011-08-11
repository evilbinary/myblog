Django on OpenShift Express
============================

This git repository helps you get up and running quickly w/ a Django installation
on OpenShift Express.  The Django project name used in this repo is 'openshift'
but you can feel free to change it.  Right now the backend is sqlite3 and the
database runtime is @ $OPENSHIFT_DATA_DIR/sqlite3.db.

When you push this application up for the first time, the sqlite database is
copied from wsgi/openshift/sqlite3.db.  This is the stock database that is created
when 'python manage.py syncdb' is run with only the admin app installed.


Running on OpenShift
----------------------------

Create an account at http://openshift.redhat.com/

Create a wsgi-3.2 application

    rhc-create-app -a django -t wsgi-3.2

Add this upstream seambooking repo

    cd django
    git remote add upstream -m master git://github.com/openshift/django-example.git
    git pull -s recursive -X theirs upstream master
    
Then push the repo upstream

    git push

That's it, you can now checkout your application at:

    http://django-$yourlogin.rhcloud.com

