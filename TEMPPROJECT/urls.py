# TEMPPROJECT URL Configuration https://docs.djangoproject.com/en/1.9/topics/http/urls/

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = []

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^categories/', include('categories.urls')),
    url(r'^announcements/', include('announcements.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^polls/', include('polls.urls')),
    url(r'^', include('base.urls')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
