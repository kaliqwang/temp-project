from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

import urllib2
import json

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

from django.utils import timezone

from models import *
from forms import *


def index(request):
    return render(request, 'main/index.html')

################################################################################
################################ ANNOUNCEMENTS #################################
################################################################################

@login_required
def announcement_list(request):
    announcements = Announcement.objects.all()
    return render(request, 'main/announcement_list.html', {'announcements': announcements})

@login_required
def announcement_detail(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    return render(request, 'main/announcement_detail.html', {'announcement': announcement})

@staff_member_required()
def pin_announcement(request, pk):
    a = Announcement.objects.get(pk=pk)
    a.pin()
    return redirect('announcement-list')

@staff_member_required()
def unpin_announcement(request, pk):
    a = Announcement.objects.get(pk=pk)
    a.unpin()
    return redirect('announcement-list')

@staff_member_required()
def announcement_create(request):
    form = AnnouncementForm(request.POST or None)
    if form.is_valid():
        a = form.save(commit=False)
        a.author = request.user.profile
        a.save()

        image_files = request.FILES.getlist('image-files')
        image_links = request.POST.getlist('image-links')
        youtube_videos = request.POST.getlist('youtube-videos')

        for image_file in image_files:
            f = ImageFile(image_file=image_file, announcement=a)
            f.save()
        for image_link in image_links:
            link = ImageLink(image_link=image_link, announcement=a)
            link.save()
        for youtube_video in youtube_videos:
            video = YouTubeVideo(youtube_video=youtube_video, announcement=a)
            video.save()

        return redirect('announcement-list')
    return render(request, 'main/announcement_create.html', {'form': form})

@staff_member_required()
def announcement_update(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    announcement = Announcement.objects.get(pk=pk)
    form = AnnouncementForm(request.POST or None, instance=announcement)
    if form.is_valid():
        a = form.save()

        image_files = request.FILES.getlist('image-files')
        image_links = request.POST.getlist('image-link[]')
        youtube_videos = request.POST.getlist('youtube-video[]')

        for image_file in image_files:
            f = ImageFile(image_file=image_file, announcement=a)
            f.save()
        for image_link in image_links:
            link = ImageLink(image_link=image_link, announcement=a)
            link.save()
        for youtube_video in youtube_videos:
            video = YouTubeVideo(youtube_video=youtube_video, announcement=a)
            video.save()

        # TODO: Define model's get_absolute_url() and redirect() to the model instance redirect(model_instance)
        return redirect(announcement)
    return render(request, 'main/announcement_update.html', {'form': form, 'announcement': announcement})

@staff_member_required()
def announcement_delete(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    announcement = Announcement.objects.get(pk=pk)
    announcement.delete()
    return redirect('announcement-list')

################################################################################
#################################### EVENTS ####################################
################################################################################

@login_required
def event_list(request):
    events = Event.objects.all().reverse()
    return render(request, 'main/event_list.html', {'events': events})

@login_required
def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'main/event_detail.html', {'event': event})

@staff_member_required()
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event-list')
    else:
        print(request.POST)
        print(form.errors)
    return render(request, 'main/event_create.html', {'form': form})

@staff_member_required()
def event_update(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    event = Event.objects.get(pk=pk)
    form = EventForm(request.POST or None, instance=Event.objects.get(pk=pk))
    if form.is_valid():
        form.save()
        #TODO: Give a confirmation message at the top of form ("successfully updated") instead of redirecting immediately? Same for events, announcements, etc.?
        return redirect('event-list')
    return render(request, 'main/event_update.html', {'form': form, 'event': event})

@staff_member_required()
def event_delete(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    event = Event.objects.get(pk=pk)
    event.delete()
    return redirect('event-list')

################################################################################
#################################### POLLS #####################################
################################################################################

@login_required
def poll_list(request):
    voted_polls_id_list = request.user.profile.votes.values('poll_id')
    open_polls = Poll.objects.filter(is_open=True)
    closed_polls = Poll.objects.exclude(is_open=True)
    voted_polls= open_polls.filter(pk__in=voted_polls_id_list)
    unvoted_polls = open_polls.exclude(pk__in=voted_polls_id_list)
    return render(request, 'main/poll_list.html', {'voted_polls': voted_polls, 'unvoted_polls':unvoted_polls, 'closed_polls' : closed_polls})

@login_required
def poll_detail(request, pk):
    poll = Poll.objects.get(pk=pk)
    return render(request, 'main/poll_detail.html', {'poll': poll})

@staff_member_required()
def pin_poll(request, pk):
    p = Poll.objects.get(pk=pk)
    p.pin()
    return redirect('poll-list')

@staff_member_required()
def unpin_poll(request, pk):
    p = Poll.objects.get(pk=pk)
    p.unpin()
    return redirect('poll-list')

@staff_member_required()
def poll_create(request):
    form = PollForm(request.POST or None)
    if form.is_valid():
        p = form.save(commit=False)
        p.author = request.user.profile
        p.save()
        choices = request.POST.getlist('choice[]')
        for choice in choices:
            c = Choice(content=choice, poll=p)
            c.save()
        return redirect('poll-list')
    return render(request, 'main/poll_create.html', {'form': form})

@staff_member_required()
def poll_update(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    poll = Poll.objects.get(pk=pk)
    form = PollForm(request.POST or None, instance=poll)
    if form.is_valid():
        p = form.save()

        old_choices = p.choices.all()
        for choice in old_choices:
            choice.delete()

        new_choices = request.POST.getlist('choice[]')
        for choice in new_choices:
            c = Choice(content=choice, poll=p)
            c.save()

        return redirect('poll-list')
    return render(request, 'main/poll_update.html', {'form': form, 'poll': poll})

@staff_member_required()
def poll_delete(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    poll = Poll.objects.get(pk=pk)
    poll.delete()
    return redirect('poll-list')

@staff_member_required()
def get_vote(request, poll_pk):
    poll = Poll.objects.get_or_none(pk=poll_pk)
    if poll:
        vote = poll.get_vote(request.user.profile.pk)
        if vote:
            return HttpRespones(vote.pk)
    return HttpRespones(-1)

################################################################################
#################################### OTHER #####################################
################################################################################

@staff_member_required()
def category_list(request):
    if request.method == 'POST':
        categories = request.POST.lists()
        for k,c in categories:
            if k.startswith('category'):
                pk = c[0]
                name = c[1]
                color = c[2]
                if pk == 'new':
                    new_c = Category(name=name, color=color)
                else:
                    new_c = Category.objects.get_or_none(pk=int(pk))
                    new_c.name = name
                    new_c.color = color
                new_c.save()
        return redirect('category-list')
    categories = Category.objects.all()
    return render(request, 'main/category_list.html', {'categories': categories})

def student_register(request):
    userForm = UserForm(request.POST or None)
    userProfileForm = UserProfileForm(request.POST or None)
    studentProfileForm = StudentProfileForm(request.POST or None)

    if userForm.is_valid() and userProfileForm.is_valid() and studentProfileForm.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = userForm.save(commit=False)
        user.set_password(password)
        user.save()
        userProfile = userProfileForm.save(commit=False)
        userProfile.user = user
        userProfile.save()
        studentProfile = studentProfileForm.save(commit=False)
        studentProfile.user_profile = userProfile
        studentProfile.save()
        user = authenticate(username=username, password=password)
        auth_login(request, user)
        return redirect('index')

    return render(request, 'main/student_register.html', {'userForm': userForm, 'userProfileForm': userProfileForm, 'studentProfileForm': studentProfileForm})

def register(request):
    userForm = UserForm(request.POST or None)
    userProfileForm = UserProfileForm(request.POST or None)

    if userForm.is_valid() and userProfileForm.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = userForm.save(commit=False)
        user.set_password(password)
        user.save()
        userProfile = userProfileForm.save(commit=False)
        userProfile.user = user
        userProfile.save()
        user = authenticate(username=username, password=password)
        auth_login(request, user)
        return redirect('index')
    return render(request, 'main/register.html', {'userForm': userForm, 'userProfileForm': userProfileForm})

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)
    return render(request, 'main/index.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('index')

@staff_member_required
def ytdata(request, video_id):
    try:
        json_string = urllib2.urlopen('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=' + video_id + '&format=json').read()
        data = json.loads(json_string)
        return JsonResponse(data)
    except urllib2.HTTPError as e:
        print(e.code())
        raise Http404()
