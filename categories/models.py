from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse

from colorful.fields import RGBColorField

from base.models import GetOrNoneManager

################################################################################

colors = [
    '#f2f3f4', '#f3c300', '#875692', '#f38400', '#a1caf1', '#be0032', '#c2b280',
    '#848482', '#008856', '#e68fac', '#0067a5', '#f99379', '#604e97', '#f6a600',
    '#b3446c', '#dcd300', '#882d17', '#8db600', '#654522', '#e25822', '#2b3d26',
]

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
