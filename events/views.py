from models import *
from forms import *
from categories.models import *
from push_notifications.models import APNSDevice

from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def event_list(request):
    hidden = request.user.profile.categories_hidden_announcements.values_list('pk', flat=True)
    categories_hidden_announcements = Category.objects.filter(pk__in=hidden)
    categories_shown = Category.objects.exclude(pk__in=hidden)
    return render(request, 'events/event_list.html', {'categories_shown': categories_shown, 'categories_hidden_announcements': categories_hidden_announcements})

@login_required
def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@staff_member_required()
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        devices = APNSDevice.objects.all()
        devices.send_message("New Event!");
        return redirect('events:list')
    return render(request, 'events/event_create.html', {'form': form})

@staff_member_required()
def event_update(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    event = Event.objects.get(pk=pk)
    form = EventForm(request.POST or None, instance=Event.objects.get(pk=pk))
    if form.is_valid():
        form.save()
        #TODO: Give a confirmation message at the top of form ("successfully updated") instead of redirecting immediately? Same for events, announcements, etc.?
        return redirect(event)
    return render(request, 'events/event_update.html', {'form': form, 'event': event})

@staff_member_required()
def event_delete(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    event = Event.objects.get(pk=pk)
    event.delete()
    return redirect('events:list')

@staff_member_required
def generator(request, count):
    if request.method == 'POST':
        generated_count = Event.generate_random_objects(int(count))
        if (generated_count == int(count)):
            return HttpResponse('Success: %d events were generated' % generated_count)
        else:
            return HttpResponse('Error: %d events were generated' % generated_count)
