# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

# Views for Groups
def groups_list(request):

    groups = (
        {'id': 1,
        'group_name': u'Мехмат',
        'boss': u'Подоба',
        'note': u'1 year'},

        {'id': 2,
        'group_name': u'РФФ',
        'boss': u'Чіпа',
        'note': u'1 year'},

        {'id': 3,
        'group_name': u'Рфф 2',
        'boss': u'Бех',
        'note': u'2 year'},
    )

    return render(request, 'students/groups_list.html', {'groups': groups, 'group_link': request.path})

def groups_add(request):
    return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
    return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
    return HttpResponse('<h1>Delete Group %s</h1>' % gid)
