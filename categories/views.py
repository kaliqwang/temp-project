from models import *

from django.shortcuts import render, redirect

from django.contrib.admin.views.decorators import staff_member_required

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
    categories = Category.objects.all()
    return render(request, 'categories/category_list.html', {'categories': categories})

@staff_member_required
def category_merge(request):
    category_pks = request.GET.getlist('category')
    categories = Category.objects.filter(pk__in=category_pks)
    new_name = request.GET.get('new_name')
    new_color = request.GET.get('new_color')
    if categories:
        Category.merge(categories=categories, new_name=new_name, new_color=new_color)
    return redirect('categories:list')
