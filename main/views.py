from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from serializers import EventSerializer

from django.http import HttpResponse

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


from models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from forms import *

from django.utils import timezone

def index(request):
    return render(request, 'main/index.html')

def announcement_list(request):
    announcements = Announcement.objects.all()
    categories = Category.objects.all()
    return render(request, 'main/announcement_list.html', {'announcements': announcements, 'categories': categories})

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
        a.author = request.user
        a.save()

        image_files = request.FILES
        image_links = request.POST.getlist('image-link[]')
        youtube_videos = request.POST.getlist('youtube-video[]')

        for image_file in request.FILES.getlist('image-file[]'):
            f = ImageFile(image_file=image_file, announcement=a)
            f.save()
        for image_link in image_links:
            link = ImageLink(image_link=image_link, announcement=a)
            link.save()
        for youtube_video in youtube_videos:
            video = YoutubeVideo(youtube_video=youtube_video, announcement=a)
            video.save()

        return redirect('announcement-list')
    return render(request, 'main/announcement_create.html', {'form': form})

@staff_member_required()
def announcement_update(request, pk):
    # restrict access to either the original author or a superuser admin
    announcement = Announcement.objects.get(pk=pk)
    form = AnnouncementForm(request.POST or None, instance=announcement)
    if form.is_valid():
        a = form.save()

        image_files = request.FILES
        image_links = request.POST.getlist('image-link[]')
        youtube_videos = request.POST.getlist('youtube-video[]')

        for image_file in request.FILES.getlist('image-file[]'):
            f = ImageFile(image_file=image_file, announcement=a)
            f.save()

        for image_link in image_links:
            link = ImageLink(image_link=image_link, announcement=a)
            link.save()

        for youtube_video in youtube_videos:
            video = YoutubeVideo(youtube_video=youtube_video, announcement=a)
            video.save()

        return redirect('announcement-list')
    return render(request, 'main/announcement_update.html', {'form': form, 'announcement': announcement})

@staff_member_required()
def announcement_delete(request, pk):
    # restrict access to either the original author or a superuser admin
    announcement = Announcement.objects.get(pk=pk)
    announcement.delete()
    return redirect('announcement-list')






def event_list(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    return render(request, 'main/event_list.html', {'events': events, 'categories': categories})

def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'main/event_detail.html', {'event': event})

@staff_member_required()
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event-list')
    return render(request, 'main/event_create.html', {'form': form})

@staff_member_required()
def event_update(request, pk):
    # restrict access to either the original author or a superuser admin
    event = Event.objects.get(pk=pk)
    form = EventForm(request.POST or None, instance=Event.objects.get(pk=pk))
    if form.is_valid():
        form.save()
        #TODO: Give a confirmation message at the top of form ("successfully updated") instead of redirecting immediately? Same for events, announcements, etc.?
        return redirect('event-list')
    return render(request, 'main/event_update.html', {'form': form, 'event': event})

@staff_member_required()
def event_delete(request, pk):
    # restrict access to either the original author or a superuser admin
    event = Event.objects.get(pk=pk)
    event.delete()
    return redirect('event-list')






def poll_list(request):
    categories = Category.objects.all()

    polls_voted_id_list = request.user.votes.values('poll_id')

    open_polls = Poll.objects.filter(is_open=True)
    closed_polls = Poll.objects.exclude(is_open=True)

    polls_voted = open_polls.filter(pk__in=polls_voted_id_list)
    polls_unvoted = open_polls.exclude(pk__in=polls_voted_id_list)

    return render(request, 'main/poll_list.html', {'polls_voted': polls_voted, 'polls_unvoted': polls_unvoted, 'closed_polls' : closed_polls, 'categories': categories})

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
        p.author = request.user
        p.save()
        choices = request.POST.getlist('choice[]')
        for choice in choices:
            c = Choice(content=choice, poll=p)
            c.save()
        return redirect('poll-list')
    return render(request, 'main/poll_create.html', {'form': form})

@staff_member_required()
def poll_update(request, pk):
    # restrict access to either the original author or a superuser admin
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

        #TODO: Give a confirmation message at the top of form ("successfully updated") instead of redirecting immediately? Same for events, announcements, etc.?
        return redirect('poll-list')
    return render(request, 'main/poll_update.html', {'form': form, 'poll': poll})

@staff_member_required()
def poll_delete(request, pk):
    # restrict access to either the original author or a superuser admin
    poll = Poll.objects.get(pk=pk)
    poll.delete()
    return redirect('poll-list')






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
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        studentProfileForm = StudentProfileForm(request.POST)

        if userForm.is_valid() and studentProfileForm.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = userForm.save(commit=False)
            user.set_password(password)
            user.save()
            studentProfile = studentProfileForm.save(commit=False)
            studentProfile.user = user
            studentProfile.save()
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('index')
        else:
            pass
    else:
        userForm = UserForm()
        studentProfileForm = StudentProfileForm()
    return render(request, 'main/student_register.html', {'userForm': userForm, 'studentProfileForm': studentProfileForm})

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



# def votes(request, choice_pk):
#     # check for None matching case?
#     vote = request.user.votes.filter(choice__pk=choice_pk)
#     return HttpResponse(vote.pk)


def votes(request, poll_pk):
    # check for None matching case?
    #Find the poll using poll.pk
    selected_Poll= Poll.objects.all().get(id=poll_pk)
    a = 0;
    #for every choice associated with that poll, if not null, vote = that.
    for choice in selected_Poll.choices.all():
        try:
           vote = request.user.votes.get(choice_id=choice.pk)
        except:
           pass
    return HttpResponse(vote.pk)
