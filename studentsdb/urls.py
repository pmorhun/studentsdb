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
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import RedirectView, TemplateView

from .settings import MEDIA_ROOT, DEBUG

from students.views.students import StudentView, StudentAddView, StudentUpdateView, StudentDeleteView
from students.views.journal import JournalView
from students.views.groups import GroupView, GroupAddView, GroupUpdateView, GroupDeleteView
from students.views.exams import ExamView, ExamAddView, ExamUpdateView, ExamDeleteView
from students.views.ratings import RatingView, RatingAddView, RatingUpdateView, RatingDeleteView


js_info_dict = {'packages': ('students',),}

urlpatterns = [
    # Students urls
    url(r'^$', StudentView.as_view(), name='home'),
    url(r'^students/add/$', login_required(StudentAddView.as_view()), name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', login_required(StudentUpdateView.as_view()), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', login_required(StudentDeleteView.as_view()), name='students_delete'),
    # Journal urls
    url(r'^journal/(?P<pk>\d+)?/?$', login_required(JournalView.as_view()), name='journal'),
    # Groups urls
    url(r'^groups/$', login_required(GroupView.as_view()), name='groups'),
    url(r'^groups/add/$', login_required(GroupAddView.as_view()), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', login_required(GroupUpdateView.as_view()), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', login_required(GroupDeleteView.as_view()), name='groups_delete'),
    # Exams urls
    url(r'^exams/$', login_required(ExamView.as_view()), name='exams'),
    url(r'^exams/add/$', login_required(ExamAddView.as_view()), name='exams_add'),
    url(r'^exams/(?P<pk>\d+)/edit/$', login_required(ExamUpdateView.as_view()), name='exams_edit'),
    url(r'^exams/(?P<pk>\d+)/delete/$', login_required(ExamDeleteView.as_view()), name='exams_delete'),
    # Rating urls
    url(r'^ratings/$', login_required(RatingView.as_view()), name='ratings'),
    url(r'^ratings/add/$', login_required(RatingAddView.as_view()), name='ratings_add'),
    url(r'^ratings/(?P<pk>\d+)/edit/$', login_required(RatingUpdateView.as_view()), name='ratings_edit'),
    url(r'^ratings/(?P<pk>\d+)/delete/$', login_required(RatingDeleteView.as_view()), name='ratings_delete'),
    # Contact Admin Form
    url(r'^contact_admin/$', 'students.views.contact_admin.contact_admin', name='contact_admin'),
    # User Related urls
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),
    # Admin urls
    url(r'^admin/', include(admin.site.urls)),
    # Js internationalization urls
    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),


]

if DEBUG:
    # serve files from media folder
    urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT}))
