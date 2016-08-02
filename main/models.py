# -*- coding: utf-8 -*-

################################################################################

from __future__ import unicode_literals

import os

import math

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from colorful.fields import RGBColorField
from django.utils import timezone
from datetime import datetime, date, time, timedelta
import pytz
import requests
import urllib2
import json

from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit

from django.core.files.images import ImageFile
from django.core.files.base import ContentFile
from django.core.files import File

from PIL import Image
from io import BytesIO
from urlparse import urlparse

from random import randint, random

from django.conf import settings

################################################################################

colors = [
    '#f2f3f4', '#f3c300', '#875692', '#f38400', '#a1caf1', '#be0032', '#c2b280',
    '#848482', '#008856', '#e68fac', '#0067a5', '#f99379', '#604e97', '#f6a600',
    '#b3446c', '#dcd300', '#882d17', '#8db600', '#654522', '#e25822', '#2b3d26',
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

mobile_validator = RegexValidator(
    regex=r'^\d{10}$', message='Enter a valid phone number')
student_id_validator = RegexValidator(
    regex=r'^\d{10}$', message='Enter a valid student id')
youtube_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_-]{11}$', message='Invalid YouTube video id')

class GetOrNoneManager(models.Manager):

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

################################################################################

lorem_random = [
    # First 100 words are capitalized
    'Lorem','Ipsum','Dolor','Sit','Amet','Consectetur','Adipiscing','Elit','Donec','Vel',
    'Facilisis','Mi','Imperdiet','Hendrerit','Est','Nam','Venenatis','Magna','Semper','Libero',
    'Pretium','A','Lacinia','Nisl','Varius','Ut','Velit','Vitae','Viverra','Nibh',
    'Sed','Eleifend','Volutpat','Placerat','Duis','Eu','Tortor','Nec','Mauris','Aliquam',
    'Ac','Urna','In','Metus','Augue','Ultrices','At','Felis','Gravida','Fermentum',
    'Etiam','Fringilla','Purus','Congue','Eget','Turpis','Condimentum','Id','Luctus','Lacus',
    'Commodo','Porta','Lectus','Vehicula','Nulla','Odio','Erat','Maximus','Et','Sodales',
    'Tellus','Sapien','Duis','Integer','Dictum','Rhoncus','Nunc','Neque','Dui','Suscipit',
    'Aliquet','Rutrum','Vestibulum','Tristique','Sem','Enim','Accumsan','Eros','Non','Curabitur',
    'Laoreet','Quis','Sagittis','Nisi','Efficitur','Auctor','Fusce','Blandit','Pharetra','Leo',
     # Second 100 words are lowercase
    'lorem','ipsum','dolor','sit','amet','consectetur','adipiscing','elit','integer','felis',
    'in','egestas','vitae','malesuada','nisi','proin','pellentesque','est','nec','luctus',
    'vestibulum','et','metus','at','dui','efficitur','iaculis','a','eleifend','massa',
    'morbi','elementum','eget','leo','ornare','vel','nunc','placerat','odio','ut',
    'tincidunt','pulvinar','curabitur','mauris','viverra','eu','id','laoreet','mattis','donec',
    'erat','facilisis','porttitor','nibh','fringilla','turpis','arcu','sem','molestie','quis',
    'libero','sed','euismod','fermentum','ultrices','porta','accumsan','neque','nam','quam',
    'posuere','quisque','dapibus','nisl','ac','nulla','facilisi','nullam','ligula','bibendum',
    'diam','dapibus','augue','varius','maecenas','risus','semper','dignissim','aliquam','sodales',
    'pretium','ante','ullamcorper','suscipit','condimentum','tortor','cursus','praesent','non','eros',
]

random_videos = [
    "mT0DpuAlJbs", "_yhf_PvRGIE", "LKiDgFySXg8", "zMN9otsaZ80", "cb1Jp-rFJDI",
    "gGrXEewfz34", "6QdOI4zZC0g", "LWgqWuJG5Jg", "Z1lpZRe7-R8", "Kkr9hf9d8Fo",
    "s1exvkLxQi8", "T7iiwsT5hWg", "eZ5C7dfU6-A", "pmhqMajav8Y", "8SF1Wt__W6g",
    "oQq9vDU4IfU", "wLXVDzM8Tnk", "V3i0eOfchxg", "BG9rW-hYikw", "4SxWtQzL6js",
]

