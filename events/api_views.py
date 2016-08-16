from rest_framework.viewsets import ModelViewSet
from rest_framework import pagination

from .models import *
from serializers import *

class EventPaginator(pagination.PageNumberPagination):
    page_size = 100

class EventViewSet(ModelViewSet):
    queryset = Event.objects.none()
    serializer_class = EventSerializer
    pagination_class = EventPaginator

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Event.objects.exclude(category_id__in=user_profile.categories_hidden_announcements.values_list('pk'))
