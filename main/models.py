################################################################################

from __future__ import unicode_literals

import os

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from colorful.fields import RGBColorField
from django.utils import timezone
from datetime import datetime, date, time, timedelta
import requests
import urllib2
import json

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from django.core.files import File
from StringIO import StringIO
from PIL import Image
from urlparse import urlparse

################################################################################

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

colors = [
    '#f2f3f4', '#222222', '#f3c300', '#875692', '#f38400', '#a1caf1', '#be0032',
    '#c2b280', '#848482', '#008856', '#e68fac', '#0067a5', '#f99379', '#604e97',
    '#f6a600', '#b3446c', '#dcd300', '#882d17', '#8db600', '#654522', '#e25822',
    '#2b3d26'
]

################################################################################

ten_digit_validator = RegexValidator(
    regex=r'^\d{10}$', message='Please enter a 10 digit value')
youtube_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_-]{11}$', message='Invalid YouTube video id')

################################################################################

class GetOrNoneManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

################################################################################

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', null=True)
    mobile = models.CharField("Phone Number", unique=True, max_length=10,
                              validators=[ten_digit_validator])
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    objects = GetOrNoneManager()

    def __str__(self):
        return self.user.get_full_name()

class StudentProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, related_name='student_profile', null=True)
    student_id = models.CharField("Student ID", unique=True, max_length=10,
                                  validators=[ten_digit_validator])
    grade_level = models.IntegerField("Grade Level", default=FRESHMAN, choices=grade_levels)
    objects = GetOrNoneManager()

    def __str__(self):
        return '%s - student profile' % self.user_profile

class TeacherProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, related_name='teacher_profile', null=True)
    room = models.CharField("Room Number", unique=True, max_length=6)
    objects = GetOrNoneManager()

    def __str__(self):
        return self.user_profile  + ' - teacher profile'

################################################################################

class Category(models.Model):
    name = models.CharField(max_length=50)
    color = RGBColorField(unique=True, colors=colors)

    objects = GetOrNoneManager()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def merge(self, c):
        # get all related objects of c
        announcements = c.announcements.all()
        events = c.events.all()
        polls = c.polls.all()
        # for each related object, set category field to self
        #TODO: use special queryset functions that efficiently update all fields (single column) at once
        for a in announcements:
            a.category = self
            a.save()
        for e in events:
            e.category = self
            e.save()
        for p in polls:
            p.category = self
            p.save()
        # delete c
        c.delete()
        # set color with kwarg
        self.color = kwargs.pop('color', self.color)
        self.save()

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(UserProfile, related_name="announcements", blank=True, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    category = models.ForeignKey(Category, related_name='announcements', blank=True, null=True, on_delete=models.SET_NULL)
    rank = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('-rank', '-date_created')

    def __str__(self):
        return "%s - %s (%s)" % (self.date_created.strftime('%b %d'), self.title, self.category)

    def get_absolute_url(self):
        return reverse('announcement-detail', args=[str(self.pk)])

    @classmethod
    def clean_ranks(cls):
        pinned = Announcement.objects.filter(rank__gt=0).reverse()
        i = 1
        for a in pinned:
            a.rank = i
            a.save()
            i += 1

    @classmethod
    def get_top_rank(cls):
        return cls.objects.all().first().rank

    def pin(self):
        self.rank = Announcement.get_top_rank() + 1
        self.save()

    def unpin(self):
        self.rank = 0
        self.save()

def default_date():
    return date.today()

def default_time():
    return datetime.now().time().strftime('%I:%M %p')

class Event(models.Model):
    name = models.CharField(max_length=50)
    date_start = models.DateField("Starts on")
    time_start = models.TimeField("Starts at", blank=True, null=True)
    date_end = models.DateField("Ends on", blank=True)
    time_end = models.TimeField("Ends at", blank=True, null=True)
    is_multi_day = models.BooleanField(default=False)
    location = models.CharField(blank=True, max_length=50)
    details = models.TextField(blank=True)
    category = models.ForeignKey(Category, related_name='events', blank=True, null=True, on_delete=models.SET_NULL)
    #TODO: record attendees and points

    class Meta:
        ordering = ('-date_start', '-time_start')

    def __str__(self):
        return "%s - %s (%s)" % (self.date_start.strftime('%b %d'), self.name, self.category)

    def clean(self):
        # Set end date if needed
        if self.date_end is None:
            self.date_end = self.date_start
        # Check if end date comes before start date
        elif self.date_end < self.date_start:
            raise ValidationError(_('Invalid end date'))
        # Check if both end time comes before start time if both are on the same day
        elif self.date_end == self.date_start and self.time_start and self.time_end:
            if self.time_end < self.time_start:
                raise ValidationError(_('Invalid end time'))

    def save(self, *args, **kwargs):
        if self.date_start < self.date_end:
            self.is_multi_day = True
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.pk)])

