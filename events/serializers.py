from rest_framework import serializers

from .models import *
from ..categories.models import *

from django.conf import settings
from django.utils.formats import dateformat

from categories.serializers import *

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
            return dateformat.format(obj.date_start, settings.SHORT_DATE_FORMAT)
        return None

    def get_time_start_data(self, obj):
        if obj.time_start:
            return dateformat.format(obj.time_start, settings.TIME_FORMAT)
        return None

    def get_date_end_data(self, obj):
        if obj.date_end:
            return dateformat.format(obj.date_end, settings.SHORT_DATE_FORMAT)
        return None

    def get_time_end_data(self, obj):
        if obj.time_end:
            return dateformat.format(obj.time_end, settings.TIME_FORMAT)
        return None
