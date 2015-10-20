"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from .settings import MEDIA_ROOT, DEBUG

from students.views.students import StudentUpdateView


urlpatterns = [
    # Students urls
    url(r'^$', 'students.views.students.students_list', name='home'),
    url(r'^students/add/$', 'students.views.students.students_add', name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', StudentUpdateView.as_view(), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', 'students.views.students.students_delete', name='students_delete'),
    # Groups urls
    url(r'^groups/$', 'students.views.groups.groups_list', name='groups'),
    url(r'^groups/add/$', 'students.views.groups.groups_add', name='groups_add'),
    url(r'^groups/(?P<gid>\d+)/edit/$', 'students.views.groups.groups_edit', name='groups_edit'),
    url(r'^groups/(?P<gid>\d+)/delete/$', 'students.views.groups.groups_delete', name='groups_delete'),
    # Exams urls
    url(r'^exams/$', 'students.views.exams.exams_list', name='exams'),
    url(r'^exams/add/$', 'students.views.exams.exams_add', name='exams_add'),
    url(r'^exams/(?P<eid>\d+)/edit/$', 'students.views.exams.exams_edit', name='exams_edit'),
    url(r'^exams/(?P<eid>\d+)/delete/$', 'students.views.exams.exams_delete', name='exams_delete'),
    # Rating urls
    url(r'^ratings/$', 'students.views.ratings.ratings_list', name='ratings'),
    url(r'^ratings/add/$', 'students.views.ratings.ratings_add', name='ratings_add'),
    url(r'^ratings/(?P<rid>\d+)/edit/$', 'students.views.ratings.ratings_edit', name='ratings_edit'),
    url(r'^ratings/(?P<rid>\d+)/delete/$', 'students.views.ratings.ratings_delete', name='ratings_delete'),
    # Contact Admin Form
    url(r'^contact_admin/$', 'students.views.contact_admin.contact_admin', name='contact_admin'),


    # Admin urls
    url(r'^admin/', include(admin.site.urls)),


]

if DEBUG:
    # serve files from media folder
    urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}))
