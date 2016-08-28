from rest_framework.viewsets import ModelViewSet
from rest_framework import pagination

from .models import *
from .serializers import *

class EventPaginator(pagination.PageNumberPagination):
    page_size = 30

class EventViewSet(ModelViewSet):
    queryset = Event.objects.none()
    serializer_class = EventSerializer
    pagination_class = EventPaginator

    def get_queryset(self):
        user_profile = self.request.user.profile
        events = Event.objects.exclude(category_id__in=user_profile.categories_hidden_events.values_list('pk'))
        # TODO: allow multiple years and months in the same query
        year = self.request.GET.get('year', None)
        month = self.request.GET.get('month', None)
        if year:
            events = events.filter(date_start__year=int(year))
        if month:
            events = events.filter(date_start__month=int(month))
        return events.reverse()