class Poll(models.Model):
    content = models.CharField(max_length=200)
    author = models.ForeignKey(UserProfile, related_name="polls", blank=True, null=True, on_delete=models.SET_NULL)
    date_open = models.DateTimeField(auto_now_add=True)
    date_close = models.DateTimeField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='polls', blank=True, null=True, on_delete=models.SET_NULL)
    rank = models.IntegerField(default=0, blank=True)
    # voters = models.ManyToManyField(UserProfile, related_name="polls_submitted", blank=True)
    #TODO: allow visibility to be set for each poll (students, parents, teachers, etc.)

    objects = GetOrNoneManager()

    class Meta:
        ordering = ('is_open', 'rank', '-date_close', '-date_open')

    def __str__(self):
        return "%s (%s)" % (self.content, self.category)

    def save(self, *args, **kwargs):
        if not self.is_open and not self.date_close:
            self.date_close = timezone.now()
        else:
            self.date_close = None
        super(Poll, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('poll-detail', args=[str(self.pk)])

    def vote_count(self):
        count = {c.pk : c.vote_count() for c in self.choices}
        for v in count.values():
            total += v
        count['total'] = total
        return count

    def get_vote(self, user_profile_pk):
        for c in self.choices:
            vote = UserProfile.objects.get(pk=user_profile_pk).votes.get_or_none(choice_id=c.pk)
            if vote:
                return vote
        return None

    def pin(self):
        self.rank = Poll.get_top_rank() + 1
        self.save()

    def unpin(self):
        self.rank = 0
        self.save()

    @classmethod
    def get_top_rank(cls):
        return cls.objects.all().first().rank

    @classmethod
    def clean_ranks(cls):
        pinned = Announcement.objects.filter(rank__gt=0).reverse()
        i = 1
        for a in pinned:
            a.rank = i
            a.save()
            i += 1

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)

    class Meta:
        ordering = ('poll',)

    def __str__(self):
        return self.content

    def vote_count(self):
        return self.votes.count

class Vote(models.Model):
    voter = models.ForeignKey(UserProfile, related_name='votes', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)

    objects = GetOrNoneManager()

    class Meta:
        ordering = ('poll', 'choice')
        unique_together = ('voter', 'poll')

    def __str__(self):
        return "%s - %s" %(self.choice, self.voter)

    def save(self, *args, **kwargs):
        self.poll = self.choice.poll
        previous_vote = Vote.objects.get_or_none(voter=self.voter, poll=self.poll)
        if previous_vote:
            previous_vote.delete()
        super(Vote, self).save(*args, **kwargs)

################################################################################

class ImageFile(models.Model):
    announcement = models.ForeignKey(Announcement, related_name='image_files', on_delete=models.CASCADE)
    #TODO: change w, h, and quality settings to settings.py variables
    image_file = ProcessedImageField(upload_to='main/images/', blank=True, null=True, processors=[ResizeToFit(1280, 720)], format='JPEG', options={'quality': 80})
    image_file_thumbnail = ImageSpecField(source='image_file', processors=[ResizeToFill(110, 110)], format='JPEG', options={'quality': 50})

    def __str__(self):
        return os.path.basename(self.image_file.path)

