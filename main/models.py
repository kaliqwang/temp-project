# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from django.core.validators import RegexValidator

from django.utils import timezone
from datetime import datetime, date, time, timedelta

from colorful.fields import RGBColorField

import urllib2
import json

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

colors = [
    '#f2f3f4', '#222222',
    '#f3c300', '#875692',
    '#f38400', '#a1caf1',
    '#be0032', '#c2b280',
    '#848482', '#008856',
    '#e68fac', '#0067a5',
    '#f99379', '#604e97',
    '#f6a600', '#b3446c',
    '#dcd300', '#882d17',
    '#8db600', '#654522',
    '#e25822', '#2b3d26'
]

FRESHMAN = 0
SOPHOMORE = 1
JUNIOR = 2
SENIOR = 3

grade_levels = (
    (FRESHMAN, 'Freshman'),
    (SOPHOMORE, 'Sophomore'),
    (JUNIOR, 'Junior'),
    (SENIOR, 'Senior'),
)

student_id_validator = RegexValidator(
    regex=r'^\d{10}$', message='Please enter a valid student ID')

phone_validator = RegexValidator(
    regex=r'^\d{10}$', message="Must be a 10 digit phone number")

class GetOrNoneManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

class Category(models.Model):

    #TODO: create a feature where people can combine categories into a single category and apply it to the correct announcements, events, etc.

    name = models.CharField(max_length=50)
    color = RGBColorField(unique=True, colors=colors)

    objects = GetOrNoneManager()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def display_color(self):
        return '<div style="width: 16px; height:16px; background-color: %s"></div>' % self.color
    display_color.short_description = 'Color'
    display_color.allow_tags = True

    def display_color_and_name(self):
        return '<span style="border-left: 5px solid %s; padding-left: 5px">%s</span>' % (self.color, self.name)
        # return '<li type="circle" style="color:%s;line-height:16px">%s</li>'
        # % (self.color, self.name)
    display_color_and_name.short_description = 'Color'
    display_color_and_name.allow_tags = True

periods = (
    ('1', 'Period 1'),
    ('2', 'Period 2'),
    ('3', 'Period 3'),
    ('4', 'Period 4'),
    ('5a','Period 5A'),
    ('5b','Period 5B'),
    ('6', 'Period 6'),
    ('7', 'Period 7'),
)

class Subject(models.Model):
    subject = models.CharField(max_length=50)

    objects = GetOrNoneManager()

    def __str__(self):
        return self.subject

class Class(models.Model):
    subject = models.ForeignKey('Subject', related_name='classes', blank=True, null=True, on_delete=models.SET_NULL)
    teacher = models.ForeignKey('TeacherProfile', related_name='classes', blank=True, null=True)
    room = models.CharField('Room Number', max_length=6)
    period = models.CharField(max_length=2, choices=periods)
    is_honors = models.BooleanField(default=False)
    is_ap = models.BooleanField(default=False)
    is_dual = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.subject, self.teacher)

    class Meta:
        unique_together = ('teacher', 'period')

class Schedule(models.Model):
    classes = models.ManyToManyField(Class, related_name='schedules_included')

    def __str__(self):
        return '%s\'s Schedule' % self.user

    #TODO: validate overlapping classes by period

class ParentProfile(models.Model):
    user = models.OneToOneField(User, related_name='parent_profile')
    mobile = models.CharField("Phone Number", unique=True, validators=[
                              phone_validator], max_length=10)

    objects = GetOrNoneManager()

    def __str__(self):
        return self.user.get_full_name()

