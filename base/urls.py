from django.conf.urls import url

from django.views.generic.base import RedirectView

from .views import *

app_name='base'

urlpatterns = [
    # Index (redirect to announcements list)
    url(r'^$', RedirectView.as_view(pattern_name='announcements:list'), name='index'),
    # Generator
    url(r'^generator/$', generator, name='generator'),
]
