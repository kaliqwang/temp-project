from django.conf.urls import url

from django.views.generic.base import RedirectView

from views import *

app_name='base'

urlpatterns = [
    # Index
    url(r'^$', index, name='index'),
    # Generator
    url(r'^generator/$', generator, name='generator'),
    # Other (redirect to index page)
    url(r'^.*$', RedirectView.as_view(pattern_name='base:index')),
]
