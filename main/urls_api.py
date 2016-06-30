from django.conf.urls import url
from main import views_api

urlpatterns = [

    url(r'^users/$', views_api.UserViewSet.as_view({'get':'list', 'post':'create'}), name='users'),
    url(r'^users/(?P<pk>\d+)$', views_api.UserViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='users'),

    url(r'^categories/$', views_api.CategoryViewSet.as_view({'get':'list', 'post':'create'}), name='categories'),
    url(r'^categories/(?P<pk>\d+)$', views_api.CategoryViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='category'),

    url(r'^subjects/$', views_api.SubjectViewSet.as_view({'get':'list', 'post':'create'}), name='subjects'),
    url(r'^subjects/(?P<pk>\d+)$', views_api.SubjectViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='subject'),

    url(r'^classes/$', views_api.ClassViewSet.as_view({'get':'list', 'post':'create'}), name='classes'),
    url(r'^classes/(?P<pk>\d+)$', views_api.ClassViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='class'),

    url(r'^schedules/$', views_api.ScheduleViewSet.as_view({'get':'list', 'post':'create'}), name='schedules'),
    url(r'^schedules/(?P<pk>\d+)$', views_api.ScheduleViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='schedule'),

    url(r'^student_profiles/$', views_api.StudentProfileViewSet.as_view({'get':'list', 'post':'create'}), name='student_profiles'),
    url(r'^student_profiles/(?P<pk>\d+)$', views_api.StudentProfileViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='student_profile'),

    url(r'^teacher_profiles/$', views_api.TeacherProfileViewSet.as_view({'get':'list', 'post':'create'}), name='teacher_profiles'),
    url(r'^teacher_profiles(?P<pk>\d+)/$', views_api.TeacherProfileViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='teacher_profile'),

    url(r'^image_files/$', views_api.ImageFileViewSet.as_view({'get':'list', 'post':'create'}), name='image_files'),
    url(r'^image_files/(?P<pk>\d+)$', views_api.ImageFileViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='image_file'),

    url(r'^image_links/$', views_api.ImageLinkViewSet.as_view({'get':'list', 'post':'create'}), name='image_links'),
    url(r'^image_links/(?P<pk>\d+)$', views_api.ImageLinkViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='image_link'),

    url(r'^youtube_videos/$', views_api.YoutubeVideoViewSet.as_view({'get':'list', 'post':'create'}), name='youtube_videos'),
    url(r'^youtube_videos/(?P<pk>\d+)$', views_api.YoutubeVideoViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='youtube_video'),

    url(r'^announcements/$', views_api.AnnouncementViewSet.as_view({'get':'list', 'post':'create'}), name='announcements'),
    url(r'^announcements/(?P<pk>\d+)$', views_api.AnnouncementViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='announcement'),

    url(r'^events/$', views_api.EventViewSet.as_view({'get':'list', 'post':'create'}), name='events'),
    url(r'^events(?P<pk>\d+)/$', views_api.EventViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='event'),

    url(r'^polls/$', views_api.PollViewSet.as_view({'get':'list', 'post':'create'}), name='polls'),
    url(r'^polls/(?P<pk>\d+)$', views_api.PollViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='poll'),

    url(r'^choices/$', views_api.ChoiceViewSet.as_view({'get':'list', 'post':'create'}), name='choices'),
    url(r'^choices/(?P<pk>\d+)$', views_api.ChoiceViewSet.as_view({'get': 'retrieve', 'put':'update', 'delete':'destroy'}), name='choice'),

]
