# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


# Views for Students
def students_list(request):

    students = (
        {'id': 1,
        'first_name': u'Віталій',
        'last_name': u'Подоба',
        'ticket': 235,
        'image': 'img/st1.jpg'},
        {'id': 2,
        'first_name': u'Корост',
        'last_name': u'Андрій',
        'ticket': 2123,
        'image': 'img/st2.jpg'},
        {'id': 2,
        'first_name': u'Янукович',
        'last_name': u'Віктор',
        'ticket': 23,
        'image': 'img/st3.jpg'},
        )
    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)

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
