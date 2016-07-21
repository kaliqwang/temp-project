from rest_framework.viewsets import ModelViewSet
from models import *
from serializers import *


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
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


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
#
# class ClassViewSet(ModelViewSet):
#     queryset = Class.objects.all()
#     serializer_class = ClassSerializer
#
#
# class ScheduleViewSet(ModelViewSet):
#     queryset = Schedule.objects.all()
#     serializer_class = ScheduleSerializer
