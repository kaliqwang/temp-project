from __future__ import unicode_literals

from categories.models import *

from django.shortcuts import render

from django.contrib.admin.views.decorators import staff_member_required

def index(request):
    return render(request, 'base/index.html')

@staff_member_required
def generator(request):
    categories_count = Category.objects.count()
    return render(request, 'base/generator.html', {'categories_count': categories_count})