first_names = [
    # 70 male first names
    'Adam','Adrian','Alan','Alexander','Andrew','Anthony','Austin','Benjamin','Blake','Boris',
    'Brandon','Brian','Cameron','Charles','Christian','Christopher','Colin','Connor','Dan','David',
    'Dominic','Dylan','Edward','Eric','Evan','Frank','Gavin','Gordon','Harry','Ian',
    'Isaac','Jack','Jacob','Jake','James','Jason','Joe','John','Jonathan','Joseph',
    'Julian','Justin','Keith','Kevin','Leonard','Liam','Lucas','Luke','Matt','Max',
    'Michael','Nathan','Nicholas','Oliver','Paul','Peter','Phil','Richard','Robert','Ryan',
    'Sam','Sean','Sebastian','Stephen','Steven','Stewart','Thomas','Tim','Trevor','William',
    # 70 female first names
    'Abigail','Alexandra','Alison','Amanda','Amelia','Amy','Andrea','Angela','Anna','Anne',
    'Audrey','Ava','Bella','Caroline','Carolyn','Chloe','Claire','Diana','Dorothy','Elizabeth',
    'Ella','Emily','Emma','Faith','Felicity','Gabrielle','Grace','Hannah','Heather','Irene',
    'Jane','Jasmine','Jennifer','Jessica','Joan','Julia','Karen','Katherine','Kimberly','Kylie',
    'Lauren','Leah','Lillian','Lily','Lisa','Madeleine','Maria','Mary','Megan','Melanie',
    'Michelle','Molly','Natalie','Nicola','Olivia','Penelope','Rachel','Rebecca','Rose','Samantha',
    'Sarah','Sonia','Sophie','Stephanie','Theresa','Vanessa','Victoria','Virginia','Wendy','Zoe',
]

last_names = [
    # 140 last names
    'Abraham','Allan','Anderson','Arnold','Avery','Bailey','Baker','Ball','Bell', 'Berry',
    'Black','Blake','Bower','Brown','Buckland','Burgess','Butler','Cameron','Campbell','Chapman',
    'Churchill','Clark','Clarkson','Coleman','Davidson','Davies','Dickens','Dowd','Duncan','Dyer',
    'Edmunds','Ellison','Ferguson','Fisher','Forsyth','Fraser','Gibson','Gill','Glover','Graham',
    'Grant','Gray','Greene','Hamilton','Harris','Hart','Hemmings','Henderson','Hill','Howard',
    'Hudson','Hughes','Hunter','Jackson','James','Johnston','Jones','Kelly','Kerr','King',
    'Knox','Lambert','Lawrence','Lee','Lewis','Lyman','MacDonald','Mackay','Mackenzie','Manning',
    'Marshall','Martin','Mathis','May','McDonald','McLean','McGrath','Metcalfe','Miller','Mills',
    'Mitchell','Morgan','Morrison','Murray','Nash','Newman','Nolan','North','Ogden','Oliver',
    'Paige','Parr','Parsons','Paterson','Payne','Peake','Peters','Piper','Poole','Powell',
    'Pullman','Quinn','Rampling','Randall','Rees','Reid','Roberts','Robertson','Ross','Russell',
    'Rutherford','Sanderson','Scott','Sharp','Short','Simpson','Skinner','Slater','Smith','Springer',
    'Stewart','Sutherland','Taylor','Terry','Thomson','Tucker','Turner','Underwood','Vance','Vaughan',
    'Walker','Wallace','Walsh', 'Watson','Welch','White','Wilkins','Wilson','Wright','Young',
]

def get_random_name():
    first = first_names[randint(0, 139)]
    last = last_names[randint(0, 139)]
    return (first, last)

