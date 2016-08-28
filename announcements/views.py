from .models import *
from .forms import *
from categories.models import *
from push_notifications.models import APNSDevice

import json
import requests

from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def announcement_list(request):
    hidden = request.user.profile.categories_hidden_announcements.values_list('pk', flat=True)
    categories_hidden_announcements = Category.objects.filter(pk__in=hidden)
    categories_shown = Category.objects.exclude(pk__in=hidden)
    return render(request, 'announcements/announcement_list.html', {'categories_shown': categories_shown, 'categories_hidden_announcements': categories_hidden_announcements})

@login_required
def announcement_detail(request, pk):
    announcement = Announcement.objects.get(pk=pk)
    return render(request, 'announcements/announcement_detail.html', {'announcement': announcement})

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

        # TODO: Push Notifications
        devices = APNSDevice.objects.all()
        devices.send_message("New Announcement!");

        return redirect('announcements:list')
    return render(request, 'announcements/announcement_create.html', {'form': form})

@staff_member_required()
def announcement_update(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    announcement = Announcement.objects.get(pk=pk)
    form = AnnouncementForm(request.POST or None, instance=announcement)
    if form.is_valid():
        a = form.save()

        image_files = request.FILES.getlist('image-files')
        image_links = request.POST.getlist('image-links')
        youtube_videos = request.POST.getlist('youtube-videos')

        for image_file in image_files:
            i = ImageFile(image_file=image_file, announcement=a)
            i.save()
        for image_link in image_links:
            i = ImageLink(image_link=image_link, announcement=a)
            i.save()
        for youtube_video in youtube_videos:
            v = YouTubeVideo(youtube_video=youtube_video, announcement=a)
            v.save()

        # TODO: Define model's get_absolute_url() and redirect() to the model instance redirect(model_instance)
        return redirect(announcement)
    return render(request, 'announcements/announcement_update.html', {'form': form, 'announcement': announcement})

@staff_member_required()
def announcement_delete(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    announcement = Announcement.objects.get(pk=pk)
    announcement.delete()
    return redirect('announcements:list')

@staff_member_required()
def pin_announcement(request, pk):
    a = Announcement.objects.get(pk=pk)
    a.pin()
    return redirect('announcements:list')

@staff_member_required()
def unpin_announcement(request, pk):
    a = Announcement.objects.get(pk=pk)
    a.unpin()
    return redirect('announcements:list')

@staff_member_required
def ytdata(request, video_id):
    r = requests.get('https://www.youtube.com/oembed?url=http://www.youtube.com/watch?v=' + video_id + '&format=json')
    if r.status_code == 200:
        json_data = r.text
        data = json.loads(json_data)
        return JsonResponse(data)
    else:
        raise Http404()

@staff_member_required
def generator(request):
    if request.method == 'POST':
        count = int(request.GET.get('count'))
        generated_count = Announcement.generate_random_objects(count)
        if (generated_count == count):
            return HttpResponse('Success: %d announcements were generated' % generated_count)
        else:
            return HttpResponse('Error: %d announcements were generated' % generated_count)
