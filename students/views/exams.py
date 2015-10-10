__author__ = 'travelist'
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Exam


# Views for Exams
def exams_list(request):
    exams = Exam.objects.all()

    # try to order exam list
    reverse_begin = False
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'title', 'teacher', 'exam_group'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()
    else:
        exams = exams.order_by('title')
        reverse_begin = True

    # paginate students
    paginator = Paginator(exams, 4)
    page = request.GET.get('page', '1')
    number_on_page = (int(page) - 1) * 4

    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        exams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        exams = paginator.page(paginator.num_pages)

    return render(request, 'students/exams_list.html', {'exams': exams,
                                                         'reverse_begin': reverse_begin,
                                                         'number_on_page': number_on_page})

def exams_add(request):
    return HttpResponse('<h1>exam Add Form</h1>')

def exams_edit(request, gid):
    return HttpResponse('<h1>Edit exam %s</h1>' % gid)

def exams_delete(request, gid):
    return HttpResponse('<h1>Delete exam %s</h1>' % gid)
