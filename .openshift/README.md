# Django Template for OpenShift

## Template App Information
Product: Django  
Version: 1.4  
Source:  https://github.com/django/django.git  
Commit:  2591fb8d4c0246f68b79554976c012039df75359

## Maintenance
This folder contains a diff file that includes the changes made to the
stock Django app in order to make it OpenShift-Template-ready. If
you are a maintainer tasked with updating the Django template, you
may be able to use this patch file on the updated Django code to
automatically reapply these changes.

Here are the steps involved:

1. Under the 'wsgi' directory, apply any patches required to update the 'openshift' Django app.
2. From the template root directory, run 'git apply --check .openshift/template.patch' to test for patching problems.
3. Next run 'git am --signoff < .openshift/template.patch' to apply the patch to the template.

If this process succeeds, then the changes have been automatically
applied. Otherwise it may be necessary to manually apply the
changes. If the base package has changed enough, you may need to
re-audit the base code and generate a new patch file.
