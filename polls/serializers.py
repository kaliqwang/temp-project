from rest_framework import serializers

from models import *
from accounts.models import *
from categories.models import *

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
