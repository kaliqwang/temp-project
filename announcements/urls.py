from django.conf.urls import url

from .views import *

app_name = 'announcements'

urlpatterns = [
    url(r'^$', announcement_list, name='list'),
    url(r'^create$', announcement_create, name='create'),
    url(r'^(?P<pk>\d+)$', announcement_detail, name='detail'),
    url(r'^(?P<pk>\d+)/update$', announcement_update, name='update'),
    url(r'^(?P<pk>\d+)/delete$', announcement_delete, name='delete'),
    url(r'^ytdata/(?P<video_id>[a-zA-Z0-9_-]{11})$', ytdata, name='ytdata'),
    url(r'^generator$', generator, name='generator'),
]
