from django.conf.urls import url

from views import *

app_name = 'categories'

urlpatterns = [
    url(r'^$', category_list, name='list'),
]
