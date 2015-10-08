# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


from ..models import Student

# Views for Students

def students_list(request):
    students = Student.objects.all()

    # try to order students list
    reverse_begin = False
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        students = students.order_by('last_name')
        reverse_begin = True

    # paginate students

    page = request.GET.get('page', '')
    count_page = len(students) // 3 + 1

    if page != '':
        page = int(page)
    else:
        page = 1
    pages = range(1, count_page + 1)
    if page == 1:
        students = students.filter(id__gte=1, id__lt=6)
    elif page > 9999:
        students = students.filter(id__gte=len(pages) * 3 - 3)
    else:
        students = students.filter(id__gte=page * 3 - 3, id__lt=page * 3)

    return render(request, 'students/students_list.html', {'students': students,
                                                           'reverse_begin': reverse_begin,
                                                           'pages': pages,
                                                           'page': page})


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