def get_random_datetime(interval):
    steps = int(400000 / interval)
    random_minutes = timedelta(minutes=(randint(0, steps) * interval))
    start_date_naive = datetime(2016, 8, 8)
    local = pytz.timezone ("EST5EDT")
    start_date_local = local.localize(start_date_naive)
    return start_date_local + random_minutes

def get_random_minutes(interval):
    steps = int(10000 / interval)
    return timedelta(minutes=(randint(6, steps) * interval))

################################################################################

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', null=True)
    # TODO: set mobile to unique = True in production
    mobile = models.CharField("Phone Number", max_length=10, validators=[mobile_validator])
    # TODO: create a signal (or just update save function of related model) that automatically sets these values when a related student/teacher profile object is saved
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    categories_hidden_announcements = models.ManyToManyField('Category', blank=True)
    # related_name="user_profiles_categories_hidden_announcements",
    # categories_hidden_events = models.ManyToManyField('Category', related_name="user_profiles_categories_hidden_events", blank=True)

    objects = GetOrNoneManager()

    def __str__(self):
        return self.user.get_full_name()

class StudentProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, related_name='student_profile', null=True)
    # TODO: set student_id to unique = True in production
    student_id = models.CharField("Student ID", max_length=10, validators=[student_id_validator])
    grade_level = models.IntegerField("Grade Level", default=FRESHMAN, choices=grade_levels)
    objects = GetOrNoneManager()

    def __str__(self):
        return '%s - student profile' % self.user_profile

    @classmethod
    def generate_random_objects(cls, count):
        user_pk = User.objects.latest('pk').pk + 1
        generated_count = 0
        for i in range(0, count):
            first_name, last_name = get_random_name()
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
            student_id = randint(1100000000, 1100999999)
            grade_level = randint(0, 3)
            student_profile= StudentProfile.objects.create(
                user_profile=user_profile,
                grade_level=grade_level,
            )
            user_pk += 1
            generated_count += 1
            print('StudentProfile %d created (user=%d, user_profile=%d)' %(student_profile.pk, user.pk, user_profile.pk))
        return generated_count

class TeacherProfile(models.Model):
    user_profile = models.OneToOneField(UserProfile, related_name='teacher_profile', null=True)
    room = models.CharField("Room Number", unique=True, max_length=6)
    objects = GetOrNoneManager()

    def __str__(self):
        return '%s - teacher profile' % self.user_profile

################################################################################

class Category(models.Model):
    name = models.CharField(max_length=30)
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

################################################################################

