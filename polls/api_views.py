from rest_framework.viewsets import ModelViewSet
from rest_framework import pagination

from .models import *
from .serializers import *

class PollPaginator(pagination.PageNumberPagination):
    page_size = 36

class PollViewSet(ModelViewSet):
    queryset = Poll.objects.none()
    serializer_class = PollSerializer
    pagination_class = PollPaginator

    def get_queryset(self):
        user_profile = self.request.user.profile
        polls = Poll.objects.exclude(category_id__in=user_profile.categories_hidden_announcements.values_list('pk'))
        polls_voted_id_list = self.request.user.profile.votes.values('poll_id')

        is_open = self.request.GET.get('is_open', None)
        is_voted = self.request.GET.get('is_voted', None)

        if is_open == 'True':
        	polls = polls.filter(is_open=True)
        elif is_open == 'False':
          	polls = polls.exclude(is_open=True)

        if is_voted == 'True':
          	polls = polls.filter(pk__in=polls_voted_id_list)
        elif is_voted == 'False':
          	polls = polls.exclude(pk__in=polls_voted_id_list)

        return polls

class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class VoteViewSet(ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
