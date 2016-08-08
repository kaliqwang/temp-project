from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

from colorful.fields import RGBColorField

from base.models import GetOrNoneManager

################################################################################

class Category(models.Model):
    COLOR_CHOICES = [
        '#f2f3f4', '#f3c300', '#875692', '#f38400', '#a1caf1', '#be0032', '#c2b280',
        '#848482', '#008856', '#e68fac', '#0067a5', '#f99379', '#604e97', '#f6a600',
        '#b3446c', '#dcd300', '#882d17', '#8db600', '#654522', '#e25822', '#2b3d26',
    ]
    name = models.CharField(max_length=30)
    color = RGBColorField(unique=True, colors=COLOR_CHOICES)

    objects = GetOrNoneManager()

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    @classmethod
    def merge(cls, categories, new_name=None, new_color=None):
        count = len(categories)
        if count > 0:
            first = categories[0]
            for i in range(1, count):
                categories[i].announcements.all().update(category=first)
                categories[i].events.all().update(category=first)
                categories[i].polls.all().update(category=first)
                categories[i].delete()
            # Keep first category's name and color by default
            if new_name:
                first.name = new_name
            if new_color:
                first.color = new_color
            first.save()
            return True
