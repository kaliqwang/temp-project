from django.conf.urls import url
from main import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^announcements/$', views.announcement_list, name='announcement-list'),
    url(r'^announcements/create/$', views.announcement_create, name='announcement-create'),
    url(r'^announcements/(?P<pk>\d+)/$', views.announcement_detail, name='announcement-detail'),
    url(r'^announcements/(?P<pk>\d+)/update/$', views.announcement_update, name='announcement-update'),
    url(r'^announcements/(?P<pk>\d+)/delete/$', views.announcement_delete, name='announcement-delete'),

    url(r'^events/$', views.event_list, name='event-list'),
    url(r'^events/create/$', views.event_create, name='event-create'),
    url(r'^events/(?P<pk>\d+)/$', views.event_detail, name='event-detail'),
    url(r'^events/(?P<pk>\d+)/update/$', views.event_update, name='event-update'),
    url(r'^events/(?P<pk>\d+)/delete/$', views.event_delete, name='event-delete'),

    url(r'^polls/$', views.poll_list, name='poll-list'),
    url(r'^polls/create/$', views.poll_create, name='poll-create'),
    url(r'^polls/(?P<pk>\d+)/$', views.poll_detail, name='poll-detail'),
    url(r'^polls/(?P<pk>\d+)/update/$', views.poll_update, name='poll-update'),
    url(r'^polls/(?P<pk>\d+)/delete/$', views.poll_delete, name='poll-delete'),
    url(r'^get_vote/(?P<poll_pk>\d+)/$', views.get_vote, name='get_vote'),

    url(r'^categories/$', views.category_list, name='category-list'),
    url(r'^register/$', views.register, name='register'),

    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),

    url(r'^ytdata/(?P<video_id>[a-zA-Z0-9_-]{11})/$', views.ytdata, name='ytdata'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
