from django.conf.urls.defaults import *
from collection.views import *
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from django.http import HttpResponse
import os.path
#admin.autodiscover()
stylesheet = os.path.join(
    os.path.dirname(__file__), 'stylesheet'
)
scripts = os.path.join(
    os.path.dirname(__file__), 'scripts'
)
images = os.path.join(
    os.path.dirname(__file__), 'images'
)

#files = os.path.join(
#    os.path.dirname(__file__), 'files'
#)
files = '/data/kooking/files'
urlpatterns = patterns('',
    (r'^$',index),
    (r'^category/(\w+)',ranking),
    (r'^kooking_oauth',kooking_oauth),
    (r'^oauth/',oauth),
    (r'^api/plenary',plenary),
    (r'^api/abstention',abstention),
    (r'^api/nonattendance',nonattendance),
    
    
    #(r'^search',search),
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': files} ),
    (r'^stylesheet/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': stylesheet} ),
    (r'^scripts/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': scripts} ),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': images} )

)
