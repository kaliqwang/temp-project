from rest_framework import serializers

from .models import *
from accounts.models import *
from categories.models import *

from django.conf import settings
from django.utils.formats import dateformat

from categories.serializers import *

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
        return dateformat.format(obj.date_created, settings.SHORT_DATE_FORMAT)

    def get_time_created_data(self, obj):
        return dateformat.format(obj.date_created, settings.TIME_FORMAT)