class ImageLink(models.Model):
    announcement = models.ForeignKey(Announcement, related_name='image_links', on_delete=models.CASCADE)
    image_link = models.URLField()
    #TODO: change w, h, and quality settings to settings.py variables
    image_file = ProcessedImageField(upload_to='main/images/', blank=True, null=True, processors=[ResizeToFit(1280, 720)], format='JPEG', options={'quality': 80})
    image_file_thumbnail = ImageSpecField(source='image_file', processors=[ResizeToFill(110, 110)], format='JPEG', options={'quality': 50})

    def __str__(self):
        return os.path.basename(self.image_file.path)

    def save(self, *args, **kwargs):
        #TODO: MESSY SOLUTION: clean up all of the code in this method: find a cleaner solution
        original = ImageLink.objects.get(pk=self.pk)
        if not self.image_file or self.image_link != original.image_link:
            # Image Object
            img = self.download_image()
            if img is not None:
                # w, h = img.size
                # format = img.format
                # file_size = f.size
                # Image filename
                name = os.path.basename(self.image_link)
                # Write image contents to temporary file-like object
                f = StringIO()
                img.save(f)
                # Save image to model's ImageField
                self.image_file.save(name, File(f), save=False)
                super(ImageLink, self).save(*args, **kwargs)

    def download_image(self):
        r = requests.get(self.image_link)
        if r.status_code == 200:
            img = Image.open(StringIO(r.content))
            return img
        return None

    def image_exists(self):
        try:
            r = requests.head(self.image_link)
        except:
            return False
        return r.status_code == 200

class YouTubeVideo(models.Model):
    announcement = models.ForeignKey(Announcement, related_name='youtube_videos', on_delete=models.CASCADE)
    title = models.CharField('Video Title', max_length=200, blank=True)
    youtube_video = models.CharField('YouTube Video ID', max_length=11, validators=[youtube_validator])

    def __str__(self):
        return self.title

    def clean(self):
        req = urllib2.Request('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=' + self.youtube_video + '&format=json')
        try:
            resp = urllib2.urlopen(req)
        except urllib2.HTTPError:
            raise ValidationError(_('Invalid YouTube video ID'))

    def save(self, *args, **kwargs):
        json_string = urllib2.urlopen('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=' + self.youtube_video + '&format=json').read()
        data = json.loads(json_string)
        self.title = data['title']
        super(YouTubeVideo, self).save(*args, **kwargs)

################################################################################

# CURRENTLY UNUSED
#
# periods = (
#     ('1', 'Period 1'),
#     ('2', 'Period 2'),
#     ('3', 'Period 3'),
#     ('4', 'Period 4'),
#     ('5a','Period 5A'),
#     ('5b','Period 5B'),
#     ('6', 'Period 6'),
#     ('7', 'Period 7'),
# )
#
# class Subject(models.Model):
#     subject = models.CharField(max_length=50)
#
#     def __str__(self):
#         return self.subject
#
# class Class(models.Model):
#     subject = models.ForeignKey('Subject', related_name='classes', blank=True, null=True, on_delete=models.SET_NULL)
#     teacher = models.ForeignKey('TeacherProfile', related_name='classes', blank=True, null=True)
#     room = models.CharField('Room Number', max_length=6)
#     period = models.CharField(max_length=2, choices=periods)
#     is_honors = models.BooleanField(default=False)
#     is_ap = models.BooleanField(default=False)
#     is_dual = models.BooleanField(default=False)
#
#     def __str__(self):
#         return '%s - %s' % (self.subject, self.teacher)
#
#     class Meta:
#         unique_together = ('teacher', 'period')
#
# class Schedule(models.Model):
#     #TODO: validate overlapping classes by period
#     classes = models.ManyToManyField(Class, related_name='schedules_included')
#
#     def __str__(self):
#         return '%s\'s Schedule' % self.user
