from rest_framework import serializers

from models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserProfile
        fields = ('user', 'mobile')

class StudentProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = StudentProfile
        fields = ('user_profile', 'student_id', 'grade_level')

class TeacherProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_profile = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())

    class Meta:
        model = TeacherProfile
        fields = ('user_profile', 'room')

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'color')

class ImageFileSerializer(serializers.HyperlinkedModelSerializer):
    announcement =  serializers.PrimaryKeyRelatedField(queryset=Announcement.objects.all())

    class Meta:
        model = ImageFile
        fields = ('announcement', 'image_file',)

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ImageFileSerializer, self).__init__(many=many, *args, **kwargs)

class ImageLinkSerializer(serializers.HyperlinkedModelSerializer):
    announcement =  serializers.PrimaryKeyRelatedField(queryset=Announcement.objects.all())

    class Meta:
        model = ImageLink
        fields = ('announcement', 'image_link',)

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ImageLinkSerializer, self).__init__(many=many, *args, **kwargs)

class YouTubeVideoSerializer(serializers.HyperlinkedModelSerializer):
    announcement =  serializers.PrimaryKeyRelatedField(queryset=Announcement.objects.all())

    class Meta:
        model = YouTubeVideo
        fields = ('announcement', 'title', 'youtube_video')

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(YouTubeVideoSerializer, self).__init__(many=many, *args, **kwargs)

class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    image_files = serializers.PrimaryKeyRelatedField(many=True, queryset=ImageFile.objects.all(), allow_null=True)
    image_links = serializers.PrimaryKeyRelatedField(many=True, queryset=ImageLink.objects.all(), allow_null=True)
    youtube_videos = serializers.PrimaryKeyRelatedField(many=True, queryset=YouTubeVideo.objects.all(), allow_null=True)

    class Meta:
        model = Announcement
        fields = ('title', 'author', 'date_created', 'content', 'category',
                  'rank', 'image_files', 'image_links', 'youtube_videos')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)

    class Meta:
        model = Event
        fields = ('name', 'date_start', 'time_start', 'date_end', 'time_end',
                  'is_multi_day', 'location', 'details', 'category')

class PollSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    choices = serializers.PrimaryKeyRelatedField(many=True, queryset=Choice.objects.all())

    class Meta:
        model = Poll
        fields = ('content', 'author', 'is_open', 'date_open', 'date_close',
                  'category', 'rank', 'choices')

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())

    class Meta:
        model = Choice
        fields = ('content', 'poll')

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    voter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())
    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())

    class Meta:
        model = Vote
        fields = ('voter', 'choice', 'poll')

################################################################################

# class SubjectSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = Subject
#         fields = ('subject',)
#
# class ClassSerializer(serializers.HyperlinkedModelSerializer):
#     subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())
#     teacher = serializers.PrimaryKeyRelatedField(queryset=TeacherProfile.objects.all())
#
#     class Meta:
#         model = Class
#         fields = ('subject', 'teacher', 'room', 'period', 'is_honors', 'is_ap', 'is_dual')
#
# class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
#     classes = serializers.PrimaryKeyRelatedField(many=True, queryset=Class.objects.all())
#
#     class Meta:
#         model = Schedule
#         fields = ('classes',)