class StudentProfile(models.Model):
    user = models.OneToOneField(User, related_name='student_profile')
    student_id = models.CharField("Student ID", unique=True, validators=[
                                  student_id_validator], max_length=10)
    grade_level = models.IntegerField("Grade Level", choices=grade_levels, default=FRESHMAN)
    schedule = models.OneToOneField(Schedule, related_name='student_profile', blank=True, null=True)

    mobile = models.CharField("Phone Number", unique=True, validators=[
                              phone_validator], max_length=10, default="secret :)")

    objects = GetOrNoneManager()

    def __str__(self):
        return self.user.get_full_name()

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, related_name='teacher_profile')
    room = models.CharField("Room Number", max_length=6, unique=True)
    schedule = models.OneToOneField(Schedule, related_name='teacher_profile', blank=True, null=True)

    mobile = models.CharField("Phone Number", unique=True, validators=[
                              phone_validator], max_length=10, default="secret :)")

    objects = GetOrNoneManager()

    def __str__(self):
        return self.user.get_full_name()

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, related_name='announcements', on_delete=models.SET_NULL, blank=True, null=True)
    author = models.ForeignKey(User, related_name="announcements",
                               on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    content = models.TextField()

    rank = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('-rank', '-date_created')

    def __str__(self):
        return "%s (%s)" % (self.title, self.category)

    @classmethod
    def get_top_rank(cls):
        return cls.objects.all().first().rank

    def pin(self):
        self.rank = Announcement.get_top_rank() + 1
        self.save()

    def unpin(self):
        self.rank = 0
        self.save()

    # call this with daily script
    @classmethod
    def clean_ranks(cls):
        pinned = Announcement.objects.filter(rank__gt=0).reverse()
        i = 1
        for a in pinned:
            a.rank = i
            a.save()
            i += 1

class ImageFile(models.Model):
    image_file = models.ImageField(upload_to='main/images/')
    announcement = models.ForeignKey(Announcement, related_name='image_files', on_delete=models.CASCADE)

    def __str__(self):
        return self.image_file.name

class ImageLink(models.Model):
    image_link = models.URLField()
    announcement = models.ForeignKey(Announcement, related_name='image_links', on_delete=models.CASCADE)

    def __str__(self):
        return self.image_link

class YoutubeVideo(models.Model):
    title = models.CharField('Video Title', max_length=200, blank=True)
    youtube_video = models.CharField('Youtube Video ID', max_length=11)
    announcement = models.ForeignKey(Announcement, related_name='youtube_videos', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    #TODO: perform validation in html form

    def clean(self):
        req = urllib2.Request('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=' + self.youtube_video + '&format=json')
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError:
            raise ValidationError(_('Invalid Youtube Video ID'))

    def save(self, *args, **kwargs):
            json_string = urllib2.urlopen('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=' + self.youtube_video + '&format=json').read()
            video_data = json.loads(json_string)
            self.title = video_data['title']
            super(YoutubeVideo, self).save(*args, **kwargs)

class Event(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        'Category', related_name='events', on_delete=models.SET_NULL, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True)
    date_start = models.DateField(
        "Starts on", default=date.today, blank=True, null=True)
    time_start = models.TimeField(
        "Starts at", default=timezone.now, blank=True, null=True)
    date_end = models.DateField("Ends on", blank=True, null=True)
    time_end = models.TimeField("Ends at", blank=True, null=True)

    details = models.TextField(blank=True)

    # attendees = models.ManyToManyField('User', related_name='events_attended', blank=True, editable=False)
    # points = models.IntegerField(default=0)

    class Meta:
        ordering = ('-date_start',)
    def __str__(self):
        return self.name + " " + self.date_start.strftime('%m/%d/%Y')


def get_default_date():
    return date.today() + timedelta(weeks=1)


class Poll(models.Model):
    content = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, related_name='polls', on_delete=models.SET_NULL, blank=True, null=True)
    author = models.ForeignKey(
        User, related_name="polls", on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_closed = models.DateTimeField(blank=True, null=True)
    # TODO: send a signal which automatically fills in date_close whenever is_open is set to false? that way the admin just has to press a button "close poll" which sets is_open and date_close automatically
    # date_close = models.DateField("Open Until", default=get_default_date(), blank=True, null=True, help_text="Optional - you can manually close a poll at any time.")
    # have a scheduled script check for closed polls every day

    rank = models.IntegerField(default=0, blank=True)
    is_open = models.BooleanField('Open', default=True)

    #TODO: restrict access to certain polls; allow admin to choose visibility in create form "parents only"/"students only" / "teachers" only etc.
    voters = models.ManyToManyField(User, related_name="polls_submitted", blank=True)

    class Meta:
        ordering = ('is_open', 'rank', 'date_closed', 'date_created', )

    def __str__(self):
        return self.content

    def display_category(self):
        if self.category is not None:
            return self.category.display_color_and_name()
        return 'General'
    display_category.short_description = 'Category'
    display_category.allow_tags = True

    @classmethod
    def get_top_rank(cls):
        return cls.objects.all().first().rank

    def pin(self):
        self.rank = Poll.get_top_rank() + 1
        self.save()

    def unpin(self):
        self.rank = 0
        self.save()

    # call this with daily script
    @classmethod
    def clean_ranks(cls):
        pinned = Announcement.objects.filter(rank__gt=0).reverse()
        i = 1
        for a in pinned:
            a.rank = i
            a.save()
            i += 1


class Choice(models.Model):
    poll = models.ForeignKey(
        Poll, related_name='choices', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)

    def __str__(self):
        return self.content


class Vote(models.Model):
    voter = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return "%s - %s" %(self.choice, self.voter)
