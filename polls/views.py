from models import *
from forms import *
from categories.models import *

from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@login_required
def poll_list(request):
    polls = Poll.objects.all()
    categories = Category.objects.all()
    polls_voted_id_list = request.user.profile.votes.values('poll_id')
    polls_open = polls.filter(is_open=True)
    polls_closed = polls.exclude(is_open=True)
    polls_voted= polls.filter(pk__in=polls_voted_id_list)
    polls_unvoted = polls.exclude(pk__in=polls_voted_id_list)
    return render(request, 'polls/poll_list.html', {'polls_voted': polls_voted, 'polls_unvoted':polls_unvoted, 'polls_closed' : polls_closed, 'categories': categories})

@login_required
def poll_detail(request, pk):
    poll = Poll.objects.get(pk=pk)
    return render(request, 'polls/poll_detail.html', {'poll': poll})

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
        return redirect('polls:list')
    return render(request, 'polls/poll_create.html', {'form': form})

@staff_member_required()
def poll_update(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    poll = Poll.objects.get(pk=pk)
    form = PollForm(request.POST or None, instance=poll)
    #New Stuff
    if form.is_valid():
        p = form.save()
        new_choices = request.POST.getlist('new-choice[]')
        for choice in new_choices:
            c = Choice(content=choice, poll=p)
            c.save()
        return redirect(poll)
    return render(request, 'polls/poll_update.html', {'form': form, 'poll': poll})

@staff_member_required()
def poll_delete(request, pk):
    #TODO: restrict access to either the original author or a superuser admin
    poll = Poll.objects.get(pk=pk)
    poll.delete()
    return redirect('polls:list')

@staff_member_required()
def pin_poll(request, pk):
    p = Poll.objects.get(pk=pk)
    p.pin()
    return redirect('polls:list')

@staff_member_required()
def unpin_poll(request, pk):
    p = Poll.objects.get(pk=pk)
    p.unpin()
    return redirect('polls:list')

@login_required
def get_vote(request, poll_pk):
    poll = Poll.objects.get_or_none(pk=poll_pk)
    if poll:
        vote = poll.get_vote(request.user.profile.pk)
        if vote:
            return HttpResponse(vote.pk)
    return HttpResponse(-1)

@staff_member_required()
def get_vote_count(request, choice_pk):
    choice = Choice.objects.get_or_none(pk=poll_pk)
    if choice:
        return HttpResponse(choice.vote_count())
    return HttpResponse(-1)

@staff_member_required
def generator(request, count):
    if request.method == 'POST':
        generated_count = Poll.generate_random_objects(int(count), add_votes=False)
        if (generated_count == int(count)):
            return HttpResponse('Success: %d polls were generated' % generated_count)
        else:
            return HttpResponse('Error: %d polls were generated' % generated_count)
