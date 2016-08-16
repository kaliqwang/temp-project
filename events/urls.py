from django.conf.urls import url

from .views import *

app_name = 'events'

urlpatterns = [
    url(r'^$', event_list, name='list'),
    url(r'^create/$', event_create, name='create'),
    url(r'^(?P<pk>\d+)/$', event_detail, name='detail'),
    url(r'^(?P<pk>\d+)/update/$', event_update, name='update'),
    url(r'^(?P<pk>\d+)/delete/$', event_delete, name='delete'),
    url(r'^generator/(?P<count>\d+)/$', generator, name='generator'),
]
