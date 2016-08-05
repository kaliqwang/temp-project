from django.conf.urls import url

from views import *

app_name = 'polls'

urlpatterns = [
    url(r'^$', poll_list, name='list'),
    url(r'^create/$', poll_create, name='create'),
    url(r'^(?P<pk>\d+)/$', poll_detail, name='detail'),
    url(r'^(?P<pk>\d+)/update/$', poll_update, name='update'),
    url(r'^(?P<pk>\d+)/delete/$', poll_delete, name='delete'),
    url(r'^generator/(?P<count>\d+)/$', generator, name='generator'),
    url(r'^get_vote/(?P<poll_pk>\d+)/$', get_vote, name='get_vote'),
    url(r'^get_vote_count/(?P<choice_pk>\d+)/$', get_vote_count, name='get_vote_count'),
]
