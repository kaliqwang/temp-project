# from __future__ import unicode_literals
#
# from rest_framework import serializers
#
# from .models import *
#
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
