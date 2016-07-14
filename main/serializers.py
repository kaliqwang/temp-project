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

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'color')


class SubjectSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Subject
        fields = ('subject',)


class ClassSerializer(serializers.HyperlinkedModelSerializer):

    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all())
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=TeacherProfile.objects.all())

    class Meta:
        model = Class
        fields = ('subject', 'teacher', 'room', 'period',
                  'is_honors', 'is_ap', 'is_dual')


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):

    classes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Class.objects.all())

    class Meta:
        model = Schedule
        fields = ('classes',)


class StudentProfileSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    schedule = serializers.PrimaryKeyRelatedField(
        queryset=Schedule.objects.all())

    class Meta:
        model = StudentProfile
        fields = ('user', 'student_id', 'grade_level', 'schedule')


class TeacherProfileSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    schedule = serializers.PrimaryKeyRelatedField(queryset=Schedule.objects.all())

    class Meta:
        model = TeacherProfile
        fields = ('user', 'room', 'schedule')
        # broken: user
        # not-broken: schedule


class ImageFileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ImageFile
        fields = ('image_file',)


class ImageLinkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ImageLink
        fields = ('image_link',)


class YoutubeVideoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = YoutubeVideo
        fields = ('youtube_video', 'title')


class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    image_files = serializers.PrimaryKeyRelatedField(many=True, queryset=ImageFile.objects.all(), allow_null=True)
    image_links = serializers.PrimaryKeyRelatedField(many=True, queryset=ImageLink.objects.all(), allow_null=True)
    youtube_videos = serializers.PrimaryKeyRelatedField(many=True, queryset=YoutubeVideo.objects.all(), allow_null=True)

    class Meta:
        model = Announcement
        fields = ('author', 'title', 'category', 'date_created', 'content',
                  'image_files', 'image_links', 'youtube_videos', 'rank')


class EventSerializer(serializers.HyperlinkedModelSerializer):

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)

    class Meta:
        model = Event
        fields = ('name', 'category', 'location', 'date_start',
                  'time_start', 'date_end', 'time_end', 'details')


class PollSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)

    class Meta:
        model = Poll
        fields = ('content', 'category', 'author',
                  'date_created', 'date_closed', 'is_open', 'rank')


class ChoiceSerializer(serializers.HyperlinkedModelSerializer):

    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())

    class Meta:
        model = Choice
        fields = ('poll', 'content')

class VoteSerializer(serializers.HyperlinkedModelSerializer):

    voter = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())
    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())

    class Meta:
        model = Vote
        fields = ('voter', 'choice', 'poll')
