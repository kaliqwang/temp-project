from rest_framework.viewsets import ModelViewSet
from rest_framework import pagination

from .models import *
from .serializers import *

class AnnouncementPaginator(pagination.PageNumberPagination):
    page_size = 20

class AnnouncementViewSet(ModelViewSet):
    queryset = Announcement.objects.none()
    serializer_class = AnnouncementSerializer
    pagination_class = AnnouncementPaginator

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Announcement.objects.exclude(category_id__in=user_profile.categories_hidden_announcements.values_list('pk'))

class ImageFileViewSet(ModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer

class ImageLinkViewSet(ModelViewSet):
    queryset = ImageLink.objects.all()
    serializer_class = ImageLinkSerializer

class YouTubeVideoViewSet(ModelViewSet):
    queryset = YouTubeVideo.objects.all()
    serializer_class = YouTubeVideoSerializer