class Announcement(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(UserProfile, related_name="announcements", blank=True, null=True, on_delete=models.SET_NULL)
    # TODO: set auto_now_add=True for production
    date_created = models.DateTimeField()
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

    @classmethod
    def generate_random_objects(cls, count):
        user_profiles = UserProfile.objects.all()
        user_profiles_count = user_profiles.count()
        categories = Category.objects.all()
        categories_count = categories.count()

        generated_count = 0
        for i in range(0, count):
            # Random title
            title = lorem_random[randint(0, 99)] + ' '
            length = int(pow(random(), 3) * 6 + 1)
            for x in range(0, length):
                title += lorem_random[randint(0, 199)] + ' '
            # Random author
            author = user_profiles[int(random() * user_profiles_count)]
            # Random date_created
            date_created = get_random_datetime(1)
            # Random content
            content = lorem_random[randint(0, 99)] + ' '
            length = int(pow(random(), 3) * 60 + 10)
            for y in range(0, length):
                content += lorem_random[randint(0, 199)] + ' '
            # Random category
            category = categories[int(random() * categories_count)]
            # Create Object
            a = Announcement(
                title=title,
                author=author,
                date_created=date_created,
                content=content,
                category=category,
            )
            a.save()
            # Random Images
            image_count = int(pow(random(), 5) * 12)
            for y in range(0, image_count):
                ImageLink.objects.create(
                    announcement=a,
                    image_link="https://unsplash.it/200/300/?random"
                )
            # Random Videos
            video_count = int(pow(random(), 5) * 4)
            for z in range(0, video_count):
                YouTubeVideo.objects.create(
                    announcement=a,
                    youtube_video=random_videos[randint(0, 19)]
                )
            generated_count += 1
            print('Announcement %d created: %d images %d videos' % (a.pk, image_count, video_count))
        return generated_count

def default_date():
    return date.today()

def default_time():
    return datetime.now().time().strftime('%I:%M %p')

class Event(models.Model):
    name = models.CharField(max_length=100)
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
            print('End date set')
        # Check if end date comes before start date
        elif self.date_end < self.date_start:
            raise ValidationError(_('Invalid end date'))
            print('End date came before start date')
        # Check if both end time comes before start time if both are on the same day
        elif self.date_end == self.date_start and self.time_start and self.time_end:
            if self.time_end < self.time_start:
                raise ValidationError(_('Invalid end time'))
                print('End time came before start time')

    def save(self, *args, **kwargs):
        if self.date_start < self.date_end:
            self.is_multi_day = True
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event-detail', args=[str(self.pk)])

    @classmethod
    def generate_random_objects(cls, count):
        categories = Category.objects.all()
        categories_count = categories.count()

        generated_count = 0
        for i in range(0, count):
            # Random title
            name = lorem_random[randint(0, 99)] + ' '
            length = int(pow(random(), 3) * 6 + 1)
            for x in range(0, length):
                name += lorem_random[randint(0, 99)] + ' '
            # Random date_start / time_start
            datetime_start = get_random_datetime(5)
            date_start = datetime_start.date()
            time_start = datetime_start.time()
            # Random date_end / time_end
            datetime_end = datetime_start + get_random_minutes(5)
            date_end = datetime_end.date()
            time_end = datetime_end.time()
            # Random Location
            location = ''
            length = int(pow(random(), 2) * 4 + 2)
            for y in range (0, length):
                location += lorem_random[randint(0, 99)] + ' '
            # Random Details
            details = lorem_random[randint(0, 99)]
            length = int(pow(random(), 3) * 100)
            for z in range(0, length):
                details += lorem_random[randint(0, 199)] + ' '
            # Random category
            category = categories[int(random() * categories_count)]
            # Create Object
            e = Event(
                name=name,
                date_start=date_start,
                time_start=time_start,
                date_end=date_end,
                time_end=time_end,
                location=location,
                details=details,
                category=category,
            )
            e.save()
            generated_count += 1
            print('Event %d created' % e.pk)
        return generated_count

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
        count = {c.pk : c.vote_count() for c in self.choices.all()}
        for v in count.values():
            total += v
        count['total'] = total
        return count

    def get_vote(self, user_profile_pk):
        for c in self.choices.all():
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

    @classmethod
    def generate_random_objects(cls, count, add_votes):
        user_profiles = UserProfile.objects.all()
        user_profiles_count = user_profiles.count()
        categories = Category.objects.all()
        categories_count = categories.count()

        generated_count = 0
        for i in range(0, count):
            # Random content
            content = lorem_random[randint(0, 99)] + ' '
            length = int(pow(random(), 2) * 6 + 6)
            for x in range(0, length):
                content += lorem_random[randint(0, 199)] + ' '
            content += '?'
            # Random author
            author = user_profiles[int(random() * user_profiles_count)]
            # Random category
            category = categories[int(random() * categories_count)]
            # Create Object
            p = Poll(content=content, author=author, category=category)
            p.save()
            # Random Choices
            choice_count = randint(2, 6)
            choice_length = int(pow(random(), 2) * 10)
            for y in range(0, choice_count):
                choice_content = lorem_random[randint(0, 99)] + ' '
                for z in range(0, choice_length):
                    choice_content += lorem_random[randint(0, 199)] + ' '
                    c = Choice(poll=p, content=choice_content)
                    c.save()
            # Random status
            status = randint(0, 2)
            vote_count = 0
            if status == 2:
                p.is_open = False
                p.save()
            if add_votes:
                vote_count = p.generate_random_votes(user_profiles, user_profiles_count)
            generated_count += 1
            print('Poll %d created: %d choices, %d votes, open: %s' % (p.pk, choice_count, vote_count, p.is_open))
        return generated_count

    def generate_random_votes(self, user_profiles, user_profiles_count):
        choices = self.choices.all()
        choices_count = self.choices.count()
        vote_counter = 0
        for user_profile in user_profiles:
            choice = choices[randint(0, choices_count - 1)]
            v = Vote(poll=self, choice=choice, voter=user_profile)
            v.save()
            print('Userprofile %d voted for choice %d' % (user_profile.pk, choice.pk))
            vote_counter += 1
        return vote_counter

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)

    class Meta:
        ordering = ('poll',)

    def __str__(self):
        return self.content

    def vote_count(self):
        return self.votes.count()

