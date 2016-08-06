from rest_framework import serializers

from models import *
from accounts.models import *
from categories.models import *

from django.conf import settings
from django.utils.formats import dateformat

from categories.serializers import *

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    voter = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.all())
    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())

    class Meta:
        model = Vote
        fields = ('pk', 'voter', 'choice', 'poll')

class ChoiceSerializer(serializers.HyperlinkedModelSerializer):
    poll = serializers.PrimaryKeyRelatedField(queryset=Poll.objects.all())

    class Meta:
        model = Choice
        fields = ('pk', 'poll', 'content', 'vote_count')

class PollSerializer(serializers.HyperlinkedModelSerializer):
    absolute_url = serializers.SerializerMethodField()
    author = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), allow_null=True)
    date_open_data = serializers.SerializerMethodField()
    time_open_data = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True)
    category_data = CategorySerializer(source='category')
    choices_data = ChoiceSerializer(source='choices', many=True)

    class Meta:
        model = Poll
        fields = ('pk', 'absolute_url', 'content', 'author', 'is_open', 'date_open', 'date_close',
                  'category', 'rank', 'total_vote_count', 'choices_data', 'date_open_data', 'time_open_data', 'category_data')

    def get_absolute_url(self, obj):
    	return obj.get_absolute_url()

    def get_date_open_data(self, obj):
        return dateformat.format(obj.date_open, settings.LONG_DATE_FORMAT)

    def get_time_open_data(self, obj):
        return dateformat.format(obj.date_open, settings.TIME_FORMAT)
