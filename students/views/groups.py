# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Group


# Views for Groups
def groups_list(request):
    groups = Group.objects.all()

    # try to order group list
    reverse_begin = False
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()
    else:
        groups = groups.order_by('title')
        reverse_begin = True

    # paginate students
    paginator = Paginator(groups, 4)
    page = request.GET.get('page', '1')
    number_on_page = (int(page) - 1) * 4

    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        groups = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        groups = paginator.page(paginator.num_pages)

    return render(request, 'students/groups_list.html', {'groups': groups,
                                                         'reverse_begin': reverse_begin,
                                                         'number_on_page': number_on_page})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
