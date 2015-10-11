__author__ = 'travelist'
# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Rating, Student


# Views for Exams
def ratings_list(request):
    ratings = Rating.objects.all()

    # try to order rating list
    reverse_begin = False
    order_by = request.GET.get('order_by', '')
    if order_by in ('id', 'student_ball', 'exam_title', 'date_exam' 'ball'):
        ratings = ratings.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            ratings = ratings.reverse()
    else:
        ratings = ratings.order_by('student_ball')
        reverse_begin = True

    # paginate students
    paginator = Paginator(ratings, 4)
    page = request.GET.get('page', '1')
    number_on_page = (int(page) - 1) * 4

    try:
        ratings = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        ratings = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        ratings = paginator.page(paginator.num_pages)

    return render(request, 'students/ratings_list.html', {'ratings': ratings,
                                                         'reverse_begin': reverse_begin,
                                                         'number_on_page': number_on_page})

def ratings_add(request):
    return HttpResponse('<h1>rating Add Form</h1>')

def ratings_edit(request, gid):
    return HttpResponse('<h1>Edit rating %s</h1>' % gid)

def ratings_delete(request, gid):
    return HttpResponse('<h1>Delete rating %s</h1>' % gid)
