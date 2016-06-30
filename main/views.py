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

import urllib2
import json

def announcement_list(request):
    announcements = Announcement.objects.all()
    categories = Category.objects.all()
    return render(request, 'main/announcement_list.html', {'announcements': announcements, 'categories': categories})

class EventData(APIView):

    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self):
        pass

def index(request):
    return render(request, 'main/index.html')

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

        return redirect('announcements')
    else:
        print(form.errors)
    return render(request, 'main/announcement_create.html', {'form': form})

@staff_member_required()
def pin_announcement(request, pk):
    a = Announcement.objects.get(pk=pk)
    a.pin()
    return redirect('announcements')

@staff_member_required()
def unpin_announcement(request, pk):
    a = Announcement.objects.get(pk=pk)
    a.unpin()
    return redirect('announcements')

@staff_member_required()
def poll_create(request):
    form = PollForm(request.POST or None)
    if form.is_valid():
        p = form.save(commit=False)
        p.author = request.user
        p.save()
        choices = request.POST.getlist('choice[]')
        for choice in choices:
            if choice != "":
                c = Choice(poll=p, subject=choice)
                c.save()
        return redirect('polls')
    return render(request, 'main/poll_create.html', {'form': form})

@staff_member_required()
def pin_poll(request, pk):
    a = Poll.objects.get(pk=pk)
    a.pin()
    return redirect('polls')

@staff_member_required()
def unpin_poll(request, pk):
    a = Poll.objects.get(pk=pk)
    a.unpin()
    return redirect('polls')

@staff_member_required()
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        e = form.save()
        return redirect('events')
    else:
        print(form.errors)
    return render(request, 'main/event_create.html', {'form': form})

@staff_member_required()
def category_create(request):
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
        return redirect('category_create')
    categories = Category.objects.all()
    return render(request, 'main/category_create.html', {'categories': categories})

@method_decorator(staff_member_required, name='dispatch')
class AnnouncementUpdate(UpdateView):
    model = Announcement
    fields = '__all__'
    template_name_suffix = '_update'
    success_url = reverse_lazy('index')

@method_decorator(staff_member_required, name='dispatch')
class AnnouncementDelete(DeleteView):
    model = Announcement
    template_name_suffix = '_delete'
    success_url = reverse_lazy('index')


class EventList(ListView):
    model = Event

@method_decorator(staff_member_required, name='dispatch')
class EventUpdate(UpdateView):
    model = Event
    fields = '__all__'
    template_name_suffix = '_update'
    success_url = reverse_lazy('index')

@method_decorator(staff_member_required, name='dispatch')
class EventDelete(DeleteView):
    model = Event
    template_name_suffix = '_delete'
    success_url = reverse_lazy('index')


class PollList(ListView):
    model = Poll

@method_decorator(staff_member_required, name='dispatch')
class PollUpdate(UpdateView):
    model = Poll
    fields = '__all__'
    template_name_suffix = '_update'
    success_url = reverse_lazy('index')

@method_decorator(staff_member_required, name='dispatch')
class PollDelete(DeleteView):
    model = Poll
    template_name_suffix = '_delete'
    success_url = reverse_lazy('index')

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
        studentProfileForm = studentProfileForm()
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
