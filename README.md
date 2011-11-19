Django on OpenShift Express
============================

This git repository helps you get up and running quickly w/ a Django installation
on OpenShift Express.  The Django project name used in this repo is 'openshift'
but you can feel free to change it.  Right now the backend is sqlite3 and the
database runtime is @ $OPENSHIFT_DATA_DIR/sqlite3.db.

When you push this application up for the first time, the sqlite database is
copied from wsgi/openshift/sqlite3.db.  This is the stock database that is created
when 'python manage.py syncdb' is run with only the admin app installed.

You can delete the database from your git repo after the first push (you probably
should for security).  On subsequent pushes, a 'python manage.py syncdb' is
executed to make sure that any models you added are created in the DB.  If you
do anything that requires an alter table, you could add the alter statements
in GIT_ROOT/.openshift/action_hooks/alter and then use
GIT_ROOT/.openshift/action_hooks/build to execute that script (make sure to
back up your database w/ rhc-snapshot first :) )


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

That's it, you can now checkout your application at (default admin account is admin/admin):

    http://django-$yournamespace.rhcloud.com

