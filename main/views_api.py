from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework import pagination

from models import *
from serializers import *

class AnnouncementPaginator(pagination.PageNumberPagination):
    page_size = 36

class EventPaginator(pagination.PageNumberPagination):
    page_size = 100

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class StudentProfileViewSet(ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

class TeacherProfileViewSet(ModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AnnouncementViewSet(ModelViewSet):
    queryset = Announcement.objects.none()
    serializer_class = AnnouncementSerializer
    pagination_class = AnnouncementPaginator

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Announcement.objects.exclude(category_id__in=user_profile.categories_hidden_announcements.values_list('pk'))

class EventViewSet(ModelViewSet):
    queryset = Event.objects.none()
    serializer_class = EventSerializer
    pagination_class = EventPaginator

    def get_queryset(self):
        user_profile = self.request.user.profile
        return Event.objects.exclude(category_id__in=user_profile.categories_hidden_announcements.values_list('pk'))

class PollViewSet(ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class ChoiceViewSet(ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

class VoteViewSet(ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

class ImageFileViewSet(ModelViewSet):
    queryset = ImageFile.objects.all()
    serializer_class = ImageFileSerializer

class ImageLinkViewSet(ModelViewSet):
    queryset = ImageLink.objects.all()
    serializer_class = ImageLinkSerializer

class YouTubeVideoViewSet(ModelViewSet):
    queryset = YouTubeVideo.objects.all()
    serializer_class = YouTubeVideoSerializer

# class SubjectViewSet(ModelViewSet):
#     queryset = Subject.objects.all()
#     serializer_class = SubjectSerializer
#
# class ClassViewSet(ModelViewSet):
#     queryset = Class.objects.all()
#     serializer_class = ClassSerializer
#
# class ScheduleViewSet(ModelViewSet):
#     queryset = Schedule.objects.all()
#     serializer_class = ScheduleSerializer
