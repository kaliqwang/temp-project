from django.conf.urls import url

from accounts import api_views as accounts_api
from categories import api_views as categories_api
from announcements import api_views as announcements_api
from events import api_views as events_api
from polls import api_views as polls_api
from push_notifications.api.rest_framework import APNSDeviceAuthorizedViewSet
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
app_name = 'api'

router = DefaultRouter()
router.register(r'device/apns', APNSDeviceAuthorizedViewSet)

urlpatterns = [

    url(r'^users/$', accounts_api.UserViewSet.as_view({'get':'list', 'post':'create'}), name='users'),
    url(r'^users/(?P<pk>\d+)$', accounts_api.UserViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='user'),

    url(r'^user_profiles/$', accounts_api.UserProfileViewSet.as_view({'get':'list', 'post':'create'}), name='user_profiles'),
    url(r'^user_profiles/(?P<pk>\d+)$', accounts_api.UserProfileViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='user_profile'),

    url(r'^student_profiles/$', accounts_api.StudentProfileViewSet.as_view({'get':'list', 'post':'create'}), name='student_profiles'),
    url(r'^student_profiles/(?P<pk>\d+)$', accounts_api.StudentProfileViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='student_profile'),

    url(r'^teacher_profiles/$', accounts_api.TeacherProfileViewSet.as_view({'get':'list', 'post':'create'}), name='teacher_profiles'),
    url(r'^teacher_profiles(?P<pk>\d+)/$', accounts_api.TeacherProfileViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='teacher_profile'),

    url(r'^categories/$', categories_api.CategoryViewSet.as_view({'get':'list', 'post':'create'}), name='categories'),
    url(r'^categories/(?P<pk>\d+)$', categories_api.CategoryViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='category'),

    url(r'^announcements/$', announcements_api.AnnouncementViewSet.as_view({'get':'list', 'post':'create'}), name='announcements'),
    url(r'^announcements/(?P<pk>\d+)$', announcements_api.AnnouncementViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='announcement'),

    url(r'^image_files/$', announcements_api.ImageFileViewSet.as_view({'get':'list', 'post':'create'}), name='image_files'),
    url(r'^image_files/(?P<pk>\d+)$', announcements_api.ImageFileViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='image_file'),

    url(r'^image_links/$', announcements_api.ImageLinkViewSet.as_view({'get':'list', 'post':'create'}), name='image_links'),
    url(r'^image_links/(?P<pk>\d+)$', announcements_api.ImageLinkViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='image_link'),

    url(r'^youtube_videos/$', announcements_api.YouTubeVideoViewSet.as_view({'get':'list', 'post':'create'}), name='youtube_videos'),
    url(r'^youtube_videos/(?P<pk>\d+)$', announcements_api.YouTubeVideoViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='youtube_video'),

    url(r'^events/$', events_api.EventViewSet.as_view({'get':'list', 'post':'create'}), name='events'),
    url(r'^events(?P<pk>\d+)/$', events_api.EventViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='event'),

    url(r'^polls/$', polls_api.PollViewSet.as_view({'get':'list', 'post':'create'}), name='polls'),
    url(r'^polls/(?P<pk>\d+)$', polls_api.PollViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='poll'),

    url(r'^choices/$', polls_api.ChoiceViewSet.as_view({'get':'list', 'post':'create'}), name='choices'),
    url(r'^choices/(?P<pk>\d+)$', polls_api.ChoiceViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='choice'),

    url(r'^votes/$', polls_api.VoteViewSet.as_view({'get':'list', 'post':'create'}), name='votes'),
    url(r'^votes/(?P<pk>\d+)$', polls_api.VoteViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='vote'),

    # url(r'^', include(router.urls)),
    # url(r'^subjects/$', views_api.SubjectViewSet.as_view({'get':'list', 'post':'create'}), name='subjects'),
    # url(r'^subjects/(?P<pk>\d+)$', views_api.SubjectViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='subject'),
    #
    # url(r'^classes/$', views_api.ClassViewSet.as_view({'get':'list', 'post':'create'}), name='classes'),
    # url(r'^classes/(?P<pk>\d+)$', views_api.ClassViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='class'),
    #
    # url(r'^schedules/$', views_api.ScheduleViewSet.as_view({'get':'list', 'post':'create'}), name='schedules'),
    # url(r'^schedules/(?P<pk>\d+)$', views_api.ScheduleViewSet.as_view({'get': 'retrieve', 'put':'partial_update', 'delete':'destroy'}), name='schedule'),

]
