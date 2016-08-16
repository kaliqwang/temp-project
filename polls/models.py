from __future__ import unicode_literals

from numpy import random

import pytz
from django.utils import timezone
from datetime import datetime, date, time, timedelta

from django.db import models

from django.core.urlresolvers import reverse

from categories.models import *
from accounts.models import *

from base.models import GetOrNoneManager, lorem_random

################################################################################

class Poll(models.Model):
    content = models.CharField(max_length=200)
    author = models.ForeignKey(UserProfile, related_name="polls", blank=True, null=True, on_delete=models.SET_NULL)
    date_open = models.DateTimeField(auto_now_add=True)
    date_close = models.DateTimeField(blank=True, null=True)
    is_open = models.BooleanField(default=True)
    category = models.ForeignKey(Category, related_name='polls', blank=True, null=True, on_delete=models.SET_NULL)
    rank = models.IntegerField(default=0, blank=True)
    total_vote_count = models.IntegerField(default=0, blank=True)
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
        return reverse('polls:detail', args=[str(self.pk)])

    def update_vote_count(self):
        total_vote_count = 0
        for c in self.choices.all():
          	total_vote_count += c.vote_count
        self.total_vote_count = total_vote_count
        self.save()

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
        poll_manager = Poll.objects
        choice_manager = Choice.objects
        user_profiles = UserProfile.objects.all()
        user_profile_count = user_profiles.count()
        if user_profile_count < 100:
            StudentProfile.generate_random_objects(100)
        voter_count = 100
        # Contents
        rand_1 = random.randint(100, size=count) # first word
        rand_2 = random.randint(5, 11, size=count) # length
        # Authors
        rand_3 = random.randint(user_profile_count, size=count)
        # Categories
        categories = Category.objects.all()
        categories_count = categories.count()
        rand_4 = random.randint(categories_count, size=count)
        # Choices
        rand_5 = random.randint(2, 6, size=count)
        # status
        rand_6 = random.randint(3, size=count)

        # Generator loop
        generated_count = 0
        for i in range(0, count):
            # Random Content
            content = lorem_random[rand_1[i]] + ' '
            content_length = rand_2[i]
            content_rand = random.randint(200, size=content_length)
            for c in range(0, content_length):
                content += lorem_random[content_rand[c]] + ' '
            content += '?'
            # Random Author
            author = user_profiles[rand_3[i]]
            # Random Category
            category = categories[rand_4[i]]
            # Random Status
            is_open = True
            if rand_6[i] == 2:
                is_open = False
            # Create Object
            p = poll_manager.create(content=content, author=author, category=category, is_open=is_open)
            # Random Choices
            choice_count = rand_5[i]
            for x in range(0, choice_count):
                choice_content = lorem_random[rand_1[i]] + ' '
                choice_length = rand_2[i]
                choice_rand = random.randint(200, size=choice_length)
                for y in range(0, choice_length):
                    choice_content += lorem_random[choice_rand[y]] + ' '
                c = choice_manager.create(poll=p, content=choice_content)
            # Random Votes
            vote_count = 0
            if add_votes:
                vote_count = p.generate_random_votes(user_profiles, choice_count, voter_count)
            generated_count += 1
            print('Generated Poll %d (%d choices, %d votes, open: %s)' % (p.pk, choice_count, vote_count, p.is_open))
        return generated_count

    def generate_random_votes(self, user_profiles, choice_count, voter_count):
        vote_manager = Vote.objects
        rand_votes = random.randint(choice_count, size=voter_count)
        choices = self.choices.all()
        vote_counter = 0
        for i in range(0, voter_count):
            voter = user_profiles[i]
            choice = choices[rand_votes[i]]
            v = vote_manager.create(poll=self, choice=choice, voter=voter)
            print('Generated Vote %d (Userprofile %d, Choice %d)' % (v.pk, voter.pk, choice.pk))
            vote_counter += 1
        return vote_counter

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    vote_count = models.IntegerField(default=0, blank=True)

    objects = GetOrNoneManager()

    class Meta:
        ordering = ('poll',)

    def __str__(self):
        return self.content

    def update_vote_count(self):
        self.vote_count = self.votes.count()
        self.save()

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
        p = self.choice.poll
        self.poll = p
        previous_vote = Vote.objects.get_or_none(voter=self.voter, poll=self.poll)
        if previous_vote:
            original_choice = previous_vote.choice
            original_choice.vote_count -= 1
            original_choice.save()
            previous_vote.delete()
        new_choice = Choice.objects.get_or_none(pk=self.choice.pk)
        if new_choice.vote_count % 100 == 0:
          	new_choice.update_vote_count()
        new_choice.vote_count += 1
        new_choice.save()
        p.update_vote_count()
        super(Vote, self).save(*args, **kwargs)
