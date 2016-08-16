from rest_framework import serializers

from .models import *
from ..categories.models import *
from django.contrib.auth.models import User

from categories.serializers import *

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
