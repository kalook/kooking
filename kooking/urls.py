from django.conf.urls.defaults import *
from collection.views import *
from admin.views import *

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
files = '/data/fpage/files'
urlpatterns = patterns('',
    (r'^$',index),
    #(r'^page/(\d+)',index),
    (r'^category/(\w+)/page/(\d+)',index),
    (r'^category/(\w+)',index),
    (r'^pageinfo/(\w+)/page/(\d+)',pageinfo),
    
   	(r'^detail/(\w+)',detail),
    (r'^info/',info),
    (r'^event/(\w+)',event),
    (r'^events/(\w+)/(\d+)',events),

    (r'^admin/events/create/',eventmanagement_create),
    (r'^admin/events/view/(\w+)',eventmanagement_view),
    (r'^admin/events/modify/(\w+)',eventmanagement_modify),
    (r'^admin/events/(\w+)',eventmanagement_list),


    (r'^goods/',goods),
    (r'^marketing/',marketing),
    (r'^validate/',validate),
    (r'^admin/event_management/',event_management),
    (r'^admin/event_download/(\w+)',event_download),
    (r'^admin/counselling/(\w+)/',counselling),
    (r'^admin/counselling_view/(\w+)',counselling_view),
    (r'^admin/counselling_delete/(\w+)',counselling_delete),
    (r'^admin/status/',status),
    (r'^admin/page/(\d+)',adminpage),
    (r'^admin',adminpage),

	(r'^logout/',logout),
    (r'^popup/',popup),
    (r'^event_oauth/',event_oauth),
    (r'^image_proxy/',image_proxy),
    (r'^url_proxy/',url_proxy),
    (r'^script_proxy/',script_proxy),


    #(r'^search',search),
    (r'^files/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': files} ),
    (r'^stylesheet/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': stylesheet} ),
    (r'^scripts/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': scripts} ),
    (r'^images/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': images} )

)
