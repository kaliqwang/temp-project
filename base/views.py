from __future__ import unicode_literals

from categories.models import *
from accounts.models import *
from announcements.models import *
from events.models import *
from polls.models import *

from django.shortcuts import render

from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    return render(request, 'base/index.html')

@staff_member_required
def generator(request):
    categories_count = Category.objects.count()
    announcements_count = Announcement.objects.count()
    events_count = Event.objects.count()
    Poll.objects.prefetch_related('votes').all()
    polls_without_votes_count = Poll.objects.filter(votes=None).count()
    polls_with_votes_count = Poll.objects.count() - polls_without_votes_count
    student_profiles_count = StudentProfile.objects.count()
    return render(request, 'base/generator.html', {
        'categories_count': categories_count,
        'announcements_count': announcements_count,
        'events_count': events_count,
        'polls_without_votes_count': polls_without_votes_count,
        'polls_with_votes_count': polls_with_votes_count,
        'student_profiles_count': student_profiles_count
    })
