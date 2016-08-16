from django.conf.urls import url

from .views import *

app_name = 'accounts'

urlpatterns = [
    url(r'^parent_register/$', parent_register, name='register-parent'),
    url(r'^student_register/$', student_register, name='register-student'),
    url(r'^teacher_register/$', teacher_register, name='register-teacher'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^(?P<model>[a-z_]+)/generator/(?P<count>\d+)/$', generator, name='generator'),
]
