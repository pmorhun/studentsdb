# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Student

# Views for Students

def students_list(request):
    students = Student.objects.all()

    # try to order students list
    reverse_begin = False
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'last_name', 'first_name', 'student_group', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
    else:
        students = students.order_by('last_name')
        reverse_begin = True

    # paginate students
    paginator = Paginator(students, 3)
    page = request.GET.get('page', '1')
    number_on_page = (int(page) - 1) * 3

    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        students = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        students = paginator.page(paginator.num_pages)

    return render(request, 'students/students_list.html', {'students': students,
                                                           'reverse_begin': reverse_begin,
                                                           'number_on_page': number_on_page})


def students_add(request):
    return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
    return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
    return HttpResponse('<h1>Delete Student %s</h1>' % sid)
