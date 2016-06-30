from django.conf.urls import url
from main import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^announcements/$', views.announcement_list, name='announcements'),
    url(r'^announcement_create/$', views.announcement_create, name='announcement_create'),
    url(r'^announcement_update/$', views.AnnouncementUpdate.as_view(), name='announcement_update'),
    url(r'^announcement_delete/$', views.AnnouncementDelete.as_view(), name='announcement_delete'),

    url(r'^events/$', views.EventList.as_view(), name='events'),
    url(r'^event_create/$', views.event_create, name='event_create'),
    url(r'^event_update/$', views.EventUpdate.as_view(), name='event_update'),
    url(r'^event_delete/$', views.EventDelete.as_view(), name='event_delete'),

    url(r'^polls/$', views.PollList.as_view(), name='polls'),
    url(r'^poll_create/$', views.poll_create, name='poll_create'),
    url(r'^poll_update/$', views.PollUpdate.as_view(), name='poll_update'),
    url(r'^poll_delete/$', views.PollDelete.as_view(), name='poll_delete'),

    url(r'^category_create/$', views.category_create, name='category_create'),
    url(r'^student_register/$', views.student_register, name='student_register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
