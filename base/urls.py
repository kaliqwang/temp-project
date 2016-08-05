from django.conf.urls import url

from views import *

app_name='base'

urlpatterns = [
    # Homepage
    url(r'^$', index, name='index'),
    # Generator
    url(r'^generator/$', generator, name='generator'),
]
