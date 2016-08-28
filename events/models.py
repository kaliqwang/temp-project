from __future__ import unicode_literals

from numpy import random

import pytz
from django.utils import timezone
from datetime import datetime, date, time, timedelta

from django.db import models

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from categories.models import *
from accounts.models import *

from base.models import GetOrNoneManager, youtube_validator, lorem_random

################################################################################

def default_date():
    return date.today()

def default_time():
    return datetime.now().time().strftime('%I:%M %p')

class Event(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(UserProfile, related_name="events", blank=True, null=True, on_delete=models.SET_NULL)
    # TODO: set auto_now_add=True for production
    date_created = models.DateTimeField(default=timezone.now)
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
        return reverse('events:detail', args=[str(self.pk)])

    @classmethod
    def generate_random_objects(cls, count):
        event_manager = Event.objects
        user_profiles = UserProfile.objects.all()
        user_profiles_count = user_profiles.count()
        # Names
        rand_1 = random.randint(100, size=count) # first word
        rand_2 = random.randint(1, 7, size=count) # length
        # Authors
        rand_3 = random.randint(user_profiles_count, size=count)
        # Datetimes
        datetime_base = pytz.timezone("EST5EDT").localize(datetime(2016, 8, 8))
        rand_4 = random.randint(400000, size=count) # start
        rand_5 = random.randint(80000, size=count) # start
        rand_6 = random.randint(6, 2000, size=count) # end - start
        # Locations
        rand_7 = random.randint(100, size=count) # first word
        rand_8 = random.randint(1, 7, size=count) # length
        # Details
        rand_9 = random.randint(100, size=count) # first word
        rand_10 = random.randint(60, size=count) # length
        # Categories
        categories = Category.objects.all()
        categories_count = categories.count()
        rand_11 = random.randint(categories_count, size=count)
        # Generator loop
        generated_count = 0
        for i in range(0, count):
            # Random name
            name = lorem_random[rand_1.item(i)] + ' '
            name_length = rand_2.item(i)
            name_rand = random.randint(200, size=name_length)
            for n in range(0, name_length):
                name += lorem_random[name_rand[n]] + ' '
            # Random author
            author = user_profiles[rand_3.item(i)]
            # Random date_created
            days = (rand_4.item(i) * 5) / (60 * 24)
            minutes = (rand_4.item(i) * 5) % (60 * 24)
            date_created = datetime_base + timedelta(days=days, minutes=minutes)
            # Random datetime start/end
            days = (rand_5.item(i) * 5) / (60 * 24)
            minutes = (rand_5.item(i) * 5) % (60 * 24)
            datetime_start = datetime_base + timedelta(days=days, minutes=minutes)
            date_start = datetime_start.date()
            time_start = datetime_start.time()
            days = (rand_6.item(i) * 5) / (60 * 24)
            minutes = (rand_6.item(i) * 5) % (60 * 24)
            datetime_end = datetime_start + timedelta(days=days, minutes=minutes)
            date_end = datetime_end.date()
            time_end = datetime_end.time()
            # Random Location
            location = lorem_random[rand_7.item(i)] + ' '
            location_length = rand_8.item(i)
            location_rand = random.randint(200, size=location_length)
            for l in range (0, location_length):
                location += lorem_random[location_rand[l]] + ' '
            # Random Details
            details = lorem_random[rand_9.item(i)] + ' '
            details_length = rand_10.item(i)
            details_rand = random.randint(200, size=details_length)
            for d in range(0, details_length):
                details += lorem_random[details_rand[d]] + ' '
            # Random category
            category = categories[rand_11.item(i)]
            # Create Object
            e = event_manager.create(
                name=name,
                author=author,
                date_created=date_created,
                date_start=date_start,
                time_start=time_start,
                date_end=date_end,
                time_end=time_end,
                location=location,
                details=details,
                category=category,
            )
            generated_count += 1
            print('Generated Event %d' % e.pk)
        return generated_count
