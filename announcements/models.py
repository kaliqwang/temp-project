from __future__ import unicode_literals

import os
import json
import requests
from numpy import random

import pytz
from django.utils import timezone
from datetime import datetime, date, time, timedelta

from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from PIL import Image
from io import BytesIO
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit
from django.core.files.base import ContentFile
# from django.core.files import File
# from django.core.files.images import ImageFile

from django.conf import settings

from categories.models import *
from accounts.models import *

from base.models import GetOrNoneManager, youtube_validator, lorem_random, random_videos

################################################################################

class Announcement(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey(UserProfile, related_name="announcements", blank=True, null=True, on_delete=models.SET_NULL)
    # TODO: set auto_now_add=True for production
    date_created = models.DateTimeField(default=timezone.now)
    content = models.TextField()
    category = models.ForeignKey(Category, related_name='announcements', blank=True, null=True, on_delete=models.SET_NULL)
    rank = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('-rank', '-date_created')

    def __str__(self):
        return "%s - %s (%s)" % (self.date_created.strftime('%b %d'), self.title, self.category)

    def get_absolute_url(self):
        return reverse('announcements:detail', args=[str(self.pk)])

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
        announcement_manager = Announcement.objects
        image_manager = ImageLink.objects
        video_manager = YouTubeVideo.objects
        #
        user_profiles = UserProfile.objects.all()
        user_profiles_count = user_profiles.count()
        # Titles
        rand_1 = random.randint(100, size=count) # first word
        rand_2 = random.randint(1, 7, size=count) # length
        # Authors
        rand_3 = random.randint(user_profiles_count, size=count)
        # Datetimes
        datetime_base = pytz.timezone("EST5EDT").localize(datetime(2016, 8, 8))
        rand_4 = random.randint(400000, size=count) # start
        # Contents
        rand_5 = random.randint(100, size=count) # first word
        rand_6 = random.randint(5, 40, size=count) # length
        # Categories
        categories = Category.objects.all()
        categories_count = categories.count()
        rand_7 = random.randint(categories_count, size=count)
        # Images
        rand_8 = random.rand(count)
        # Videos
        rand_9 = random.rand(count)
        # Generator loop
        generated_count = 0
        for i in range(0, count):
            # Random title
            title = lorem_random[rand_1.item(i)] + ' '
            title_length = rand_2.item(i)
            title_content = random.randint(200, size=title_length)
            for t in range(0, title_length):
                title += lorem_random[title_content[t]] + ' '
            # Random author
            author = user_profiles[rand_3.item(i)]
            # Random date_created
            days = (rand_4.item(i) * 5) / (60 * 24)
            minutes = (rand_4.item(i) * 5) % (60 * 24)
            date_created = datetime_base + timedelta(days=days, minutes=minutes)
            # Random content
            content = lorem_random[rand_5.item(i)] + ' '
            content_length = rand_6.item(i)
            content_rand = random.randint(200, size=content_length)
            for c in range(0, content_length):
                content += lorem_random[content_rand[c]] + ' '
            # Random category
            category = categories[rand_7.item(i)]
            # Create Object
            a = announcement_manager.create(
                title=title,
                author=author,
                date_created=date_created,
                content=content,
                category=category,
            )
            # Random Images
            image_count = int(pow(rand_8.item(i), 5) * 8)
            for x in range(0, image_count):
                image_manager.create(
                    announcement=a,
                    image_link="https://unsplash.it/200/300/?random"
                )
            # Random Videos
            video_count = int(pow(rand_9.item(i), 5) * 3)
            video_content = random.randint(20, size=video_count)
            for y in range(0, video_count):
                video_manager.create(
                    announcement=a,
                    youtube_video=random_videos[video_content[y]]
                )
            generated_count += 1
            print('Generated Announcement %d (%d images, %d videos)' % (a.pk, image_count, video_count))
        return generated_count

################################################################################

class ImageFile(models.Model):
    # NOTE: set on_delete=models.CASCADE and remove null=True for production
    announcement = models.ForeignKey(Announcement, related_name='image_files', null=True, on_delete=models.SET_NULL)
    image_file = ProcessedImageField(
        upload_to='announcements/images/', blank=True, null=True,
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
        upload_to='announcements/images/', blank=True, null=True,
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
        if content:
            name = os.path.basename(self.image_link)
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
            i = ImageLink(image_link=random_images.item(i))
            i.save()

@receiver(post_delete, sender=ImageFile)
def image_file_delete_on_delete(sender, instance, **kwargs):
    if instance.image_file:
        if os.path.isfile(instance.image_file.path):
            os.remove(instance.image_file.path)

@receiver(pre_save, sender=ImageFile)
def image_file_delete_on_save(sender, instance, **kwargs):
    if instance.pk:
        old = ImageFile.objects.get(pk=instance.pk).image_file
        new = instance.image_file
        if new != old:
            if os.path.isfile(old.path):
                os.remove(old.path)

@receiver(post_delete, sender=ImageLink)
def image_link_delete_on_delete(sender, instance, **kwargs):
    if instance.image_file:
        if os.path.isfile(instance.image_file.path):
            os.remove(instance.image_file.path)

@receiver(pre_save, sender=ImageLink)
def image_link_delete_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = ImageLink.objects.get(pk=instance.pk).image_file
    except ImageLink.DoesNotExist:
        return False

    new_file = instance.image_file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class YouTubeVideo(models.Model):
    # TODO: set on_delete=models.CASCADE and remove null=True for production
    announcement = models.ForeignKey(Announcement, related_name='youtube_videos', null=True, on_delete=models.SET_NULL)
    title = models.CharField('Video Title', max_length=200, blank=True)
    youtube_video = models.CharField('YouTube Video ID', max_length=11, validators=[youtube_validator])

    def __str__(self):
        return self.title

    def clean(self):
        r = requests.get('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=' + self.youtube_video + '&format=json')
        if r.status_code != 200:
            raise ValidationError(_('Invalid YouTube video ID'))

    def save(self, *args, **kwargs):
        json_data = requests.get('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=' + self.youtube_video + '&format=json').text
        data = json.loads(json_data)
        self.title = data['title']
        super(YouTubeVideo, self).save(*args, **kwargs)
