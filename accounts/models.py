from __future__ import unicode_literals

from numpy import random

from datetime import datetime, date, time, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from categories.models import *

from base.models import GetOrNoneManager, mobile_validator, student_id_validator, first_names, last_names

################################################################################

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', null=True)
    # TODO: set mobile to unique = True in production
    mobile = models.CharField("Phone Number", max_length=10, validators=[mobile_validator])
    # TODO: create a signal (or just update save function of related model) that automatically sets these values when a related student/teacher profile object is saved
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    categories_hidden_announcements = models.ManyToManyField(Category, related_name="user_profiles_with_category_hidden_for_announcements", blank=True)
    categories_hidden_events = models.ManyToManyField(Category, related_name="user_profiles_with_category_hidden_for_events", blank=True)
    categories_hidden_polls = models.ManyToManyField(Category, related_name="user_profiles_with_category_hidden_for_polls", blank=True)

    objects = GetOrNoneManager()

    def __str__(self):
        return self.user.get_full_name()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = self.user.pk
        super(UserProfile, self).save(*args, **kwargs)

class StudentProfile(models.Model):
    FRESHMAN = 0
    SOPHOMORE = 1
    JUNIOR = 2
    SENIOR = 3
    GRADE_LEVEL_CHOICES = (
        (FRESHMAN, 'Freshman'),
        (SOPHOMORE, 'Sophomore'),
        (JUNIOR, 'Junior'),
        (SENIOR, 'Senior'),
    )
    user_profile = models.OneToOneField(UserProfile, related_name='student_profile', null=True)
    # TODO: set student_id to unique = True in production
    student_id = models.CharField("Student ID", max_length=10, validators=[student_id_validator])
    grade_level = models.IntegerField("Grade Level", default=FRESHMAN, choices=GRADE_LEVEL_CHOICES)

    objects = GetOrNoneManager()

    def __str__(self):
        return '%s - student profile' % self.user_profile

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = self.user_profile.user.pk
        super(StudentProfile, self).save(*args, **kwargs)

    @classmethod
    def generate_random_objects(cls, count):
        rand_1 = random.randint(140, size=count)
        rand_2 = random.randint(140, size=count)
        rand_3 = random.randint(1100000000, 1100999999, size=count)
        rand_4 = random.randint(3, size=count)

        user_pk = User.objects.latest('pk').pk + 1
        generated_count = 0
        for i in range(0, count):
            first_name = first_names[rand_1.item(i)]
            last_name = last_names[rand_2.item(i)]
            student_id = rand_3.item(i)
            grade_level = rand_4.item(i)
            user = User.objects.create_user(
                username=user_pk,
                password=user_pk,
                first_name=first_name,
                last_name=last_name,
            )
            user_profile = UserProfile.objects.create(
                user=user,
                mobile='6787901506',
                is_student=True,
            )
            student_profile= StudentProfile.objects.create(
                user_profile=user_profile,
                student_id = student_id,
                grade_level=grade_level,
            )
            user_pk += 1
            generated_count += 1
            print('Generated StudentProfile %d (UserProfile %d User %d)' %(student_profile.pk, user_profile.pk, user.pk))
        return generated_count

class TeacherProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, related_name='teacher_profile', null=True)
    room = models.CharField("Room Number", unique=True, max_length=6)

    objects = GetOrNoneManager()

    def __str__(self):
        return '%s - teacher profile' % self.user_profile

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = self.user_profile.user.pk
        super(TeacherProfile, self).save(*args, **kwargs)
