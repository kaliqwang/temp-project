from models import *
from forms import *

from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

def parent_register(request):
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
        return redirect('base:index')
    return render(request, 'accounts/register_parent.html', {'userForm': userForm, 'userProfileForm': userProfileForm})

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
        userProfile.is_student = True
        userProfile.save()
        studentProfile = studentProfileForm.save(commit=False)
        studentProfile.user_profile = userProfile
        studentProfile.save()
        user = authenticate(username=username, password=password)
        auth_login(request, user)
        return redirect('base:index')
    return render(request, 'accounts/register_student.html', {'userForm': userForm, 'userProfileForm': userProfileForm, 'studentProfileForm': studentProfileForm})

def teacher_register(request):
    userForm = UserForm(request.POST or None)
    userProfileForm = UserProfileForm(request.POST or None)
    teacherProfileForm = TeacherProfileForm(request.POST or None)
    if userForm.is_valid() and userProfileForm.is_valid() and teacherProfileForm.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = userForm.save(commit=False)
        user.set_password(password)
        user.save()
        userProfile = userProfileForm.save(commit=False)
        userProfile.user = user
        userProfile.is_teacher = true
        userProfile.save()
        teacherProfile = teacherProfileForm.save(commit=False)
        teacherProfile.user_profile = userProfile
        teacherProfile.save()
        user = authenticate(username=username, password=password)
        auth_login(request, user)
        return redirect('base:index')
    return render(request, 'accounts/register_teacher.html', {'userForm': userForm, 'userProfileForm': userProfileForm, 'teacherProfileForm': teacherProfileForm})

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    target_url = request.GET.get('next')
    user = authenticate(username=username, password=password)
    if user:
        auth_login(request, user)
        if target_url:
            return redirect(target_url)
    return render(request, 'accounts/login.html')

@login_required
def logout(request):
    auth_logout(request)
    return redirect('base:index')

@staff_member_required
def generator(request, model, count):
    if request.method == 'POST':
        generated_count = 0
        if model == 'student_profile':
            generated_count = StudentProfile.generate_random_objects(int(count))
        if (generated_count == int(count)):
            return HttpResponse('Success: %d %s were generated' % (generated_count, model))
        else:
            return HttpResponse('Error: %d %s were generated' % (generated_count, model))
