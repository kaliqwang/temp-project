# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from rest_framework import serializers

from models import *
from django.contrib.auth.models import User

from django.utils.formats import dateformat

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ('pk', 'name', 'color')

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'username', 'password', 'email')
        read_only_fields = ('pk',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# TODO: Override the create() method in UserProfileViewSet so that you can nest UserSerializer in UserProfileSerializer, and create them both simultaneously by posting to user_profiles
class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    categories_hidden_announcements = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, allow_null=True)
    categories_hidden_announcements_data = CategorySerializer(source='categories_hidden_announcements', many=True)

    class Meta:
        model = UserProfile
        fields = ('pk', 'user', 'mobile', 'is_student', 'is_teacher', 'categories_hidden_announcements', 'categories_hidden_announcements_data')

# TODO: Override the create() method in StudentProfileViewSet so that you can nest UserProfileSerializer in StudentProfileSerializer, and create them all simultaneously by posting to student_profiles
class StudentProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ('pk', 'user_profile', 'student_id', 'grade_level')

# TODO: Override the create() method in TeacherProfileViewSet so that you can nest UserProfileSerializer in TeacherProfileSerializer, and create them all simultaneously by posting to teacher_profiles
class TeacherProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ('pk', 'user_profile', 'room')

class ImageFileSerializer(serializers.HyperlinkedModelSerializer):
    announcement =  serializers.PrimaryKeyRelatedField(queryset=Announcement.objects.all())
    image_file_url = serializers.SerializerMethodField()
    image_file_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageFile
        fields = ('pk', 'announcement', 'image_file_url', 'image_file_thumbnail_url')
        extra_kwargs = {
            'announcement': {'write_only': True},
        }

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ImageFileSerializer, self).__init__(many=many, *args, **kwargs)

    def get_image_file_url(self, obj):
        return obj.image_file.url

    def get_image_file_thumbnail_url(self, obj):
        return obj.image_file_thumbnail.url

class ImageLinkSerializer(serializers.HyperlinkedModelSerializer):
    announcement =  serializers.PrimaryKeyRelatedField(queryset=Announcement.objects.all())
    image_file_url = serializers.SerializerMethodField()
    image_file_thumbnail_url = serializers.SerializerMethodField()

    class Meta:
        model = ImageLink
        fields = ('pk', 'announcement', 'image_link', 'image_file_url', 'image_file_thumbnail_url')
        extra_kwargs = {
            'announcement': {'write_only': True},
        }

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(ImageLinkSerializer, self).__init__(many=many, *args, **kwargs)

    def get_image_file_url(self, obj):
        return obj.image_file.url

    def get_image_file_thumbnail_url(self, obj):
        return obj.image_file_thumbnail.url

class YouTubeVideoSerializer(serializers.HyperlinkedModelSerializer):
    announcement = serializers.PrimaryKeyRelatedField(queryset=Announcement.objects.all())

    class Meta:
        model = YouTubeVideo
        # TODO: download all necessary information from youtube api when saving, and store in database to reduce http requests?
        fields = ('pk', 'announcement', 'title', 'youtube_video')
        extra_kwargs = {
            'announcement': {'write_only': True},
        }

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(YouTubeVideoSerializer, self).__init__(many=many, *args, **kwargs)

class AnnouncementSerializer(serializers.HyperlinkedModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), allow_null=True)
    date_created_data = serializers.SerializerMethodField()
    time_created_data = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    category_data = CategorySerializer(source='category')
    image_files_data = ImageFileSerializer(source='image_files', many=True)
    image_links_data = ImageLinkSerializer(source='image_links', many=True)
    youtube_videos_data = YouTubeVideoSerializer(source='youtube_videos', many=True)

    class Meta:
        model = Announcement
        fields = ('pk', 'absolute_url', 'title', 'author', 'date_created', 'date_created_data', 'time_created_data', 'content', 'category', 'category_data', 'rank', 'image_files_data', 'image_links_data', 'youtube_videos_data')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    # TODO: is it necessary to check for datetimes that are None, given that the field has auto_add_now=True?
    def get_date_created_data(self, obj):
        return dateformat.format(obj.date_created, 'F j')

    def get_time_created_data(self, obj):
        return dateformat.format(obj.date_created, 'P')

class EventSerializer(serializers.HyperlinkedModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    date_start_data = serializers.SerializerMethodField()
    time_start_data = serializers.SerializerMethodField()
    date_end_data = serializers.SerializerMethodField()
    time_end_data = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    category_data = CategorySerializer(source='category')

    class Meta:
        model = Event
        fields = ('pk', 'absolute_url', 'name', 'date_start', 'date_start_data', 'time_start_data', 'date_end_data', 'time_end_data', 'is_multi_day', 'location', 'details', 'category', 'category_data')

    def get_absolute_url(self, obj):
        return obj.get_absolute_url()

    def get_date_start_data(self, obj):
        if obj.date_start:
            return dateformat.format(obj.date_start, 'M j')
        return None

    def get_time_start_data(self, obj):
        if obj.time_start:
            return dateformat.format(obj.time_start, 'P')
        return None

    def get_date_end_data(self, obj):
        if obj.date_end:
            return dateformat.format(obj.date_end, 'M j')
        return None

    def get_time_end_data(self, obj):
        if obj.time_end:
            return dateformat.format(obj.time_end, 'P')
        return None

class PollSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), allow_null=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    choices = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all(), many=True)

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
    voter = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
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