class Vote(models.Model):
    voter = models.ForeignKey(UserProfile, related_name='votes', on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, related_name='votes', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)

    objects = GetOrNoneManager()

    class Meta:
        ordering = ('poll', 'choice')

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
    # NOTE: set on_delete=models.CASCADE and remove null=True for production
    announcement = models.ForeignKey(Announcement, related_name='image_files', null=True, on_delete=models.SET_NULL)
    image_file = ProcessedImageField(
        upload_to='main/images/', blank=True, null=True,
        processors=[ResizeToFit(settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT)],
        format='JPEG', options={'quality': settings.IMAGE_QUALITY},
    )
    image_file_thumbnail = ImageSpecField(
        source='image_file',
        processors=[ResizeToFill(settings.THUMBNAIL_WIDTH, settings.THUMBNAIL_HEIGHT)],
        format='JPEG', options={'quality': settings.THUMBNAIL_QUALITY},
    )

    def __str__(self):
        return os.path.basename(self.image_file.path)

class ImageLink(models.Model):
    # NOTE: set on_delete=models.CASCADE and remove null=True for production
    announcement = models.ForeignKey(Announcement, related_name='image_links', blank=True, null=True, on_delete=models.SET_NULL)
    image_link = models.URLField()
    image_file = ProcessedImageField(
        upload_to='main/images/', blank=True, null=True,
        processors=[ResizeToFit(settings.IMAGE_WIDTH, settings.IMAGE_HEIGHT)],
        format='JPEG', options={'quality': settings.IMAGE_QUALITY},
    )
    image_file_thumbnail = ImageSpecField(
        source='image_file',
        processors=[ResizeToFill(settings.THUMBNAIL_WIDTH, settings.THUMBNAIL_HEIGHT)],
        format='JPEG', options={'quality': settings.THUMBNAIL_QUALITY},
    )


    objects = GetOrNoneManager()

    def __str__(self):
        return os.path.basename(self.image_file.path)

    def save(self, *args, **kwargs):
        content = self.download_image()
        if self.pk is None:
            if content:
                name = os.path.basename(self.image_link)
                self.image_file.save(name, content, save=False)
                super(ImageLink, self).save(*args, **kwargs)
        else:
            original = ImageLink.objects.get_or_none(pk=self.pk)
            if not self.image_file or self.image_link != original.image_link:
                if content:
                    name = os.path.basename(self.image_link)
                    original.image_file.delete(save=False)
                    self.image_file.save(name, content, save=False)
                    super(ImageLink, self).save(*args, **kwargs)

    def download_image(self):
        r = requests.get(self.image_link)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            if img:
                img_io = BytesIO()
                img.save(img_io, 'JPEG')
                return ContentFile(img_io.getvalue())
        return None

    def image_exists(self):
        try:
            r = requests.head(self.image_link)
        except:
            return False
        return r.status_code == 200

    @classmethod
    def create_image_set(cls):
        for i in range(0, len(random_images)):
            i = ImageLink(image_link=random_images[i])
            i.save()

class YouTubeVideo(models.Model):
    # TODO: set on_delete=models.CASCADE and remove null=True for production
    announcement = models.ForeignKey(Announcement, related_name='youtube_videos', null=True, on_delete=models.SET_NULL)
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
