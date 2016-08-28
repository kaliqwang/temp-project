from rest_framework import serializers

from .models import *

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(CategorySerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = Category
        fields = ('pk', 'name', 'color')
