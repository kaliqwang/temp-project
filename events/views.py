from .models import *
from .forms import *
from categories.models import *
from push_notifications.models import APNSDevice

from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def event_list(request):
    hidden = request.user.profile.categories_hidden_events.values_list('pk', flat=True)
    categories_hidden_events = Category.objects.filter(pk__in=hidden)
    categories_shown = Category.objects.exclude(pk__in=hidden)
    return render(request, 'events/event_list.html', {'categories_shown': categories_shown, 'categories_hidden_events': categories_hidden_events})

@login_required
def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@staff_member_required()
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        e = form.save(commit=False)
        e.author = request.user.profile
        e.save()

        # TODO: Push Notifications
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
def generator(request):
    if request.method == 'POST':
        count = int(request.GET.get('count'))
        generated_count = Event.generate_random_objects(count)
        if (generated_count == count):
            return HttpResponse('Success: %d events were generated' % generated_count)
        else:
            return HttpResponse('Error: %d events were generated' % generated_count)
